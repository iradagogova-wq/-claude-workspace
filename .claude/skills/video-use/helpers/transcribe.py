"""Transcribe a video with Deepgram.

Extracts mono 16kHz audio via ffmpeg, uploads to Deepgram (nova-2 model)
with diarize + smart-format + filler-words + word-level timestamps, and
writes a Scribe-schema-compatible transcript to
<edit_dir>/transcripts/<video_stem>.json — so every downstream helper
(pack_transcripts.py, render.py, timeline_view.py) keeps working unchanged.

Cached: if the output file already exists, the upload is skipped.

Usage:
    python helpers/transcribe.py <video_path>
    python helpers/transcribe.py <video_path> --edit-dir /custom/edit
    python helpers/transcribe.py <video_path> --language en
    python helpers/transcribe.py <video_path> --num-speakers 2
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests


DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"
DEEPGRAM_MODEL = "nova-2"


def load_api_key() -> str:
    for candidate in [Path(__file__).resolve().parent.parent / ".env", Path(".env")]:
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "DEEPGRAM_API_KEY":
                    return v.strip().strip('"').strip("'")
    v = os.environ.get("DEEPGRAM_API_KEY", "")
    if not v:
        sys.exit("DEEPGRAM_API_KEY not found in .env or environment")
    return v


def extract_audio(video_path: Path, dest: Path) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(dest),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _deepgram_words_to_scribe_words(dg_payload: dict) -> list[dict]:
    """Flatten Deepgram's word list into Scribe's {type, text, start, end,
    speaker_id} shape, synthesizing 'spacing' entries between words so the
    silence-based phrase grouping in pack_transcripts.py / timeline_view.py
    needs no changes.

    Deepgram has no audio-event tagging ((laughter), (applause), ...), so
    no 'audio_event' entries are produced — everything else in the schema
    downstream code reads is preserved.
    """
    try:
        alt = dg_payload["results"]["channels"][0]["alternatives"][0]
    except (KeyError, IndexError, TypeError):
        return []

    words: list[dict] = []
    prev_end: float | None = None
    for w in alt.get("words", []):
        start = w.get("start")
        end = w.get("end")
        if start is None or end is None:
            continue

        if prev_end is not None and start > prev_end:
            words.append({"type": "spacing", "text": " ", "start": prev_end, "end": start})

        entry: dict = {
            "type": "word",
            "text": w.get("punctuated_word") or w.get("word", ""),
            "start": start,
            "end": end,
        }
        speaker = w.get("speaker")
        if speaker is not None:
            entry["speaker_id"] = f"speaker_{speaker}"
        words.append(entry)
        prev_end = end

    return words


def call_deepgram(
    audio_path: Path,
    api_key: str,
    language: str | None = None,
    num_speakers: int | None = None,
) -> dict:
    params: dict[str, str] = {
        "model": DEEPGRAM_MODEL,
        "diarize": "true",
        "smart_format": "true",
        "punctuate": "true",
        "filler_words": "true",
    }
    if language:
        params["language"] = language
    else:
        params["detect_language"] = "true"
    if num_speakers:
        # Deepgram's diarization auto-detects speaker count; there is no
        # "expected speakers" parameter in the prerecorded API. Kept as a
        # CLI/API arg for compatibility with transcribe_batch.py; ignored here.
        print(
            f"  note: --num-speakers {num_speakers} is not supported by Deepgram diarization, ignoring",
            file=sys.stderr,
        )

    with open(audio_path, "rb") as f:
        resp = requests.post(
            DEEPGRAM_URL,
            headers={"Authorization": f"Token {api_key}", "Content-Type": "audio/wav"},
            params=params,
            data=f,
            timeout=1800,
        )

    if resp.status_code != 200:
        raise RuntimeError(f"Deepgram returned {resp.status_code}: {resp.text[:500]}")

    dg_payload = resp.json()
    try:
        transcript_text = dg_payload["results"]["channels"][0]["alternatives"][0].get("transcript", "")
    except (KeyError, IndexError, TypeError):
        transcript_text = ""

    return {
        "provider": "deepgram",
        "model": DEEPGRAM_MODEL,
        "language": language or "auto",
        "transcript": transcript_text,
        "words": _deepgram_words_to_scribe_words(dg_payload),
        "raw": dg_payload,
    }


def transcribe_one(
    video: Path,
    edit_dir: Path,
    api_key: str,
    language: str | None = None,
    num_speakers: int | None = None,
    verbose: bool = True,
) -> Path:
    """Transcribe a single video. Returns path to transcript JSON.

    Cached: returns existing path immediately if the transcript already exists.
    """
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcripts_dir / f"{video.stem}.json"

    if out_path.exists():
        if verbose:
            print(f"cached: {out_path.name}")
        return out_path

    if verbose:
        print(f"  extracting audio from {video.name}", flush=True)

    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / f"{video.stem}.wav"
        extract_audio(video, audio)
        size_mb = audio.stat().st_size / (1024 * 1024)
        if verbose:
            print(f"  uploading {video.stem}.wav ({size_mb:.1f} MB)", flush=True)
        payload = call_deepgram(audio, api_key, language, num_speakers)

    out_path.write_text(json.dumps(payload, indent=2))
    dt = time.time() - t0

    if verbose:
        kb = out_path.stat().st_size / 1024
        print(f"  saved: {out_path.name} ({kb:.1f} KB) in {dt:.1f}s")
        print(f"    words: {len(payload['words'])}")

    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Transcribe a video with Deepgram")
    ap.add_argument("video", type=Path, help="Path to video file")
    ap.add_argument(
        "--edit-dir",
        type=Path,
        default=None,
        help="Edit output directory (default: <video_parent>/edit)",
    )
    ap.add_argument(
        "--language",
        type=str,
        default=None,
        help="Optional ISO language code (e.g., 'en'). Omit to auto-detect.",
    )
    ap.add_argument(
        "--num-speakers",
        type=int,
        default=None,
        help="Accepted for compatibility; Deepgram diarization does not take an expected speaker count.",
    )
    args = ap.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"video not found: {video}")

    edit_dir = (args.edit_dir or (video.parent / "edit")).resolve()
    api_key = load_api_key()

    transcribe_one(
        video=video,
        edit_dir=edit_dir,
        api_key=api_key,
        language=args.language,
        num_speakers=args.num_speakers,
    )


if __name__ == "__main__":
    main()
