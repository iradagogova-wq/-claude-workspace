"""Editorial data for the reel: the cut, the type, the props, the timeline.

Design decisions behind this pass:

* The footage stays full-bleed for almost the whole runtime. Shrinking 1080p
  into a 60 %-wide card looked designed but softened the picture, so the
  design now lives in the typography and props instead of in the frame size.
* Subtitles quote the client's script. Dense enumerations are set as stacked
  lines — the client's own words, one per line — rather than as paragraphs,
  so nothing is reworded and everything still fits.
* v6 and v8 are the same hug filmed twice; only v8 is used, so no shot repeats.

Trimmed source tails carrying a CapCut end-card: v8 at 2.30 s, v5 at ~11.5 s,
v7 at ~3.60 s; v9's subject turns away after ~4.7 s.

Total runtime lands at ~41.3 s.
"""

# ---- the cut: (name, source, in, out) --------------------------------------
EDL = [
    ("seg01", "v1", 0.00, 4.60),
    ("seg02", "v3", 0.00, 2.00),
    ("seg03", "v4", 0.00, 3.00),
    ("seg04", "v5", 0.00, 5.60),
    ("seg05", "v2", 0.00, 3.15),
    ("seg06", "v3", 2.00, 4.20),
    ("seg07", "v5", 5.60, 8.80),
    ("seg08", "v7", 0.00, 1.90),
    ("seg09", "v5", 8.80, 11.45),
    ("seg10", "v4", 3.00, 5.70),
    ("seg11", "v7", 1.90, 3.55),
    ("seg12", "v8", 0.00, 2.10),
]
SLOW_TAIL = ("seg13", "v9", 4.60, 0.50)   # name, source, seconds taken, speed

# ---- big words that sit BEHIND the type ------------------------------------
HEROES = [
    ("hero_koja", "КОЖА", 1.06),
    ("hero_mimika", "МИМИКА", 1.10),
    ("hero_proporcii", "ПРОПОРЦИИ", 1.16),
    ("hero_uhod", "УХОД", 1.08),
]

# ---- foreground phrases: (name, text, size hint, y, colour, width, lines) ---
PHRASES = [
    ("ph_hook", "Три вещи, которые я бы поставила на первое место, "
                "если хочется всегда выглядеть ухоженно", 68, .745, "W", .90, 4),

    ("n1",       "Первое",        64, .300, "M", .60, 1),
    ("ph_koja",  "Качество кожи", 96, .390, "W", .88, 1),
    ("k1", "ровная текстура",           62, .530, "W", .84, 1),
    ("k2", "достаточная увлажнённость", 62, .605, "W", .84, 1),
    ("k3", "здоровый кожный барьер",    62, .680, "W", .84, 1),
    ("k4", "работа с пигментацией",     62, .755, "W", .84, 1),
    ("ph_dom", "Начинается с грамотно подобранного домашнего ухода "
               "и ежедневной фотозащиты", 66, .755, "W", .90, 3),
    ("ph_pokaz1", "Процедуры подключаются уже по показаниям", 72, .760, "M", .90, 2),

    ("n2",       "Второе", 64, .300, "M", .60, 1),
    ("ph_vyraj", "Работать с тем, что действительно меняет выражение лица",
     70, .400, "W", .88, 3),
    ("ph_botox", "При выраженной активности мимических мышц ботулинотерапия "
                 "может смягчить мимические линии", 62, .750, "W", .90, 4),
    ("ph_pokaz2", "Важна не сама процедура — важны показания к ней",
     72, .755, "W", .90, 2),

    ("n3",       "Третье", 64, .300, "M", .60, 1),
    ("ph_garm",  "Сохранять гармонию пропорций", 80, .400, "W", .88, 2),
    ("ph_zony",  "Губы, подбородок, профиль — важно смотреть, как зона "
                 "взаимодействует с остальными чертами лица", 60, .750, "W", .90, 4),
    ("ph_mm",    "Несколько миллиметров в правильном месте иногда дают больше, "
                 "чем большой объём", 64, .750, "W", .90, 4),

    ("s1", "качество кожи",         66, .330, "W", .84, 1),
    ("s2", "работа по показаниям",  66, .405, "W", .84, 1),
    ("s3", "гармоничные пропорции", 66, .480, "W", .84, 1),
    ("ph_gody", "Результат, который можно поддерживать годами",
     70, .600, "M", .90, 2),
    ("ph_cta",  "Сохраняйте эти три пункта", 62, .875, "W", .80, 1),

    ("kicker",  "эстетика лица", 40, .115, "G", .60, 1),
]

# ---- timeline: (start, end, key, layer) ------------------------------------
CUES = [
    (0.10,  4.40, "kicker",  "front"),
    (0.35,  4.40, "ph_hook", "front"),

    (5.00,  9.60, "hero_koja", "behind"),
    (5.00,  9.60, "n1",        "front"),
    (5.20,  9.60, "ph_koja",   "front"),
    (6.20,  9.60, "k1", "front"),
    (6.90,  9.60, "k2", "front"),
    (7.60,  9.60, "k3", "front"),
    (8.30,  9.60, "k4", "front"),

    (10.10, 13.60, "ph_dom",    "front"),
    (14.00, 16.40, "ph_pokaz1", "front"),

    (17.00, 20.40, "hero_mimika", "behind"),
    (17.00, 20.40, "n2",          "front"),
    (17.20, 20.40, "ph_vyraj",    "front"),
    (20.90, 24.40, "ph_botox",    "front"),
    (24.80, 27.30, "ph_pokaz2",   "front"),

    (27.90, 30.90, "hero_proporcii", "behind"),
    (27.90, 30.90, "n3",             "front"),
    (28.10, 30.90, "ph_garm",        "front"),
    (31.30, 34.30, "ph_zony",        "front"),
    (34.70, 37.60, "ph_mm",          "front"),

    (38.10, 41.10, "hero_uhod", "behind"),
    (38.10, 41.10, "s1", "front"),
    (38.60, 41.10, "s2", "front"),
    (39.10, 41.10, "s3", "front"),
    (39.70, 41.10, "ph_gody", "front"),
    (40.20, 41.10, "ph_cta",  "front"),
]

# ---- frame choreography: mostly full-bleed so the footage keeps its detail --
KEYS = [
    (0.00, 1.0, 0.0, .50, .50), (16.60, 1.0, 0.0, .50, .50),
    (17.20, .70, 3.0, .50, .48), (20.20, .70, 3.0, .50, .48),
    (20.80, 1.0, 0.0, .50, .50), (41.50, 1.0, 0.0, .50, .50),
]

# ---- props: (start, end, name, x, y, scale, angle, drift x, drift y) -------
PROPS = [
    (6.30,  9.50, "bottle",  .84, .30, .52, 10, -18, 14),
    (21.00, 24.30, "ampoule", .85, .30, .56, -9, 18, 14),
    (31.40, 34.20, "mirror",  .84, .30, .50, 10, -18, 14),
]
