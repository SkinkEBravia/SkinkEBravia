"""Render the animated profile banner (assets/banner.gif).

60k particles orbit a domain-warped vortex, condense into the name,
then detonate back into the nebula. Rendered on the CPU with numpy:
additive splatting with motion blur, multi-scale bloom, chromatic
aberration and filmic tone mapping. The animation loops seamlessly.

    pip install numpy pillow scipy
    python assets/render_banner.py
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

W, H = 800, 260
FRAMES = 72
N = 60000
SUBSTEPS = 4
TEXT = "SkinkEBravia"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
rng = np.random.default_rng(7)


def text_targets():
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, 104)
    box = d.textbbox((0, 0), TEXT, font=font)
    x = (W - (box[2] - box[0])) / 2 - box[0]
    y = (H - (box[3] - box[1])) / 2 - box[1]
    d.text((x, y), TEXT, fill=255, font=font)
    ys, xs = np.nonzero(np.asarray(img) > 128)
    idx = rng.integers(0, len(xs), N)
    return np.stack([xs[idx], ys[idx]], 1).astype(np.float64) + rng.random((N, 2)) - 0.5


def warp(p, t):
    """Static-ish curl-like domain warp built from periodic sines (loops in t)."""
    x, y = p[:, 0] / W, p[:, 1] / H
    a = 2 * np.pi * t
    dx = (np.sin(7.1 * y + 2.3 * np.sin(5.3 * x) + a) * 38
          + np.sin(13.7 * y - 9.1 * x - 2 * a) * 12)
    dy = (np.sin(6.3 * x + 2.9 * np.cos(4.1 * y) - a) * 26
          + np.cos(11.3 * x + 8.7 * y + a) * 9)
    return np.stack([p[:, 0] + dx, p[:, 1] + dy], 1)


# per-particle vortex orbit: integer laps -> periodic in t
r0 = rng.random(N) ** 1.6 * 1.05 + 0.02
arm = rng.integers(0, 3, N) * 2 * np.pi / 3
theta0 = arm + r0 * 7.0 + rng.normal(0, 0.28, N) * (0.3 + r0)   # 3 log-spiral arms
laps = np.where(r0 < 0.3, 3, np.where(r0 < 0.65, 2, 1))        # differential rotation
depth = rng.random(N)                                          # brightness / "z"


def swirl(t):
    th = theta0 + 2 * np.pi * laps * t
    rx, ry = r0 * 360, r0 * 120
    p = np.stack([W / 2 + rx * np.cos(th), H / 2 + ry * np.sin(th)], 1)
    q = warp(p, t)
    return p + (q - p) * 0.35 * r0[:, None]


targets = text_targets()
# per-particle colour: gradient across the word, cyan -> violet -> ember
u = np.clip(targets[:, 0] / W, 0, 1)
stops = np.array([[0.10, 0.85, 1.00], [0.55, 0.30, 1.00],
                  [1.00, 0.25, 0.65], [1.00, 0.60, 0.15]])
seg = u * (len(stops) - 1)
i = np.minimum(seg.astype(int), len(stops) - 2)
f = (seg - i)[:, None]
color = stops[i] * (1 - f) + stops[i + 1] * f
text_color = color * (0.45 + 0.55 * depth)[:, None]
core = np.array([1.0, 0.75, 0.45]); rim = np.array([0.25, 0.45, 1.0])
g = np.clip(r0, 0, 1)[:, None]
galaxy_color = (core * (1 - g) + rim * g) * (0.25 + 0.75 * depth ** 3)[:, None]
delay = (targets[:, 0] / W) * 0.10 + rng.random(N) * 0.03   # letters form left->right


def smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * x * (x * (6 * x - 15) + 10)


def positions(t):
    """t in [0,1). Swirl -> form text -> hold -> explode -> swirl."""
    form = smooth((t - 0.18 - delay) / 0.22)
    unform = smooth((t - 0.70) / 0.26)
    w = form * (1 - unform)
    p = swirl(t) * (1 - w)[:, None] + targets * w[:, None]
    # shimmer while held
    s = np.sin(2 * np.pi * (t * 6 + depth)) * 0.6 * w
    p[:, 1] += s
    # detonation impulse radiating from centre
    k = np.clip((t - 0.70) / 0.26, 0, 1)
    burst = np.sin(np.pi * k) ** 2 * (0.6 + depth)
    d = targets - np.array([W / 2, H / 2])
    d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-6
    p += d * burst[:, None] * 170
    return p, w, k


def splat(p, weight, color):
    x = np.round(p[:, 0]).astype(int)
    y = np.round(p[:, 1]).astype(int)
    ok = (x >= 0) & (x < W) & (y >= 0) & (y < H)
    lin = y[ok] * W + x[ok]
    out = np.empty((H, W, 3))
    for c in range(3):
        out[..., c] = np.bincount(lin, color[ok, c] * weight[ok],
                                  minlength=W * H).reshape(H, W)
    return out


yy, xx = np.mgrid[0:H, 0:W]
vignette = 1 - 0.55 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
bg = np.stack([0.010 + 0.012 * (yy / H), 0.008 + 0.0 * yy, 0.025 + 0.02 * (1 - yy / H)], -1)
rr = np.hypot(xx - W / 2, (yy - H / 2) * 2.2)


def render(t):
    acc = np.zeros((H, W, 3))
    for s in range(SUBSTEPS):                     # motion blur
        ts = (t + s / (SUBSTEPS * FRAMES)) % 1.0
        p, w, k = positions(ts)
        col = galaxy_color * (1 - w)[:, None] + text_color * w[:, None]
        acc += splat(p, 0.22 + 0.45 * w, col)
    acc /= SUBSTEPS
    bloom = (gaussian_filter(acc, (1.5, 1.5, 0)) * 0.6
             + gaussian_filter(acc, (6, 6, 0)) * 0.7
             + gaussian_filter(acc, (20, 20, 0)) * 1.1)
    img = acc * 0.9 + bloom
    # shockwave ring
    k = np.clip((t - 0.70) / 0.26, 0, 1)
    if 0 < k < 1:
        R = k * 520
        ring = np.exp(-((rr - R) / 10) ** 2) * (1 - k) ** 1.5 * 1.4
        img += ring[..., None] * np.array([0.6, 0.8, 1.0])
    # chromatic aberration
    img[..., 0] = np.roll(img[..., 0], 2, 1)
    img[..., 2] = np.roll(img[..., 2], -2, 1)
    img = 1 - np.exp(-img * 1.1)                  # filmic-ish tonemap
    img = img * vignette[..., None] + bg
    return np.clip(img, 0, 1)


def main():
    frames = []
    for n in range(FRAMES):
        frames.append((render(n / FRAMES) * 255).astype(np.uint8))
        print(f"frame {n + 1}/{FRAMES}", end="\r")
    # one shared palette avoids flicker between frames
    sample = np.concatenate(frames[::6], 0)
    pal = Image.fromarray(sample).quantize(256, method=Image.Quantize.MEDIANCUT)
    imgs = [Image.fromarray(f).quantize(palette=pal, dither=Image.Dither.NONE)
            for f in frames]
    imgs[0].save("assets/banner.gif", save_all=True, append_images=imgs[1:],
                 duration=45, loop=0, optimize=True, disposal=1)
    print("\nwrote assets/banner.gif")


if __name__ == "__main__":
    main()
