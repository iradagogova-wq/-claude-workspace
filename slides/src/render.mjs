import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import fs from 'fs';
import path from 'path';

const here = path.dirname(fileURLToPath(import.meta.url));
const targets = process.argv.slice(2);
const list = targets.length ? targets : ['slide5', 'slide6'];

const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--font-render-hinting=none'] });

for (const name of list) {
  /* если в frames/ лежит сгенерированный кадр с персонажами — он становится фоном,
     нарисованная кодом сцена прячется, текст уходит в левую тёмную колонку */
  const frame = fs.existsSync(path.join(here, 'frames', `${name}.png`)) ? `frames/${name}.png` : null;

  for (const [suffix, scale] of [['', 1], ['@2x', 2]]) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: scale });
    await page.goto('file://' + path.join(here, `${name}.html`));
    await page.waitForFunction(() => document.fonts.status === 'loaded');

    if (frame) {
      await page.evaluate(async (src) => {
        await new Promise((ok, fail) => {
          const img = new Image();
          img.onload = ok; img.onerror = () => fail(new Error('кадр не открылся: ' + src));
          img.src = src;
        });
        document.body.classList.add('has-frame');
        document.querySelector('.photo').style.backgroundImage = `url("${src}")`;
      }, frame);
    }

    await page.waitForTimeout(350);
    const out = path.join(here, '..', 'out', `${name}${suffix}.png`);
    await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1080, height: 1440 } });
    console.log('✓', path.relative(process.cwd(), out), frame ? '(с кадром)' : '(рисованная сцена)');
    await page.close();
  }
}
await browser.close();
