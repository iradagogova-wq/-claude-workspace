#!/usr/bin/env python3
"""Генерация кадров через бесплатный Gemini API прямо из чата.

Ключ берётся из переменной окружения GEMINI_API_KEY.
Получить бесплатно: aistudio.google.com -> Get API key.

Примеры:
    python3 scripts/gen_image.py --list-models
    python3 scripts/gen_image.py "prompt" --out references/characters/lisa.png
    python3 scripts/gen_image.py "prompt" --ref references/characters/lisa.png \
        --out references/S01E01/1.03.png --n 3
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "gemini-2.5-flash-image"


def api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        sys.exit(
            "Нет ключа. Получи бесплатный на aistudio.google.com -> Get API key,\n"
            "затем пропиши его в переменную окружения GEMINI_API_KEY."
        )
    return key


def call(path: str, payload: dict | None = None) -> dict:
    url = f"{API_ROOT}/{path}"
    headers = {"x-goog-api-key": api_key(), "Content-Type": "application/json"}
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        detail = body
        try:
            detail = json.loads(body)["error"]["message"]
        except (KeyError, ValueError):
            pass
        if exc.code == 429:
            sys.exit(f"Дневной бесплатный лимит исчерпан. Сброс в 03:00 МСК.\n{detail}")
        sys.exit(f"Ошибка API {exc.code}: {detail}")


def list_models() -> None:
    models = call("models").get("models", [])
    image_models = [
        m for m in models
        if "image" in m.get("name", "") or "imagen" in m.get("name", "").lower()
    ]
    print("Модели с генерацией картинок, доступные твоему ключу:\n")
    for m in image_models or models:
        name = m.get("name", "").removeprefix("models/")
        print(f"  {name:<40} {m.get('displayName', '')}")


def inline_ref(path: Path) -> dict:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return {
        "inline_data": {
            "mime_type": mime,
            "data": base64.b64encode(path.read_bytes()).decode(),
        }
    }


def generate(prompt: str, refs: list[Path], model: str, out: Path, n: int) -> None:
    parts: list[dict] = [inline_ref(p) for p in refs]
    parts.append({"text": prompt})
    payload = {"contents": [{"parts": parts}]}

    out.parent.mkdir(parents=True, exist_ok=True)
    saved = 0

    for i in range(1, n + 1):
        result = call(f"models/{model}:generateContent", payload)
        candidates = result.get("candidates") or []
        if not candidates:
            feedback = result.get("promptFeedback", {})
            sys.exit(f"Модель ничего не вернула. Возможно, промпт заблокирован: {feedback}")

        images = [
            p["inlineData"]["data"]
            for p in candidates[0].get("content", {}).get("parts", [])
            if "inlineData" in p
        ]
        if not images:
            texts = [
                p["text"] for p in candidates[0].get("content", {}).get("parts", [])
                if "text" in p
            ]
            sys.exit("Картинки в ответе нет. Модель ответила текстом: " + " ".join(texts)[:300])

        target = out if n == 1 else out.with_stem(f"{out.stem}_v{i}")
        target.write_bytes(base64.b64decode(images[0]))
        print(f"✓ {target}  ({target.stat().st_size // 1024} KB)")
        saved += 1

    if saved > 1:
        print(f"\nСгенерировано вариантов: {saved}. Выбери лучший, лишние удали.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Генерация кадров через бесплатный Gemini API")
    ap.add_argument("prompt", nargs="?", help="промпт кадра (по-английски)")
    ap.add_argument("--prompt-file", type=Path, help="взять промпт из файла")
    ap.add_argument("--ref", type=Path, action="append", default=[],
                    help="референс-картинка, можно несколько раз (лист персонажа)")
    ap.add_argument("--out", type=Path, default=Path("out.png"), help="куда сохранить")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"модель (по умолчанию {DEFAULT_MODEL})")
    ap.add_argument("--n", type=int, default=1, help="сколько вариантов сгенерировать")
    ap.add_argument("--list-models", action="store_true", help="показать доступные модели")
    args = ap.parse_args()

    if args.list_models:
        list_models()
        return

    prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else args.prompt
    if not prompt:
        ap.error("нужен промпт: аргументом или через --prompt-file")

    missing = [str(p) for p in args.ref if not p.is_file()]
    if missing:
        sys.exit("Референс не найден: " + ", ".join(missing))

    generate(prompt, args.ref, args.model, args.out, max(1, args.n))


if __name__ == "__main__":
    main()
