"""BMM reel — single-process build.

Lives inside the git repo directory because the environment's cleaner wipes
other paths mid-render. Produces the master plus lighter delivery encodes.
"""
import os, json, glob, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

UP = "/root/.claude/uploads/a0442629-227e-5e51-b202-6b3758f6cdfc"
WORK = "/home/user/-claude-workspace/.bmm_work"
SRC, EDIT = f"{WORK}/src", f"{WORK}/edit"
SEG, TYPE, PR = f"{EDIT}/segments", f"{EDIT}/type", f"{EDIT}/props"
for d in (SRC, SEG, TYPE, PR):
    os.makedirs(d, exist_ok=True)

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MAG, WHT, GREY = (225, 11, 110, 255), (255, 255, 255, 255), (170, 170, 176, 255)

FILES = {
    "v1": "6c6b07ee-copy_0C770866991B4B35A9DA0C46BB9F8850.mov",
    "v2": "c1158e6d-copy_AAE4089CF1604D9DAB3A04F91DF6C442.mov",
    "v3": "60c5d7b3-copy_64CC84E416074AD8AD298B4EFDE695A7.mov",
    "v4": "4aed7b67-copy_D1B5AB7E55F444CCB1B12F2CDCD62E37.mov",
    "v5": "9c3371bd-copy_BA40E7175FA34D3C9221B35732F7415A.mov",
    "v6": "80a5b586-copy_9522907B35F844D982999EEA56EEC7F8.mov",
    "v7": "c565b5c5-copy_0B88AFFA588C4494988F9475A699B882.mov",
    "v9": "802755de-copy_B6874F3132CB4F7480811E61DB680BF4.mov",
}
for k, v in FILES.items():
    if not os.path.exists(f"{SRC}/{k}.mov"):
        subprocess.run(["cp", f"{UP}/{v}", f"{SRC}/{k}.mov"], check=True)

EDL = [("seg01", "v1", 0, 4.20), ("seg02", "v3", 0, 1.55), ("seg03", "v4", 0, 2.60),
       ("seg04", "v5", 0, 5.40), ("seg05", "v2", 0, 3.10), ("seg06", "v3", 1.55, 3.10),
       ("seg07", "v5", 5.40, 8.50), ("seg08", "v7", 0, 1.90), ("seg09", "v5", 8.50, 10.80),
       ("seg10", "v4", 2.60, 5.70), ("seg11", "v7", 1.90, 3.55), ("seg12", "v6", 0, 1.10)]
for n, s, i, o in EDL:
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-ss", str(i), "-i", f"{SRC}/{s}.mov",
                    "-t", str(o - i), "-vf", "scale=1080:1920:flags=lanczos,fps=30", "-an",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "10", "-pix_fmt", "yuv420p",
                    f"{SEG}/{n}.mp4", "-loglevel", "error"], check=True)
subprocess.run(["ffmpeg", "-nostdin", "-y", "-t", "4.50", "-i", f"{SRC}/v9.mov",
                "-vf", "scale=1080:1920:flags=lanczos,fps=30,setpts=PTS/0.7", "-an",
                "-c:v", "libx264", "-preset", "slow", "-crf", "10", "-pix_fmt", "yuv420p",
                f"{SEG}/seg13.mp4", "-loglevel", "error"], check=True)

names = [e[0] for e in EDL] + ["seg13"]


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
    return float(r.stdout.strip())


durs = [dur(f"{SEG}/{n}.mp4") for n in names]
TX, inputs, filt = 0.22, [], []
for n in names:
    inputs += ["-i", f"{SEG}/{n}.mp4"]
cum, prev = durs[0], "0:v"
for i in range(1, len(names)):
    lbl = f"x{i}" if i < len(names) - 1 else "vout"
    filt.append(f"[{prev}][{i}:v]xfade=transition=circleopen:duration={TX}:offset={cum-TX:.3f}[{lbl}]")
    cum += durs[i] - TX
    prev = lbl
