/* ── reusable scene art: jars, shelf, bokeh, grain ───────────────── */

let UID = 0;
const uid = (p) => `${p}${++UID}`;

/* deterministic prng — renders must be byte-stable between runs */
let SEED = 20260818;
const rnd = () => { SEED = (SEED * 1664525 + 1013904223) % 4294967296; return SEED / 4294967296; };

/* amber / cream supplement jar with white cap, label and warm rim light */
function jar({ w = 118, h = 246, tint = 'amber', brand = '', title = '', color = '#4a6ea8', sub = 3 } = {}) {
  const g = uid('g'), lg = uid('l'), hi = uid('h'), cl = uid('c');
  const glass = tint === 'amber'
    ? ['#7c3f14', '#a85a1e', '#5c2e0f']
    : ['#63523f', '#877257', '#4a3d2f'];
  const capW = w * 0.66, capH = h * 0.135, capX = (w - capW) / 2;
  const bodyY = capH * 0.78, bodyH = h - bodyY;
  const labX = w * 0.075, labW = w - labX * 2;
  const labY = bodyY + bodyH * 0.30, labH = bodyH * 0.46;
  const brandSize = Math.min(labH * 0.20, (labW * 1.45) / Math.max(4, brand.length || 4));
  const titleSize = Math.min(labH * 0.27, (labW * 1.55) / Math.max(3, title.length || 3));
  const dots = Array.from({ length: sub }, (_, i) =>
    `<rect x="${labX + labW * 0.18}" y="${labY + labH * 0.66 + i * (labH * 0.10)}" width="${labW * 0.64}" height="${labH * 0.045}" rx="${labH * 0.022}" fill="#b9b0a6" opacity=".55"/>`).join('');

  return `<svg class="jar" width="${w}" height="${h + 26}" viewBox="0 0 ${w} ${h + 26}" fill="none">
    <defs>
      <linearGradient id="${g}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="${glass[2]}"/><stop offset=".18" stop-color="${glass[1]}"/>
        <stop offset=".52" stop-color="${glass[0]}"/><stop offset=".86" stop-color="${glass[2]}"/>
        <stop offset="1" stop-color="${glass[2]}"/>
      </linearGradient>
      <linearGradient id="${lg}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#f4f0ea"/><stop offset="1" stop-color="#ddd6cd"/>
      </linearGradient>
      <linearGradient id="${hi}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset="1" stop-color="#ffffff" stop-opacity=".06"/>
      </linearGradient>
      <clipPath id="${cl}"><rect x="1" y="${bodyY}" width="${w - 2}" height="${bodyH}" rx="16"/></clipPath>
    </defs>
    <ellipse cx="${w / 2}" cy="${h + 12}" rx="${w * 0.52}" ry="9" fill="#000" opacity=".45"/>
    <!-- body -->
    <rect x="1" y="${bodyY}" width="${w - 2}" height="${bodyH}" rx="16" fill="url(#${g})"/>
    <g clip-path="url(#${cl})">
      <rect x="${w * 0.14}" y="${bodyY}" width="${w * 0.10}" height="${bodyH}" fill="url(#${hi})" opacity=".85"/>
      <rect x="${w * 0.80}" y="${bodyY}" width="${w * 0.09}" height="${bodyH}" fill="#ffd9a8" opacity=".28"/>
      <rect x="1" y="${bodyY}" width="${w - 2}" height="${bodyH * 0.14}" fill="#000" opacity=".22"/>
    </g>
    <rect x="1.5" y="${bodyY + .5}" width="${w - 3}" height="${bodyH - 1}" rx="15.5" stroke="#ffcf9c" stroke-opacity=".22"/>
    <!-- label -->
    <rect x="${labX}" y="${labY}" width="${labW}" height="${labH}" rx="7" fill="url(#${lg})"/>
    <rect x="${labX}" y="${labY}" width="${labW}" height="${labH}" rx="7" fill="#000" opacity=".05"/>
    <text x="${w / 2}" y="${labY + labH * 0.31}" text-anchor="middle" fill="${color}"
      font-family="Montserrat" font-size="${brandSize}" font-weight="800" letter-spacing=".4">${brand}</text>
    <text x="${w / 2}" y="${labY + labH * 0.52}" text-anchor="middle" fill="${color}"
      font-family="Montserrat" font-size="${titleSize}" font-weight="800" letter-spacing=".3">${title}</text>
    ${dots}
    <ellipse cx="${w / 2}" cy="${bodyY + 3}" rx="${capW * 0.52}" ry="5" fill="#000" opacity=".30"/>
    <!-- cap -->
    <rect x="${capX}" y="0" width="${capW}" height="${capH}" rx="7" fill="url(#${lg})"/>
    <rect x="${capX}" y="${capH * 0.72}" width="${capW}" height="${capH * 0.28}" rx="4" fill="#cfc7bd"/>
    <rect x="${capX + capW * 0.08}" y="${capH * 0.14}" width="${capW * 0.14}" height="${capH * 0.52}" rx="3" fill="#fff" opacity=".75"/>
  </svg>`;
}

