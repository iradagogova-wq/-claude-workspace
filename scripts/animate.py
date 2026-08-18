#!/usr/bin/env python3
"""Анимация кадров в видео — целиком внутри чата, без внешних сервисов.

Все режимы проверены на ffmpeg 7.0.2. Видео-модели не нужны: движение
делается камерой, досочинением промежуточных кадров и склейкой.

    python3 scripts/animate.py ken  кадр.png --out клип.mp4 --sec 4 --move in
    python3 scripts/animate.py morph а.png б.png --out клип.mp4 --sec 2
    python3 scripts/animate.py seq  папка/ --out клип.mp4 --fps 8
    python3 scripts/animate.py join к1.mp4 к2.mp4 --out сцена.mp4
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

W, H, FPS = 1024, 576, 24

MOVES = {
    "in":    ("min(zoom+0.0011,1.35)", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
    "out":   ("max(1.35-0.0011*on,1.0)", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
    "left":  ("1.2", "(iw-iw/zoom)*(1-on/{d})", "ih/2-(ih/zoom/2)"),
    "right": ("1.2", "(iw-iw/zoom)*(on/{d})", "ih/2-(ih/zoom/2)"),
    "up":    ("1.2", "iw/2-(iw/zoom/2)", "(ih-ih/zoom)*(1-on/{d})"),
}

INTERP = "minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:vsbmc=1"


def ffmpeg() -> str:
    try:
        import imageio_ffmpeg
    except ImportError:
        sys.exit(
            "Нет ffmpeg. Поставь один раз за сессию:\n"
            "    uv pip install --system imageio-ffmpeg"
        )
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(args: list[str]) -> None:
    proc = subprocess.run([ffmpeg(), "-y", "-v", "error", *args],
                          capture_output=True, text=True)
    if proc.returncode:
        sys.exit(f"ffmpeg упал:\n{proc.stderr.strip()[:600]}")


def frames_in(video: Path) -> int:
    out = subprocess.run(
        [ffmpeg(), "-v", "error", "-i", str(video), "-f", "rawvideo", "-y",
         "/dev/null", "-progress", "-"],
        capture_output=True, text=True).stdout
    hits = [l for l in out.splitlines() if l.startswith("frame=")]
    return int(hits[-1].split("=")[1]) if hits else 0


def report(out: Path) -> None:
    n = frames_in(out)
    if not n:
        sys.exit(f"Видео пустое: {out}. Кадров не закодировано.")
    print(f"✓ {out}  —  {n} кадров, {n / FPS:.1f} сек, {out.stat().st_size // 1024} KB")


def ken(image: Path, out: Path, sec: float, move: str) -> None:
    """Движение камеры по одному кадру: наезд, отъезд, панорама."""
    d = int(sec * FPS)
    z, x, y = MOVES[move]
    zoompan = (f"zoompan=z='{z.format(d=d)}':d={d}"
               f":x='{x.format(d=d)}':y='{y.format(d=d)}':s={W}x{H}:fps={FPS}")
    run(["-loop", "1", "-i", str(image), "-t", str(sec),
         "-vf", f"scale={W*2}:{H*2},{zoompan}",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
    report(out)


def morph(first: Path, second: Path, out: Path, sec: float) -> None:
    """Два ключевых кадра -> досочинённое движение между ними.

    minterpolate не работает на входе из двух картинок, поэтому каждая
    удерживается несколько кадров — фильтру нужен запас для оценки движения.
    """
    hold = 3
    with tempfile.TemporaryDirectory() as tmp:
        i = 1
        for src in (first, second):
            for _ in range(hold):
                shutil.copy(src, Path(tmp) / f"h{i:03d}.png")
                i += 1
        run(["-framerate", f"{2 * hold / sec:.4f}", "-i", f"{tmp}/h%03d.png",
             "-vf", f"scale={W}:{H}," + INTERP.format(fps=FPS),
             "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
    report(out)


def seq(folder: Path, out: Path, fps: float) -> None:
    """Последовательность поз -> плавная анимация на 24 кадрах."""
    images = sorted(p for p in folder.iterdir()
                    if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
    if len(images) < 3:
        sys.exit(f"Нужно минимум 3 кадра, найдено {len(images)}. "
                 "Для двух кадров используй режим morph.")
    with tempfile.TemporaryDirectory() as tmp:
        for i, src in enumerate(images, 1):
            shutil.copy(src, Path(tmp) / f"s{i:03d}{src.suffix}")
        run(["-framerate", str(fps), "-i", f"{tmp}/s%03d{images[0].suffix}",
             "-vf", f"scale={W}:{H}," + INTERP.format(fps=FPS),
             "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
    print(f"   из {len(images)} поз")
    report(out)


def join(clips: list[Path], out: Path, fade: float) -> None:
    """Склейка планов в сцену с перекрёстными затуханиями."""
    if len(clips) == 1:
        shutil.copy(clips[0], out)
        report(out)
        return

    inputs: list[str] = []
    for clip in clips:
        inputs += ["-i", str(clip)]

    parts = [f"[{i}:v]scale={W}:{H},setsar=1,fps={FPS}[c{i}]" for i in range(len(clips))]
    prev, offset = "c0", frames_in(clips[0]) / FPS - fade
    for i in range(1, len(clips)):
        label = f"x{i}"
        parts.append(f"[{prev}][c{i}]xfade=transition=fade"
                     f":duration={fade}:offset={max(offset, 0.1):.2f}[{label}]")
        prev = label
        offset += frames_in(clips[i]) / FPS - fade

    run([*inputs, "-filter_complex", ";".join(parts), "-map", f"[{prev}]",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
    print(f"   склеено планов: {len(clips)}")
    report(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("ken", help="движение камеры по одному кадру")
    p.add_argument("image", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--sec", type=float, default=4)
    p.add_argument("--move", choices=sorted(MOVES), default="in")

    p = sub.add_parser("morph", help="движение между двумя ключевыми кадрами")
    p.add_argument("first", type=Path)
    p.add_argument("second", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--sec", type=float, default=2)

    p = sub.add_parser("seq", help="последовательность поз -> анимация")
    p.add_argument("folder", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--fps", type=float, default=8)

    p = sub.add_parser("join", help="склейка планов в сцену")
    p.add_argument("clips", type=Path, nargs="+")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--fade", type=float, default=0.5)

    a = ap.parse_args()
    a.out.parent.mkdir(parents=True, exist_ok=True)

    if a.cmd == "ken":
        ken(a.image, a.out, a.sec, a.move)
    elif a.cmd == "morph":
        morph(a.first, a.second, a.out, a.sec)
    elif a.cmd == "seq":
        seq(a.folder, a.out, a.fps)
    else:
        join(a.clips, a.out, a.fade)


if __name__ == "__main__":
    main()
