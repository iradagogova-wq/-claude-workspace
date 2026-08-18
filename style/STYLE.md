# Визуальный стандарт студии

Один и тот же стиль во всех сериях. Этот блок вставляется в **каждый** промпт кадра.

---

## STYLE BLOCK (копировать дословно в начало каждого промпта картинки)

```
3D animated feature film style, Pixar and Disney animation aesthetic,
stylized character proportions with large expressive eyes and soft rounded forms,
subsurface scattering on skin, soft global illumination, warm cinematic key light
with cool bounce fill, shallow depth of field, physically based rendering,
rich saturated color palette, volumetric light rays, high detail, 8k render,
family friendly, no text, no watermark
```

## NEGATIVE BLOCK (куда сервис просит «negative prompt»)

```
photorealistic, live action, anime, manga, 2d flat illustration, sketch, ugly,
deformed face, extra fingers, extra limbs, mutated hands, blurry, low quality,
jpeg artifacts, text, watermark, signature, logo, dark gloomy, horror, gore
```

---

## Правила кадра

**Планы.** Чередуй: общий (где мы) → средний (кто говорит) → крупный (что чувствует).
Три одинаковых плана подряд — зритель засыпает.

**Камера.** В промпте видео всегда указывай ОДНО движение, не два.
Хорошо: `slow dolly in`. Плохо: `dolly in while panning right and tilting up`.
Бесплатные модели ломаются на сложных движениях.

Рабочий набор: `slow push in` · `slow pull out` · `gentle pan left/right` ·
`low angle hero shot` · `overhead establishing shot` · `static shot, character moves`

**Свет.** Тёплый ключевой + холодная заливка — базовая формула диснеевского объёма.
Время суток задавай явно: `golden hour`, `soft morning light`, `warm interior lamplight`.

**Цвет.** У каждой серии — своя доминанта. Записывай её в файл серии, иначе к третьему
эпизоду сериал расползётся по палитре.

---

## Как звучит хороший промпт кадра

Порядок частей строго такой — модели читают начало внимательнее конца:

```
[STYLE BLOCK] + [LOCKED CHARACTER BLOCK] + [что делает] +
[где находится] + [план и камера] + [свет и время суток]
```