function shelfSilhouette() {
  let books = '', x = 18;
  const tones = ['#3a2b46', '#4a3350', '#2f2340', '#523a58', '#3d2c49', '#5b4260', '#342744'];
  while (x < 520) {
    const w = 16 + Math.round(rnd() * 20), hh = 78 + Math.round(rnd() * 46);
    books += `<rect x="${x}" y="${190 - hh}" width="${w}" height="${hh}" rx="3" fill="${tones[Math.floor(rnd() * tones.length)]}"/>`;
    x += w + 3 + Math.round(rnd() * 5);
  }
  let books2 = '', x2 = 44;
  while (x2 < 520) {
    const w = 15 + Math.round(rnd() * 22), hh = 70 + Math.round(rnd() * 40);
    books2 += `<rect x="${x2}" y="${420 - hh}" width="${w}" height="${hh}" rx="3" fill="${tones[Math.floor(rnd() * tones.length)]}" opacity=".8"/>`;
    x2 += w + 4 + Math.round(rnd() * 6);
  }
  return `<svg width="560" height="620" viewBox="0 0 560 620" fill="none">
    ${books}<rect x="10" y="190" width="530" height="9" rx="3" fill="#2a1f36"/>
    ${books2}<rect x="10" y="420" width="530" height="9" rx="3" fill="#2a1f36" opacity=".85"/>
  </svg>`;
}

function bokeh(host, n = 16) {
  let s = '';
  for (let i = 0; i < n; i++) {
    const size = 8 + rnd() * 46;
    const x = rnd() * 1080, y = rnd() * 780;
    const warm = x > 560;
    const c = warm ? '255,196,140' : '176,150,232';
    s += `<i style="left:${x}px;top:${y}px;width:${size}px;height:${size}px;
      background:radial-gradient(circle,rgba(${c},.34) 0%,rgba(${c},.10) 55%,rgba(${c},0) 72%);
      filter:blur(${1 + rnd() * 3}px);opacity:${.35 + rnd() * .5}"></i>`;
  }
  host.innerHTML = s;
}

const GRAIN = `<svg width="1080" height="1440"><filter id="gr">
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/>
  <feColorMatrix type="saturate" values="0"/></filter>
  <rect width="1080" height="1440" filter="url(#gr)"/></svg>`;

function paintScene({ shelf = true, grain = true, bokehCount = 16 } = {}) {
  if (shelf) { const s = document.querySelector('.bg-shelf'); if (s) s.innerHTML = shelfSilhouette(); }
  const b = document.querySelector('.bokeh'); if (b) bokeh(b, bokehCount);
  const g = document.querySelector('.grain'); if (g && grain) g.innerHTML = GRAIN;
}

/* loose tablets scattered on the table — same prop language as the reference frames */
function tablets(list) {
  return list.map(t => {
    const g = uid('t');
    const rx = t.r || 15, ry = (t.r || 15) * 0.62;
    return `<svg style="position:absolute;left:${t.x}px;top:${t.y}px" width="${rx * 2 + 8}" height="${ry * 2 + 16}" fill="none">
      <defs><linearGradient id="${g}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="${t.c1}"/><stop offset="1" stop-color="${t.c2}"/></linearGradient></defs>
      <ellipse cx="${rx + 4}" cy="${ry + 12}" rx="${rx * 0.92}" ry="${ry * 0.5}" fill="#000" opacity=".42"/>
      <ellipse cx="${rx + 4}" cy="${ry + 6}" rx="${rx}" ry="${ry}" fill="url(#${g})"/>
      <ellipse cx="${rx + 1}" cy="${ry + 2}" rx="${rx * 0.45}" ry="${ry * 0.34}" fill="#fff" opacity=".34"/>
    </svg>`;
  }).join('');
}
