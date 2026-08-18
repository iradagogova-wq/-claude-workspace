# Кадры для слайдов 5 и 6 карусели EL VITA

Те же мама и дочка, что на слайдах 1–4. Внешность берётся дословно из
`characters/mama.md` и `characters/dochka.md` — Locked prompt block, ни одной запятой
менять нельзя, иначе в кадре будут другие люди.

**Главное отличие от обычного кадра сериала:** поверх картинки ляжет текст.
Поэтому в промпте явно требуется пустое тёмное место слева — иначе заголовок
придётся класть на лицо.

Формат: вертикаль 3:4 (1080×1440). Комната, палитра и лампа — те же, что в слайдах 1–4.

---

## SHOT 5 · image

```
3D animated feature film style, Pixar and Disney animation aesthetic,
stylized character proportions with large expressive eyes and soft rounded forms,
subsurface scattering on skin, soft global illumination, warm cinematic key light
with cool bounce fill, shallow depth of field, physically based rendering,
rich saturated color palette, volumetric light rays, high detail, 8k render,
family friendly, no text, no watermark,

a 30-year-old young mother, soft heart-shaped face with rosy cheeks, warm fair skin,
dark chestnut-brown hair gathered in a loose messy high bun with soft wispy strands
falling around her temples, very large expressive dark brown eyes with long lashes,
thick softly arched dark eyebrows, small nose and gentle full lips, slim build,
wearing a dusty mauve-plum ribbed knit crewneck sweater with long sleeves,
gentle worried tender expression,

standing in front of a home shelf crowded with many supplement bottles, holding one
large amber vitamin jar up in her right hand and studying its label with quiet doubt,
a second jar still on the shelf under her left hand, her 5-year-old daughter standing
close beside her hip and looking up at her face,

a 5-year-old girl, round face with full soft cheeks and a warm pink flush on cheeks
and nose, long wavy auburn-chestnut hair loose over her shoulders with a soft side
part, very large expressive blue-grey eyes with long lashes, small button nose,
small delicate build, wearing a soft dusty-pink knitted sweater,
tired sad gentle expression, always holding a light-brown plush teddy bear,

evening home interior, dark navy and plum walls, wooden shelf packed with amber and
cream supplement bottles, bookshelf blurred in the background,
vertical 3:4 composition, mother and daughter placed in the RIGHT half of the frame,
the entire LEFT 45 percent of the frame is empty dark uncluttered wall in deep shadow
with nothing happening in it, faces well below the top edge,
medium shot, eye level, warm interior lamplight from the right side of the frame
casting an orange rim light on hair and shoulders, cool blue ambient fill from the left
```

**Negative prompt**

```
photorealistic, live action, anime, manga, 2d flat illustration, sketch, ugly,
deformed face, extra fingers, extra limbs, mutated hands, blurry, low quality,
jpeg artifacts, text, watermark, signature, logo, dark gloomy, horror, gore,
busy background on the left, character centered, character on the left
```

---

## SHOT 6 · image

```
3D animated feature film style, Pixar and Disney animation aesthetic,
stylized character proportions with large expressive eyes and soft rounded forms,
subsurface scattering on skin, soft global illumination, warm cinematic key light
with cool bounce fill, shallow depth of field, physically based rendering,
rich saturated color palette, volumetric light rays, high detail, 8k render,
family friendly, no text, no watermark,

a 30-year-old young mother, soft heart-shaped face with rosy cheeks, warm fair skin,
dark chestnut-brown hair gathered in a loose messy high bun with soft wispy strands
falling around her temples, very large expressive dark brown eyes with long lashes,
thick softly arched dark eyebrows, small nose and gentle full lips, slim build,
wearing a dusty mauve-plum ribbed knit crewneck sweater with long sleeves,
calm relieved warm expression, a small quiet smile,

sitting at a wooden table typing a short message on her phone, shoulders relaxed
for the first time, her 5-year-old daughter leaning sleepily against her arm,

a 5-year-old girl, round face with full soft cheeks and a warm pink flush on cheeks
and nose, long wavy auburn-chestnut hair loose over her shoulders with a soft side
part, very large expressive blue-grey eyes with long lashes, small button nose,
small delicate build, wearing a soft dusty-pink knitted sweater,
calm sleepy gentle expression, always holding a light-brown plush teddy bear,

evening home interior, dark navy and plum walls, warm table lamp glowing on the right,
three amber supplement jars and a mug standing on the table in the lower right corner,
vertical 3:4 composition, mother and daughter placed in the RIGHT half of the frame
and in the LOWER two thirds, the entire LEFT 45 percent and the TOP third of the frame
are empty dark uncluttered space in deep shadow,
medium shot, eye level, warm interior lamplight from the right casting an orange rim
light on hair and shoulders, cool blue ambient fill from the left
```

**Negative prompt** — тот же, что у SHOT 5.

---

## Как снимать

1. Сначала SHOT 5 → выбрать удачный вариант → сохранить в `references/carousel/05.png`.
2. SHOT 6 генерировать **с подгруженным `05.png` как reference image** — так лица
   и свитера гарантированно совпадут между слайдами.
3. Готовые кадры кладутся в `slides/src/frames/`, дальше:

```bash
cd slides/src && node render.mjs        # текст ляжет поверх кадров
```

Команда генерации (нужен `GEMINI_API_KEY`):

```bash
uv run scripts/gen_image.py --prompt-file prompts/shot5.txt \
  --out references/carousel/05.png --n 3
```
