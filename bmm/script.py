"""Editorial data for the reel: the cut, the type, the props, the timeline.

Kept apart from build.py so the script can be rewritten without touching
the rendering engine. Total runtime lands at ~40.4 s.

Source tails carrying a CapCut end-card are trimmed here:
v8 goes black at 2.30 s, v5 at ~11.5 s, v7 at ~3.60 s.
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
    ("seg13", "v6", 0.00, 1.10),
]
SLOW_TAIL = ("seg14", "v9", 4.60, 0.62)   # name, source, seconds taken, speed

# ---- big words that sit BEHIND the video card ------------------------------
HEROES = [
    ("hero_roskosh", "РОСКОШЬ", 1.10),
    ("hero_filtr", "БЕЗ ФИЛЬТРА", 1.16),
    ("hero_tochka", "ТОЧЕЧНО", 1.12),
    ("hero_uhod", "УХОД", 1.08),
]

# ---- foreground phrases: (name, text, size hint, y, colour, width, lines) ---
PHRASES = [
    ("ph_hook1",    "что сегодня стало",        84, .720, "W", .88, 1),
    ("ph_hook2",    "настоящей роскошью?",      92, .800, "M", .90, 1),
    ("ph_zabota",   "выглядеть так, будто вы о себе заботитесь", 74, .755, "W", .90, 3),
    ("ph_filtr",    "когда нравится кожа без фильтра", 76, .760, "W", .90, 2),
    ("ph_zerkalo",  "утром смотришь в зеркало — и нравишься себе", 70, .760, "W", .90, 3),
    ("ph_volosy",   "не прятаться за плотным тоном", 74, .760, "W", .90, 2),
    ("ph_nebolshe", "не сделать больше",        92, .755, "W", .90, 1),
    ("ph_tochno",   "а дать именно то, что нужно вам", 74, .760, "W", .90, 2),
    ("ph_nravlus",  "«мне нравится, как я выгляжу»", 76, .755, "W", .92, 2),
    ("ph_final",    "настоящий уход за собой",  86, .780, "W", .88, 2),
    ("ph_cta",      "подписывайтесь",           64, .872, "W", .70, 1),
    ("kicker",      "эстетика лица",            40, .115, "G", .60, 1),
]

# ---- stacked rows: (name, marker, word, index within its group) ------------
ROWS_NOT = [
    ("r_bag",  "✕", "сумка",              0),
    ("r_ring", "✕", "украшения",          1),
    ("r_proc", "✕", "количество процедур", 2),
]
ROWS_WHERE = [
    ("r_skin", "01", "качество кожи",   0),
    ("r_mim",  "02", "активная мимика", 1),
    ("r_cher", "03", "черты лица",      2),
]

# ---- timeline: (start, end, key, layer) ------------------------------------
CUES = [
    (0.10,  4.55, "kicker",       "front"),
    (0.10,  4.55, "hero_roskosh", "behind"),
    (0.40,  4.55, "ph_hook1",     "front"),
    (0.90,  4.55, "ph_hook2",     "front"),

    (6.30,  9.20, "r_bag",  "front"),
    (6.80,  9.20, "r_ring", "front"),
    (7.30,  9.20, "r_proc", "front"),

    (9.80, 14.00, "ph_zabota", "front"),

    (14.60, 17.60, "hero_filtr", "behind"),
    (14.80, 17.60, "ph_filtr",   "front"),
    (18.00, 20.80, "ph_zerkalo", "front"),
    (21.20, 24.20, "ph_volosy",  "front"),

    (24.80, 27.40, "hero_tochka",  "behind"),
    (25.00, 27.40, "ph_nebolshe",  "front"),
    (27.80, 30.60, "ph_tochno",    "front"),

    (31.10, 34.40, "r_skin", "front"),
    (31.60, 34.40, "r_mim",  "front"),
    (32.10, 34.40, "r_cher", "front"),

    (34.90, 37.40, "ph_nravlus", "front"),

    (37.80, 40.20, "hero_uhod", "behind"),
    (38.00, 40.20, "ph_final",  "front"),
    (38.90, 40.20, "ph_cta",    "front"),
]

# ---- card / full-bleed choreography: (t, scale, angle, cx, cy) -------------
KEYS = [
    (0.00, .60, -4.0, .50, .46), (4.20, .60, -4.0, .50, .46),
    (5.00, 1.0,  0.0, .50, .50), (9.90, 1.0,  0.0, .50, .50),
    (10.50, .62, 3.5, .48, .47), (13.70, .62, 3.5, .48, .47),
    (14.30, 1.0, 0.0, .50, .50), (21.00, 1.0, 0.0, .50, .50),
    (21.70, .60, -3.5, .50, .47), (23.90, .60, -3.5, .50, .47),
    (24.60, 1.0, 0.0, .50, .50), (34.80, 1.0, 0.0, .50, .50),
    (35.30, .60, 3.0, .50, .47), (37.10, .60, 3.0, .50, .47),
    (37.70, 1.0, 0.0, .50, .50), (41.00, 1.0, 0.0, .50, .50),
]

# ---- props: (start, end, name, x, y, scale, angle, drift x, drift y) -------
PROPS = [
    (6.40,  9.10, "luxury_x", .80, .68, .56,  9, -22, 18),
    (14.90, 17.50, "mirror",  .82, .30, .58, -10, 22, 18),
    (25.10, 27.30, "ampoule", .84, .31, .64, -10, 22, 18),
]
