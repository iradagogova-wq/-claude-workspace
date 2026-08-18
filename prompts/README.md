# Библиотека промптов

Готовые блоки для копипаста. Всё по-английски — бесплатные модели сильнее на нём.

---

## 1. Лист персонажа (генерировать первым, до любых сцен)

```
character turnaround sheet, same character shown three times in one image:
front view, side profile view, and three-quarter view, standing in T-pose,
plain white background, even neutral studio lighting, full body visible,
3D animated feature film style, Pixar and Disney animation aesthetic,
stylized proportions, large expressive eyes, subsurface scattering on skin,
character reference sheet, model sheet, no text, no watermark,

<СЮДА LOCKED PROMPT BLOCK ПЕРСОНАЖА>
```

Крути, пока не понравится. Это лицо ты будешь видеть весь сериал.

---

## 2. Кадр-картинка

```
<STYLE BLOCK из style/STYLE.md>,

<LOCKED PROMPT BLOCK персонажа>,

<что делает: одно ясное действие>,
<где: локация с деталями>,
<план: wide establishing shot / medium shot / close-up portrait>,
<свет: golden hour / soft morning light / warm interior lamplight>
```

Обязательно подгрузи лист персонажа как reference image.

---

## 3. Оживление кадра (image-to-video)

Загружаешь утверждённую картинку, промптом описываешь **только движение**:

```
<одно движение камеры: slow push in>,
<что делает персонаж: she slowly turns her head and smiles>,
subtle natural motion, cinematic 3D animation, 5 seconds
```

Не переописывай внешность — она уже на картинке. Опишешь заново — модель начнёт
её «улучшать» и персонаж поплывёт.

---

## 4. Кадр с двумя персонажами

Самое сложное для бесплатных моделей. Приём: разведи их в пространстве явно.

```
<STYLE BLOCK>,
on the left: <LOCKED BLOCK персонажа A>,
on the right: <LOCKED BLOCK персонажа B>,
they are <что делают вместе>,
two characters, medium two-shot, <локация>, <свет>
```

Если лица всё равно ломаются — снимай через восьмёрку: кадр на одного, кадр на другого.
Так делают и в настоящей анимации.

---

## 5. Установочный кадр локации (без персонажей)

```
<STYLE BLOCK>,
<локация с деталями>, no people, wide establishing shot,
<время суток и свет>, sense of scale, atmospheric depth
```

Генерируй локации один раз и переиспользуй — это экономит лимиты и держит мир цельным.
