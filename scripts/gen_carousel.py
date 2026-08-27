#!/usr/bin/env python3
"""Бесшовная Instagram-карусель: одна широкая AI-сцена, разрезанная на слайды
с идеальным швом на стыке (тот же кадр — просто разрез, а не две генерации).

Ключ — тот же GEMINI_API_KEY, что и для scripts/gen_image.py.

Пример:
    python3 scripts/gen_carousel.py \
        "a woman in a flowing orange dress standing on ocean rocks at sunset, \
         golden hour, white roses in her hands, cinematic, ultra detailed" \
        --slides 2 --out references/carousels/roses
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "gemini-2.5-flash-image"

SLIDE_W, SLIDE_H = 1080, 1350  # Instagram feed, 4:5 — стандарт карусели

# Какое соотношение сторон просить у модели для N слайдов и до какого
# итогового соотношения обрезать перед разрезом. Обрезка всегда идёт
# по внешним краям (бока для широких, верх/низ для высоких) — сам будущий
# шов между слайдами (вертикальный разрез по центру) она не трогает,
# поэтому стык гарантированно идеальный при любом N.
PLAN = {
    2: {"request_ar": "16:9", "target_ratio": 2 * SLIDE_W / SLIDE_H},  # 1.60
    3: {"request_ar": "21:9", "target_ratio": 3 * SLIDE_W / SLIDE_H},  # 2.40
}


def api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        sys.exit(
            "Нет ключа. Получи бесплатный на aistudio.google.com -> Get API key,\n"
            "затем пропиши его в переменную окружения GEMINI_API_KEY."
        )
    return key


def call(payload: dict, model: str) -> dict:
    url = f"{API_ROOT}/models/{model}:generateContent"
    headers = {"x-goog-api-key": api_key(), "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
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
        return {"__error__": detail, "__code__": exc.code}


def generate_wide(prompt: str, aspect_ratio: str, model: str) -> Image.Image:
    full_prompt = (
        f"{prompt}\n\n"
        "Composition rules: this is ONE continuous wide panoramic shot, not a "
        "collage. Frame the scene so the subject/action flows across the full "
        "width, not centered in a narrow column. No text, no watermark, no "
        "borders, no split lines, no collage effect — a single seamless photo."
    )
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"imageConfig": {"aspectRatio": aspect_ratio}},
    }
    result = call(payload, model)
    if "__error__" in result:
        # модель/версия API могла не понять imageConfig -- пробуем без него
        payload["generationConfig"] = {}
        result = call(payload, model)
        if "__error__" in result:
            sys.exit(f"Ошибка API {result['__code__']}: {result['__error__']}")

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
            p["text"]
            for p in candidates[0].get("content", {}).get("parts", [])
            if "text" in p
        ]
        sys.exit("Картинки в ответе нет. Модель ответила текстом: " + " ".join(texts)[:300])

    return Image.open(BytesIO(base64.b64decode(images[0]))).convert("RGB")


def crop_to_ratio(img: Image.Image, ratio: float) -> Image.Image:
    """Обрезает только внешние края (бока или верх/них поровну) — шов между
    будущими слайдами (вертикальный разрез по центру) не трогает."""
    w, h = img.size
    current = w / h
    if current > ratio:
        new_w = round(h * ratio)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    if current < ratio:
        new_h = round(w / ratio)
        top = (h - new_h) // 2
        return img.crop((0, top, w, top + new_h))
    return img


def slice_slides(img: Image.Image, n: int, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    w, h = img.size
    step = w / n
    paths = []
    for i in range(n):
        left = round(i * step)
        right = round((i + 1) * step)
        piece = img.crop((left, 0, right, h)).resize(
            (SLIDE_W, SLIDE_H), Image.Resampling.LANCZOS
        )
        path = out_dir / f"{i + 1}.png"
        piece.save(path)
        paths.append(path)
    return paths


def main() -> None:
    ap = argparse.ArgumentParser(description="Генерация бесшовной карусели для Instagram")
    ap.add_argument("prompt", nargs="?", help="промпт сцены целиком (по-английски)")
    ap.add_argument("--prompt-file", type=Path, help="взять промпт из файла")
    ap.add_argument(
        "--slides", type=int, default=2, choices=[2, 3],
        help="сколько слайдов карусели (2 — надёжнее всего, как в вирусных примерах)",
    )
    ap.add_argument(
        "--out", type=Path, default=Path("references/carousels/post"),
        help="папка для готовых слайдов",
    )
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else args.prompt
    if not prompt:
        ap.error("нужен промпт: аргументом или через --prompt-file")

    plan = PLAN[args.slides]
    wide = generate_wide(prompt, plan["request_ar"], args.model)
    wide = crop_to_ratio(wide, plan["target_ratio"])
    paths = slice_slides(wide, args.slides, args.out)

    order = ", ".join(str(i + 1) for i in range(args.slides))
    print(f"✓ Готово: {len(paths)} слайдов в {args.out}/")
    for p in paths:
        print(f"  {p}  ({p.stat().st_size // 1024} KB)")
    print(f"\nЗагружай в Instagram каруселью строго по номерам {order} — порядок держит шов.")


if __name__ == "__main__":
    main()