subprocess.run(["ffmpeg", "-nostdin", "-y"] + inputs + ["-filter_complex", ";".join(filt),
                "-map", "[vout]", "-c:v", "libx264", "-preset", "slow", "-crf", "10",
                "-pix_fmt", "yuv420p", f"{EDIT}/base.mp4", "-loglevel", "error"], check=True)
DUR = cum
print("BASE_DONE", round(DUR, 3), flush=True)


def shadowed(card, blur=24, off=(0, 14), op=155):
    pad = blur * 3
    out = Image.new("RGBA", (card.width + pad * 2, card.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    a = card.split()[3]
    tint = Image.new("RGBA", card.size, (0, 0, 0, op))
    tint.putalpha(a.point(lambda p: int(p * op / 255)))
    sh.paste(tint, (pad + off[0], pad + off[1]), tint)
    out = Image.alpha_composite(out, sh.filter(ImageFilter.GaussianBlur(blur)))
    out.paste(card, (pad, pad), card)
    return out


def list_note(crossed):
    Wc, Hc = 460, 600
    c = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, Wc - 1, Hc - 1], 12, fill=(240, 238, 234, 255))
    d.text((44, 52), "ХОЧУ:", font=ImageFont.truetype(F, 30), fill=(30, 30, 34, 255))
    fr = ImageFont.truetype(FR, 27)
    for i, w in enumerate(["Ботокс", "Биоревитализация", "Губы", "Подбородок"]):
        y = 130 + i * 76
        d.rounded_rectangle([46, y, 76, y + 30], 5, outline=(120, 120, 126, 255), width=3)
        d.text((100, y - 2), w, font=fr, fill=(52, 52, 58, 255))
    if crossed:
        d.line([(34, 108), (Wc - 34, Hc - 92)], fill=MAG, width=13)
        d.line([(Wc - 34, 108), (34, Hc - 92)], fill=MAG, width=13)
    return c


