"""Build the delivery page: the reel embedded as a data URI so it can be saved
straight from the browser's own video controls."""
import base64, os, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = f"{ROOT}/out"
VIDEO = f"{OUT}/BMM_web.mp4"

b64 = base64.b64encode(open(VIDEO, "rb").read()).decode()
size_mb = os.path.getsize(f"{OUT}/BMM_master_1080.mp4") / 1048576
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "default=nw=1:nk=1", VIDEO],
                     capture_output=True, text=True).stdout.strip()
dur = f"{float(dur):.1f}"

HTML = f"""<title>Ролик «Список процедур»</title>
<style>
  :root {{
    --ground:#0C0B0E; --surface:#17151A; --hair:#2A272F;
    --ink:#F4F1F3; --muted:#A09AA6; --accent:#E10B6E; --accent-soft:#FF4E96;
    --step:clamp(.95rem,.9rem + .3vw,1.05rem);
  }}
  *{{box-sizing:border-box}}
  body{{
    margin:0; background:var(--ground); color:var(--ink);
    font-family:"Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;
    font-size:var(--step); line-height:1.6;
    -webkit-font-smoothing:antialiased;
    padding:clamp(20px,5vw,52px) clamp(16px,4vw,24px) 64px;
    display:flex; justify-content:center;
  }}
  .wrap{{width:100%; max-width:452px; display:flex; flex-direction:column; gap:32px}}
  .eyebrow{{
    font-size:.68rem; letter-spacing:.22em; text-transform:uppercase;
    color:var(--muted); margin:0 0 10px;
  }}
  h1{{
    margin:0; font-size:clamp(1.7rem,1.3rem + 2.2vw,2.3rem); line-height:1.08;
    letter-spacing:-.02em; font-weight:800; text-wrap:balance;
  }}
  h1 em{{font-style:normal; color:var(--accent)}}
  .rule{{width:56px; height:3px; background:var(--accent); border:0; margin:16px 0 0}}
  .player{{
    position:relative; border-radius:18px; overflow:hidden;
    background:#000; border:1px solid var(--hair);
    box-shadow:0 26px 70px -30px rgba(225,11,110,.55), 0 2px 0 rgba(255,255,255,.03) inset;
  }}
  video{{display:block; width:100%; height:auto; background:#000}}
  h2{{
    margin:0 0 14px; font-size:.72rem; letter-spacing:.2em;
    text-transform:uppercase; color:var(--muted); font-weight:700;
  }}
  ol{{margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:1px;
     background:var(--hair); border:1px solid var(--hair); border-radius:14px; overflow:hidden}}
  li{{background:var(--surface); padding:16px 18px; display:flex; gap:14px; align-items:baseline}}
  .dev{{
    flex:0 0 auto; min-width:74px; font-size:.7rem; font-weight:800;
    letter-spacing:.1em; text-transform:uppercase; color:var(--accent-soft);
  }}
  .how{{margin:0; color:var(--ink)}}
  .how b{{font-weight:700; color:#fff}}
  table{{width:100%; border-collapse:collapse; font-size:.86rem}}
  td{{padding:11px 0; border-bottom:1px solid var(--hair); vertical-align:top}}
  td:first-child{{color:var(--muted); width:44%}}
  td:last-child{{text-align:right; font-variant-numeric:tabular-nums}}
  tr:last-child td{{border-bottom:0}}
  .note{{
    margin:0; padding:14px 16px; border-left:2px solid var(--accent);
    background:var(--surface); border-radius:0 10px 10px 0;
    color:var(--muted); font-size:.84rem;
  }}
  footer{{color:var(--muted); font-size:.76rem; letter-spacing:.04em}}
</style>

<div class="wrap">
  <header>
    <p class="eyebrow">BMM Cosmetology · Reels 9:16</p>
    <h1>Список <em>процедур</em></h1>
    <hr class="rule">
  </header>

  <div class="player">
    <video controls playsinline preload="metadata"
           src="data:video/mp4;base64,{b64}"></video>
  </div>

  <section>
    <h2>Как сохранить</h2>
    <ol>
      <li><span class="dev">iPhone</span>
        <p class="how">Задержите палец на видео → <b>«Сохранить в Фото»</b></p></li>
      <li><span class="dev">Android</span>
        <p class="how">Три точки в углу плеера → <b>«Скачать»</b></p></li>
      <li><span class="dev">Компьютер</span>
        <p class="how">Правый клик по видео → <b>«Сохранить видео как…»</b></p></li>
    </ol>
  </section>

  <section>
    <h2>Файл</h2>
    <table>
      <tr><td>Длительность</td><td>{dur} с</td></tr>
      <tr><td>Кадр</td><td>1080 × 1920</td></tr>
      <tr><td>Частота</td><td>30 к/с</td></tr>
      <tr><td>Звук</td><td>нет, под озвучку</td></tr>
      <tr><td>Мастер-версия</td><td>{size_mb:.0f} МБ</td></tr>
    </table>
  </section>

  <p class="note">Здесь встроена облегчённая версия для просмотра и быстрого
  сохранения. Мастер 1080p полного качества лежит отдельным файлом в переписке.</p>

  <footer>@bmm___cosmetolog</footer>
</div>
"""

path = f"{OUT}/page.html"
open(path, "w").write(HTML)
print("PAGE_DONE", path, round(len(HTML) / 1048576, 2), "MB", flush=True)
