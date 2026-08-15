"""Editorial data for the reel: the cut, the type, the props, the timeline.

Subtitles carry the client's script verbatim. Long sentences are split across
two consecutive cards rather than rewritten, so nothing is paraphrased.

The two hug takes (v6 and v8) are the same moment shot twice — only v8 is
used, so the cut never repeats itself. Source tails carrying a CapCut
end-card are trimmed here: v8 goes black at 2.30 s, v5 at ~11.5 s,
v7 at ~3.60 s, and v9's subject turns away after ~4.7 s.

Total runtime lands at ~42.3 s.
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
SLOW_TAIL = ("seg13", "v9", 4.60, 0.45)   # name, source, seconds taken, speed

# ---- big words that sit BEHIND the video card ------------------------------
HEROES = [
    ("hero_roskosh", "РОСКОШЬ", 1.10),
    ("hero_filtr", "БЕЗ ФИЛЬТРА", 1.16),
    ("hero_tochka", "ТОЧЕЧНО", 1.12),
    ("hero_uhod", "УХОД", 1.08),
]

# ---- foreground phrases: (name, text, size hint, y, colour, width, lines) ---
# Wording is the client's, unchanged. Sentences too long for one card are
# split in two and shown back to back (marked _a / _b).
PHRASES = [
    ("ph_hook",   "Знаете, что сегодня стало настоящей роскошью для женщины?",
     78, .745, "W", .90, 3),

    ("ph_not1",   "Не сумка.",                       88, .400, "W", .86, 1),
    ("ph_not2",   "Не украшения.",                   88, .480, "W", .86, 1),
    ("ph_not3",   "И даже не количество процедур.",  76, .570, "M", .90, 2),

    ("ph_zabota", "А выглядеть так, будто вы действительно о себе заботитесь.",
     74, .755, "W", .90, 3),

    ("ph_filtr",  "Когда нравится кожа без фильтра.", 78, .760, "W", .90, 2),
    ("ph_zerk",   "Когда утром смотришь в зеркало — и нравишься себе.",
     72, .760, "W", .90, 3),
    ("ph_vol_a",  "Когда можешь собрать волосы, не наносить плотный тон",
     70, .760, "W", .90, 3),
    ("ph_vol_b",  "и всё равно чувствовать себя красивой.", 74, .760, "W", .90, 2),

    ("ph_pochemu", "И именно поэтому я так люблю современную косметологию.",
     72, .760, "W", .90, 3),

    ("ph_nebolshe", "Не за возможность сделать больше.", 80, .755, "W", .90, 2),
    ("ph_toch_a",   "А за возможность точечно дать женщине именно то,",
     70, .760, "W", .90, 3),
    ("ph_toch_b",   "что сделает её ещё более ухоженной.", 76, .760, "M", .90, 2),

    ("ph_gde1", "Где-то поработать с качеством кожи.", 66, .400, "W", .88, 2),
    ("ph_gde2", "Где-то смягчить активную мимику.",    66, .490, "W", .88, 2),
    ("ph_gde3", "Где-то подчеркнуть черты.",           66, .580, "W", .88, 2),

    ("ph_nravlus", "«Мне нравится, как я выгляжу».", 78, .755, "W", .92, 2),
    ("ph_final",   "Вот для меня и есть настоящий уход за собой.",
     80, .775, "W", .90, 2),
    ("ph_cta",     "подписывайтесь",                 58, .880, "W", .70, 1),

    ("kicker",     "эстетика лица",                  40, .115, "G", .60, 1),
]

# ---- timeline: (start, end, key, layer) ------------------------------------
CUES = [
    (0.10,  4.50, "kicker",       "front"),
    (0.10,  4.50, "hero_roskosh", "behind"),
    (0.40,  4.50, "ph_hook",      "front"),

    # three lines stack up and hold together
    (5.10,  9.40, "ph_not1", "front"),
    (6.30,  9.40, "ph_not2", "front"),
    (7.50,  9.40, "ph_not3", "front"),

    (9.90, 13.40, "ph_zabota", "front"),

    (13.90, 16.20, "hero_filtr", "behind"),
    (14.00, 16.20, "ph_filtr",   "front"),
    (16.60, 19.40, "ph_zerk",    "front"),
    (19.80, 22.00, "ph_vol_a",   "front"),
    (22.00, 24.20, "ph_vol_b",   "front"),

    (24.70, 27.40, "ph_pochemu", "front"),

    (27.80, 29.70, "hero_tochka",  "behind"),
    (27.90, 29.70, "ph_nebolshe",  "front"),
    (30.10, 32.30, "ph_toch_a",    "front"),
    (32.30, 34.40, "ph_toch_b",    "front"),

    (34.80, 38.60, "ph_gde1", "front"),
    (36.00, 38.60, "ph_gde2", "front"),
    (37.20, 38.60, "ph_gde3", "front"),

    (39.00, 40.60, "ph_nravlus", "front"),

    (40.80, 42.20, "hero_uhod", "behind"),
    (40.80, 42.20, "ph_final",  "front"),
    (41.20, 42.20, "ph_cta",    "front"),
]

# ---- card / full-bleed choreography: (t, scale, angle, cx, cy) -------------
KEYS = [
    (0.00, .60, -4.0, .50, .46), (4.20, .60, -4.0, .50, .46),
    (5.00, 1.0,  0.0, .50, .50), (9.60, 1.0,  0.0, .50, .50),
    (10.20, .62, 3.5, .48, .47), (13.20, .62, 3.5, .48, .47),
    (13.80, 1.0, 0.0, .50, .50), (19.60, 1.0, 0.0, .50, .50),
    (20.20, .60, -3.5, .50, .47), (23.80, .60, -3.5, .50, .47),
    (24.40, 1.0, 0.0, .50, .50), (34.40, 1.0, 0.0, .50, .50),
    (35.00, .60, 3.0, .50, .47), (38.20, .60, 3.0, .50, .47),
    (38.80, 1.0, 0.0, .50, .50), (42.50, 1.0, 0.0, .50, .50),
]

# ---- props: (start, end, name, x, y, scale, angle, drift x, drift y) -------
PROPS = [
    (5.20,  9.30, "luxury_x", .81, .74, .52,  9, -20, 16),
    (14.10, 16.10, "mirror",  .82, .30, .56, -10, 20, 16),
    (30.20, 34.30, "ampoule", .85, .30, .60, -10, 20, 16),
]
