// Render studio/index.html deterministically, frame by frame, then encode assets/banner.gif.
//   npm i -g playwright   (or have it locally)   +   ffmpeg on PATH or $FFMPEG
//   node studio/capture.mjs
import { chromium } from "playwright";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, "frames");
rmSync(out, { recursive: true, force: true }); mkdirSync(out);

const browser = await chromium.launch({
  args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"],
});
const page = await browser.newPage({ viewport: { width: 960, height: 360 } });
page.on("console", m => console.log("[page]", m.text()));
page.on("pageerror", e => { console.error(e); process.exit(1); });
await page.goto(pathToFileURL(path.join(here, "index.html")).href + "?capture");
await page.waitForFunction(() => window.ready === true);
const n = await page.evaluate(() => window.FRAMES);
for (let f = 0; f < n; f++) {
  const url = await page.evaluate(f => window.renderFrame(f), f);
  writeFileSync(path.join(out, `f${String(f).padStart(3, "0")}.png`), Buffer.from(url.split(",")[1], "base64"));
  process.stdout.write(`\rframe ${f + 1}/${n}`);
}
await browser.close();

const ffmpeg = process.env.FFMPEG || "ffmpeg";
const gif = path.join(here, "..", "assets", "banner.gif");
execFileSync(ffmpeg, ["-y", "-loglevel", "error", "-framerate", "24", "-i", path.join(out, "f%03d.png"),
  "-vf", "scale=800:-1:flags=area,split[a][b];[a]palettegen=max_colors=256:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
  "-loop", "0", gif], { stdio: "inherit" });
console.log(`\nwrote ${gif}`);