shadowed(list_note(False)).save(f"{PR}/list_note.png")
shadowed(list_note(True)).save(f"{PR}/list_note_x.png")
c = Image.new("RGBA", (170, 430), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
d.polygon([(72, 18), (98, 18), (104, 96), (66, 96)], fill=(214, 224, 220, 235))
d.rounded_rectangle([56, 96, 114, 350], 16, fill=(226, 234, 230, 240))
d.rounded_rectangle([56, 210, 114, 350], 16, fill=(246, 232, 238, 245))
d.line([(70, 262), (100, 262)], fill=MAG, width=5)
d.rounded_rectangle([60, 350, 110, 392], 10, fill=(198, 206, 202, 240))
shadowed(c, 18, (0, 10)).save(f"{PR}/ampoule.png")
c = Image.new("RGBA", (240, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
d.rounded_rectangle([50, 90, 190, 400], 30, fill=(236, 234, 230, 240))
d.rounded_rectangle([92, 26, 148, 96], 12, fill=(210, 208, 204, 255))
d.rounded_rectangle([70, 190, 170, 300], 10, fill=(255, 255, 255, 235))
d.line([(88, 232), (152, 232)], fill=MAG, width=6)
d.line([(88, 258), (130, 258)], fill=(150, 150, 155, 255), width=4)
shadowed(c, 20, (0, 12)).save(f"{PR}/bottle.png")
print("PROPS_DONE", flush=True)

anchors = {}


def fit(text, max_w, start, max_lines):
    d = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    s = start
    while s > 24:
        f = ImageFont.truetype(F, s)
        lines, cur = [], ""
        for w in text.split():
            tr = (cur + " " + w).strip()
            if d.textbbox((0, 0), tr, font=f)[2] <= max_w or not cur:
                cur = tr
            else:
                lines.append(cur); cur = w
        if cur:
            lines.append(cur)
        if len(lines) <= max_lines and max(d.textbbox((0, 0), l, font=f)[2] for l in lines) <= max_w:
            return f, lines, s
        s -= 4
    return f, lines, s


def save(name, img, keep_full=False):
    if keep_full:
        img.save(f"{TYPE}/{name}.png"); anchors[name] = [0, 0, 1]; return
    bb = img.getbbox() or (0, 0, W, H)
    img.crop(bb).save(f"{TYPE}/{name}.png")
    anchors[name] = [bb[0], bb[1], 0]


def render(name, text, hint, cy, color=WHT, mw=.92, ml=1,
           shadow=True, blur=9, op=165, keep_full=False):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f, lines, s = fit(text.upper(), int(W * mw), hint, ml)
    mets = [d.textbbox((0, 0), l, font=f) for l in lines]
    hs = [m[3] - m[1] for m in mets]
    gap = int(s * .20)
    y = int(H * cy) - (sum(hs) + gap * (len(lines) - 1)) // 2
    for l, m, hh in zip(lines, mets, hs):
        x = (W - (m[2] - m[0])) // 2 - m[0]
        if shadow:
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(sh).text((x, y - m[1]), l, font=f, fill=(0, 0, 0, op))
            img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(blur)))
            d = ImageDraw.Draw(img)
        d.text((x, y - m[1]), l, font=f, fill=color)
        y += hh + gap
    save(name, img, keep_full)


for n, t, mwf in [("hero_spisok", "ХОЧУ", 1.02), ("hero_cheklist", "ЧЕК-ЛИСТ", 1.14),
                  ("hero_moda", "МОДА", 1.10), ("hero_ponimanie", "ПОНИМАНИЕ", 1.16),
                  ("hero_uhod", "УХОД", 1.08)]:
    render(n, t, 300, .21, WHT, mwf, shadow=False, keep_full=True)

render("front_spisok", "список", 132, .745, WHT, .90, blur=10, op=150)
render("front_procedur", "процедур", 132, .818, MAG, .90, blur=10, op=150)
render("ph_zapretila", "что я бы запретила", 86, .76)
render("ph_nechek", "это не чек-лист", 98, .75)
render("ph_podruga", "не то, что делает подруга", 78, .76)
render("ph_vozrast", "«уже пора по возрасту»", 82, .75)
render("ph_nichego", "иногда — ничего не добавлять", 72, .77, ml=2)
render("ph_final", "настоящий уход за собой", 86, .795, ml=2, blur=16, op=220)
render("kicker", "эстетика лица", 40, .115, GREY, .6)

rows = [("li_botoks", "01", "Ботокс"), ("li_bio", "02", "Биоревитализация"),
        ("li_guby", "03", "Губы"), ("li_podb", "04", "Подбородок")]
B, G, S = 84, 34, 62
for i, (name, num, word) in enumerate(rows):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f, fb = ImageFont.truetype(F, S), ImageFont.truetype(F, 34)
    txt = word.upper()
    b = d.textbbox((0, 0), txt, font=f)
    tw, th = b[2] - b[0], b[3] - b[1]
    block = B + G + tw
    x0 = (W - block) // 2
    cy = int(H * (.335 + i * .088))
    pl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle(
        [x0 - 40, cy - B // 2 - 18, x0 + block + 40, cy + B // 2 + 18], 44, fill=(10, 10, 12, 165))
    img = Image.alpha_composite(img, pl.filter(ImageFilter.GaussianBlur(3)))
    d = ImageDraw.Draw(img)
    d.ellipse([x0, cy - B // 2, x0 + B, cy + B // 2], fill=(14, 14, 16, 255), outline=MAG, width=3)
    nb = d.textbbox((0, 0), num, font=fb)
    d.text((x0 + (B - (nb[2] - nb[0])) // 2 - nb[0], cy - (nb[3] - nb[1]) // 2 - nb[1]),
           num, font=fb, fill=WHT)
    d.text((x0 + B + G - b[0], cy - th // 2 - b[1]), txt, font=f, fill=MAG)
    save(name, img)

img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
f = ImageFont.truetype(F, 44); t = "@BMM___COSMETOLOG"
b = d.textbbox((0, 0), t, font=f)
x, y = (W - (b[2] - b[0])) // 2 - b[0], int(H * .925) - b[1]
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).text((x, y), t, font=f, fill=(0, 0, 0, 190))
img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(6)))
d = ImageDraw.Draw(img)
d.text((x, y), t, font=f, fill=(255, 255, 255, 240))
d.line([(W // 2 - 80, int(H * .925) + 62), (W // 2 + 80, int(H * .925) + 62)], fill=MAG, width=4)
save("handle", img, keep_full=True)
json.dump(anchors, open(f"{TYPE}/anchors.json", "w"))
print("TYPE_DONE", flush=True)

KEYS = [(0, .60, -4, .50, .46), (3.4, .60, -4, .50, .46), (4.4, 1, 0, .5, .5), (7.6, 1, 0, .5, .5),
        (8.5, 1, 0, .5, .5), (11.3, 1, 0, .5, .5), (12.2, .60, 3.5, .48, .47), (16.4, .60, 3.5, .48, .47),
        (17.3, 1, 0, .5, .5), (21.0, 1, 0, .5, .5), (21.9, 1, 0, .5, .5), (26.0, 1, 0, .5, .5),
        (26.9, .58, -3.5, .48, .47), (30.4, .58, -3.5, .48, .47), (31.3, 1, 0, .5, .5), (35.4, 1, 0, .5, .5)]

CUES = [(.10, 4.30, "kicker", "front"), (.10, 4.30, "hero_spisok", "behind"),
        (.35, 4.30, "front_spisok", "front"), (.45, 4.30, "front_procedur", "front"),
        (4.80, 7.60, "ph_zapretila", "front"),
        (8.60, 11.40, "li_botoks", "front"), (9.20, 11.40, "li_bio", "front"),
        (9.80, 11.40, "li_guby", "front"), (10.40, 11.40, "li_podb", "front"),
        (12.40, 16.40, "hero_cheklist", "behind"), (12.60, 16.40, "ph_nechek", "front"),
        (17.60, 21.10, "hero_moda", "behind"), (17.90, 21.10, "ph_podruga", "front"),
        (22.10, 25.90, "ph_vozrast", "front"), (27.00, 30.50, "hero_ponimanie", "behind"),
        (27.30, 30.50, "ph_nichego", "front"), (31.60, 35.30, "hero_uhod", "behind"),
        (31.90, 35.30, "ph_final", "front")]

PROPS = [(.70, 4.20, "list_note", .79, .70, .60, -8, 26, -22),
         (12.70, 16.30, "list_note_x", .80, .30, .56, 9, -22, 20),
         (17.70, 21.00, "bottle", .83, .30, .62, 11, -26, 22),
         (27.10, 30.40, "ampoule", .84, .31, .66, -10, 22, 18)]

IN_T, OUT_T, PFADE = 0.26, 0.20, 0.40
N = int(DUR * FPS)
FBY = W * H * 3
AN = json.load(open(f"{TYPE}/anchors.json"))
TI = {os.path.basename(p)[:-4]: Image.open(p).convert("RGBA") for p in glob.glob(f"{TYPE}/*.png")}
TN = {k: np.asarray(v).astype(np.float32) for k, v in TI.items() if AN[k][2]}
P = {os.path.basename(p)[:-4]: Image.open(p).convert("RGBA") for p in glob.glob(f"{PR}/*.png")}
yy, xx = np.mgrid[0:H, 0:W]
rr = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIG = np.clip(1 - .30 * np.clip((rr - .55) / .85, 0, 1) ** 1.6, 0, 1)[:, :, None]
mc, sc_cache = {}, {}


def smooth(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def ease_out(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def layout(t):
    if t <= KEYS[0][0]:
        return KEYS[0][1:]
    for i in range(len(KEYS) - 1):
        t0, s0, a0, x0, y0 = KEYS[i]; t1, s1, a1, x1, y1 = KEYS[i + 1]
        if t0 <= t <= t1:
            k = smooth((t - t0) / (t1 - t0)) if t1 > t0 else 0
            return (s0 + (s1 - s0) * k, a0 + (a1 - a0) * k,
                    x0 + (x1 - x0) * k, y0 + (y1 - y0) * k)
    return KEYS[-1][1:]


def over(dst, src, mul=1.0):
    if mul <= .002:
        return dst
    a = (src[:, :, 3:4] / 255.) * mul
    dst[:, :, :3] = src[:, :, :3] * a + dst[:, :, :3] * (1 - a)
    return dst


def paste(dst, rgba, px, py, mul=1.0):
    h, w = rgba.shape[:2]
    y0, y1 = max(0, py), min(H, py + h); x0, x1 = max(0, px), min(W, px + w)
    if y1 <= y0 or x1 <= x0:
        return dst
    sub = rgba[y0 - py:y0 - py + (y1 - y0), x0 - px:x0 - px + (x1 - x0)]
    a = (sub[:, :, 3:4] / 255.) * mul
    dst[y0:y1, x0:x1, :3] = sub[:, :, :3] * a + dst[y0:y1, x0:x1, :3] * (1 - a)
    return dst


def rmask(size, rad):
    if size not in mc:
        m = Image.new("L", size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], rad, fill=255)
        mc[size] = m
    return mc[size]


def plate(vi):
    s = vi.resize((W // 10, H // 10), Image.BILINEAR).filter(ImageFilter.GaussianBlur(9))
    return np.asarray(s.resize((W, H), Image.BICUBIC)).astype(np.float32) * .34


def cue_anim(t, s, e):
    if t < s:
        p = (t - (s - IN_T)) / IN_T
        if p <= 0:
            return 0, 1, 0
        k = ease_out(p)
        return k, .90 + .10 * k, int((1 - k) * 26)
    if t > e - OUT_T:
        p = (e - t) / OUT_T
        if p <= 0:
            return 0, 1, 0
        hold = (e - OUT_T - s) / max(e - s, .01)
        return max(p, 0), 1.0 + .022 * hold + (1 - p) * .03, int(-(1 - p) * 10)
    hold = (t - s) / max(e - s, .01)
    return 1.0, 1.0 + .022 * hold, 0


def draw_cue(canvas, key, alpha, scale, dy):
    ax, ay, full = AN[key]
    if full:
        return over(canvas, TN[key], alpha)
    im = TI[key]
    nw, nh = max(1, int(im.width * scale)), max(1, int(im.height * scale))
    ck = (key, nw, nh)
    if ck not in sc_cache:
        if len(sc_cache) > 260:
            sc_cache.clear()
        sc_cache[ck] = np.asarray(im.resize((nw, nh), Image.LANCZOS)).astype(np.float32)
    arr = sc_cache[ck]
    cx = ax + im.width / 2
    cy = ay + im.height / 2
    return paste(canvas, arr, int(cx - nw / 2), int(cy - nh / 2) + dy, alpha)


rd = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", f"{EDIT}/base.mp4",
                       "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
wr = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                       "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-profile:v", "high",
                       "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                       f"{EDIT}/body.mp4", "-loglevel", "error"], stdin=subprocess.PIPE)

for fi in range(N):
    raw = rd.stdout.read(FBY)
    if len(raw) < FBY:
        break
    t = fi / FPS
    vnp = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
    vim = Image.fromarray(vnp)
    scl, ang, cx, cy = layout(t)
    fullb = scl >= .995 and abs(ang) < .05
    canvas = vnp.astype(np.float32).copy() if fullb else plate(vim)

    beh = np.zeros((H, W, 4), np.float32)
    for s, e, k, wl in CUES:
        if wl == "behind" and s - IN_T < t < e + OUT_T:
            a, _, _ = cue_anim(t, s, e)
            if a > 0:
                aa = (TN[k][:, :, 3:4] / 255.) * a * (.30 if fullb else .62)
                beh[:, :, :3] = TN[k][:, :, :3] * aa + beh[:, :, :3] * (1 - aa)
                beh[:, :, 3:4] = np.maximum(beh[:, :, 3:4], aa * 255.)
    canvas = over(canvas, beh)

    if not fullb:
        cw, ch = int(W * scl), int(H * scl)
        card = vim.resize((cw, ch), Image.LANCZOS).convert("RGBA")
        card.putalpha(rmask((cw, ch), 34))
        card = card.rotate(ang, resample=Image.BICUBIC, expand=True)
        ca = np.asarray(card).astype(np.float32)
        sh = Image.fromarray(ca[:, :, 3].astype(np.uint8)).resize(
            (ca.shape[1] // 6, ca.shape[0] // 6), Image.BILINEAR)
        sh = sh.filter(ImageFilter.GaussianBlur(7)).resize((ca.shape[1], ca.shape[0]), Image.BICUBIC)
        shad = np.zeros_like(ca)
        shad[:, :, 3] = np.asarray(sh).astype(np.float32) * .62
        px = int(W * cx) - ca.shape[1] // 2
        py = int(H * cy) - ca.shape[0] // 2
        canvas = paste(canvas, shad, px + 4, py + 24)
        canvas = paste(canvas, ca, px, py)

    for s, e, nm, x, y, pscl, ang2, dx, dy in PROPS:
        if s - PFADE < t < e + PFADE and nm in P:
            a = max(0.0, min(1.0, (t - s) / PFADE, (e - t) / PFADE))
            if a <= 0:
                continue
            k = smooth((t - s) / max(e - s, .01))
            im = P[nm]
            ob = im.resize((int(im.width * pscl), int(im.height * pscl)), Image.LANCZOS)
            ob = ob.rotate(ang2, resample=Image.BICUBIC, expand=True)
            oa = np.asarray(ob).astype(np.float32)
            canvas = paste(canvas, oa, int(W * x) - oa.shape[1] // 2 + int(dx * k),
                           int(H * y) - oa.shape[0] // 2 + int(dy * k), a)

    for s, e, k, wl in CUES:
        if wl == "front" and s - IN_T < t < e + OUT_T:
            a, sca, dy = cue_anim(t, s, e)
            if a > 0:
                canvas = draw_cue(canvas, k, a, sca, dy)

    canvas *= VIG
    canvas = over(canvas, TN["handle"], .9)
    wr.stdin.write(np.clip(canvas, 0, 255).astype(np.uint8).tobytes())
    if fi % 200 == 0:
        print(f"frame {fi}/{N}", flush=True)

wr.stdin.close(); wr.wait(); rd.stdout.close(); rd.wait()
print("COMPOSITE_DONE", flush=True)

OUT = "/home/user/-claude-workspace/.bmm_out"
os.makedirs(OUT, exist_ok=True)
# master
subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", f"{EDIT}/body.mp4",
                "-c:v", "libx264", "-preset", "veryslow", "-crf", "20",
                "-profile:v", "high", "-level", "4.2", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", f"{OUT}/BMM_master_1080.mp4",
                "-loglevel", "error"], check=True)
# lighter, widely compatible
subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", f"{EDIT}/body.mp4",
                "-c:v", "libx264", "-preset", "slow", "-crf", "26",
                "-profile:v", "main", "-level", "4.0", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", f"{OUT}/BMM_light_1080.mp4",
                "-loglevel", "error"], check=True)
# 720p, baseline — plays and downloads anywhere
subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", f"{EDIT}/body.mp4",
                "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264",
                "-preset", "slow", "-crf", "26", "-profile:v", "baseline",
                "-level", "3.1", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                f"{OUT}/BMM_720.mp4", "-loglevel", "error"], check=True)
print("ALL_DONE", flush=True)
