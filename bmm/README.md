# BMM Cosmetology — сборка ролика

`build.py` собирает Reels-ролик из исходников целиком за один проход:
нарезка → реквизит → типографика → слоёная композиция → три варианта экспорта.

Исходные видео берутся из папки загрузок сессии и в репозиторий не попадают.

```bash
uv venv .venv && uv pip install --python .venv/bin/python numpy pillow
.venv/bin/python bmm/build.py
```

Результат: `bmm/out/BMM_master_1080.mp4`, `BMM_light_1080.mp4`, `BMM_720.mp4`.
