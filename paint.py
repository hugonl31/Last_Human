"""paint.py - a small airbrush painter for the Last Human page's 80s box art (numpy + PIL + scipy).

Shapes are masks; solid() shades a mask as a smooth 3D object from its blurred height (diffuse light, a specular
highlight, optional chrome sky reflection, rim light), the way an airbrushed box painting reads. Backdrops: an 80s
sunset with a striped sun, a glowing perspective grid, mountains, stars, nebulae; beams, bursts and chrome lettering.
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter as gf, shift as nd_shift

SS = 3                                   # supersampling of the shape masks (antialiased edges)
FONTS = 'C:/Windows/Fonts/'


def noise(rnd, shape):
    """uniform noise from a random.Random (its own numpy generator)"""
    return np.random.default_rng(rnd.randrange(1 << 30)).random(shape, dtype=np.float32)


def C(h):
    """'#rrggbb' -> float rgb"""
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)], np.float32)


class Art:
    def __init__(self, W, H, bg='#000000'):
        self.W, self.H = W, H
        self.img = np.zeros((H, W, 3), np.float32) + C(bg)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        self.xx, self.yy = xx, yy

    # ---- masks
    def _mask(self, draw_fn):
        im = Image.new('L', (self.W * SS, self.H * SS), 0)
        draw_fn(ImageDraw.Draw(im), SS)
        im = im.resize((self.W, self.H), Image.BOX)
        return np.asarray(im, np.float32) / 255.0

    def poly(self, pts):
        return self._mask(lambda d, k: d.polygon([(x * k, y * k) for x, y in pts], fill=255))

    def ell(self, cx, cy, rx, ry=None):
        ry = rx if ry is None else ry
        return self._mask(lambda d, k: d.ellipse([(cx - rx) * k, (cy - ry) * k, (cx + rx) * k, (cy + ry) * k], fill=255))

    def rect(self, x0, y0, x1, y1, r=0):
        return self._mask(lambda d, k: d.rounded_rectangle([x0 * k, y0 * k, x1 * k, y1 * k], radius=r * k, fill=255))

    def lines(self, pts, w, closed=False):
        p = list(pts) + ([pts[0]] if closed else [])
        def f(d, k):
            d.line([(x * k, y * k) for x, y in p], fill=255, width=max(1, int(w * k)), joint='curve')
            for x, y in p:
                d.ellipse([(x - w / 2) * k, (y - w / 2) * k, (x + w / 2) * k, (y + w / 2) * k], fill=255)
        return self._mask(f)

    def text_mask(self, txt, font, size, x, y, anchor='mm', shear=0.0, sx=1.0):
        fnt = ImageFont.truetype(FONTS + font, int(size * SS))
        im = Image.new('L', (self.W * SS, self.H * SS), 0)
        ImageDraw.Draw(im).text((x * SS, y * SS), txt, font=fnt, fill=255, anchor=anchor)
        if shear or sx != 1.0:                              # italic slant / horizontal stretch about (x, y)
            a = 1.0 / sx; b = shear / sx
            im = im.transform(im.size, Image.AFFINE, (a, b, x * SS * (1 - a) - b * y * SS, 0, 1, 0), Image.BICUBIC)
        im = im.resize((self.W, self.H), Image.BOX)
        return np.asarray(im, np.float32) / 255.0

    # ---- paint
    def fill(self, m, col, k=1.0):
        col = col if isinstance(col, np.ndarray) and col.ndim == 3 else np.asarray(col, np.float32)
        a = (m * k)[..., None]
        self.img = self.img * (1 - a) + col * a

    def add(self, m, col, k=1.0):
        self.img += (m * k)[..., None] * np.asarray(col, np.float32)

    def glow(self, m, col, r, k=1.0):
        self.add(gf(m, r), col, k)

    def shadow(self, m, dx, dy, r, k=0.6):
        s = gf(nd_shift(m, (dy, dx), order=1), r)
        self.img *= (1 - k * np.clip(s, 0, 1))[..., None]

    def solid(self, m, base, light=(-0.55, -0.65, 0.55), bevel=6.0, amb=0.22, spec=0.55, shin=28,
              chrome=0.0, sky=('#2a1a5e', '#ff7bd5'), ground=('#3a1608', '#ffb347'), rim=None, rim_w=3.0,
              tex=0.0, rnd=None):
        """the mask as a smooth, lit 3D object (an airbrushed volume)"""
        h = gf(m, bevel)
        gy, gx = np.gradient(h)
        K = bevel * 2.2
        nx, ny, nz = -gx * K, -gy * K, np.ones_like(h)
        n = np.sqrt(nx * nx + ny * ny + nz * nz); nx, ny, nz = nx / n, ny / n, nz / n
        L = np.array(light, np.float32); L /= np.linalg.norm(L)
        d = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
        Hh = L + np.array([0, 0, 1.0]); Hh /= np.linalg.norm(Hh)
        sp = np.clip(nx * Hh[0] + ny * Hh[1] + nz * Hh[2], 0, 1) ** shin
        base = np.asarray(C(base) if isinstance(base, str) else base, np.float32)
        col = base * (amb + (1 - amb) * d)[..., None]
        if tex and rnd is not None:                         # (brushed / worn metal: a little grain)
            g = gf(noise(rnd, (self.H, self.W)), 1.2) - 0.5
            col *= (1 + tex * g)[..., None]
        if chrome:                                          # (80s chrome: the sky above, a horizon, the ground below)
            t = np.clip(ny * 1.6, -1, 1)                    #  normal pointing up (-y) reflects the sky
            s0, s1, g0, g1 = C(sky[0]), C(sky[1]), C(ground[0]), C(ground[1])
            u = np.clip(-t, 0, 1)[..., None]; v = np.clip(t, 0, 1)[..., None]
            skyc = s1 * (1 - u) + s0 * u
            gnd = g1 * (1 - np.sqrt(v)) + g0 * np.sqrt(v)
            w = np.clip((t + 0.35) / 0.7, 0, 1); w = (w * w * (3 - 2 * w))[..., None]   # (a soft horizon, not a cut)
            env = skyc * (1 - w) + gnd * w + np.exp(-(t / 0.09) ** 2)[..., None] * 0.55   # (+ its bright line)
            col = col * (1 - chrome) + env * chrome * (0.55 + 0.45 * d[..., None])
        col = col + (sp * spec)[..., None]
        if rim is not None:                                 # (a coloured light from behind on the far edges)
            edge = np.clip(m - gf(m, rim_w), 0, 1) * 2.5
            back = np.clip(-(nx * L[0] + ny * L[1]), 0, 1)
            col = col + (edge * back)[..., None] * C(rim)
        self.fill(m, col)

    # ---- backdrops
    def vgrad(self, stops, y0=0, y1=None, m=None):
        y1 = self.H if y1 is None else y1
        t = np.clip((self.yy - y0) / max(1, (y1 - y0)), 0, 1)
        col = np.zeros_like(self.img)
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            w = np.clip((t - a) / max(1e-6, b - a), 0, 1)[..., None]
            seg = ((t >= a) & (t <= b))[..., None]
            col = np.where(seg, C(ca) * (1 - w) + C(cb) * w, col)
        self.fill(np.ones((self.H, self.W), np.float32) if m is None else m, col)

    def stars(self, rnd, n, region=None, cols=('#ffffff', '#bcd4ff', '#ffe2b8')):
        x0, y0, x1, y1 = region or (0, 0, self.W, self.H)
        m = np.zeros((self.H, self.W), np.float32)
        big = np.zeros_like(m)
        for _ in range(n):
            x, y = rnd.uniform(x0, x1 - 1), rnd.uniform(y0, y1 - 1)
            b = rnd.random() ** 3
            m[int(y), int(x)] += 0.4 + b
            if b > 0.85: big[int(y), int(x)] = 1
        self.add(np.clip(gf(m, 0.6) * 3, 0, 1), C(cols[0]), 1.0)
        for (dx, dy) in ((1, 0), (0, 1)):                  # (the brightest: a four-point twinkle)
            st = gf(big, (0.6 + 5 * dy, 0.6 + 5 * dx)) * 40
            self.add(np.clip(st, 0, 1), C(cols[1]), 0.8)
        self.glow(big, C(cols[2]), 3, 30)

    def nebula(self, rnd, col, k=0.5, scale=60, region=None):
        n = gf(noise(rnd, (self.H, self.W)), scale)
        n = (n - n.min()) / (n.max() - n.min() + 1e-6)
        n = np.clip((n - 0.45) * 2.2, 0, 1) ** 1.5
        if region is not None:
            n *= region
        self.add(n, C(col), k)

    def sun(self, cx, cy, r, top='#ffe45c', bot='#ff2fa0', stripes=7, horizon=None):
        m = self.ell(cx, cy, r)
        t = np.clip((self.yy - (cy - r)) / (2 * r), 0, 1)[..., None]
        col = C(top) * (1 - t) + C(bot) * t
        cut = np.ones_like(m)
        for i in range(stripes):                            # (the 80s sun: bands cut from its lower half, wider below)
            yb = cy + r * (0.12 + 0.88 * i / stripes)
            hb = 2 + 9 * i / stripes
            cut *= 1 - ((self.yy > yb) & (self.yy < yb + hb)).astype(np.float32)
        if horizon is not None:
            cut *= (self.yy < horizon).astype(np.float32)
        self.glow(m, C(bot), r * 0.35, 0.9)
        self.fill(m * cut, col)

    def grid(self, horizon, vx, col='#ff3ad6', n_v=26, n_h=14, w=1.6, k=1.0, glow=3.0, spread=2.6):
        """a glowing perspective floor below the horizon line, vanishing at (vx, horizon)"""
        H = self.H
        pts = []
        m = np.zeros((self.H, self.W), np.float32)
        for i in range(-n_v, n_v + 1):
            xb = vx + i * self.W * spread / n_v
            m = np.maximum(m, self.lines([(vx, horizon), (xb, H + 40)], w))
        for j in range(1, n_h + 1):
            y = horizon + (H - horizon) * (j / n_h) ** 2.2
            m = np.maximum(m, self.lines([(-10, y), (self.W + 10, y)], w * (0.5 + j / n_h)))
        fade = np.clip((self.yy - horizon) / (H - horizon), 0, 1) ** 0.7
        m *= fade
        self.glow(m, C(col), glow, 1.4 * k)
        self.add(m, C(col), k)

    def mountains(self, rnd, base_y, hmin, hmax, col, edge=None, n=9, jag=0.35):
        pts = [(-20, self.H)]
        x = -20
        while x < self.W + 20:
            pts.append((x, base_y - rnd.uniform(hmin, hmax)))
            x += rnd.uniform(self.W / n * (1 - jag), self.W / n * (1 + jag))
            pts.append((x, base_y - rnd.uniform(hmin * 0.3, hmin)))
            x += rnd.uniform(self.W / n * 0.3, self.W / n * 0.6)
        pts += [(self.W + 20, self.H)]
        m = self.poly(pts)
        self.fill(m, C(col))
        if edge:
            e = np.clip(m - nd_shift(m, (4, 0), order=1), 0, 1)
            self.add(e, C(edge), 1.0)
        return m

    def beam(self, p0, p1, col, w=4, core='#ffffff', g=8, k=1.0):
        m = self.lines([p0, p1], w)
        self.glow(m, C(col), g, 1.6 * k)
        self.glow(m, C(col), g * 3, 0.8 * k)
        self.add(self.lines([p0, p1], max(1, w * 0.4)), C(core), k)

    def burst(self, cx, cy, r, rnd, cols=('#ffffff', '#ffe066', '#ff7a1a', '#c2185b'), spikes=18):
        for i, c in enumerate(reversed(cols)):
            rr = r * (1 - i * 0.22)
            pts = []
            for s in range(spikes * 2):
                a = s * math.pi / spikes + rnd.uniform(-0.08, 0.08)
                q = rr * (1.0 if s % 2 == 0 else rnd.uniform(0.45, 0.6))
                pts.append((cx + q * math.cos(a), cy + q * math.sin(a)))
            m = self.poly(pts)
            self.glow(m, C(c), r * 0.12, 0.6)
            self.fill(m, C(c))

    def flare(self, cx, cy, r, col='#ffffff', k=1.0):
        m = self.ell(cx, cy, r * 0.25)
        self.glow(m, C(col), r * 0.4, 2.2 * k)
        for ang, ln in ((0, 1.0), (math.pi / 2, 0.6)):
            dx, dy = math.cos(ang) * r * 2.4 * ln, math.sin(ang) * r * 2.4 * ln
            self.glow(self.lines([(cx - dx, cy - dy), (cx + dx, cy + dy)], r * 0.06), C(col), r * 0.05, 1.5 * k)

    def vignette(self, k=0.55, p=2.2):
        cx, cy = self.W / 2, self.H / 2
        d = np.sqrt(((self.xx - cx) / cx) ** 2 + ((self.yy - cy) / cy) ** 2) / math.sqrt(2)
        self.img *= (1 - k * d ** p)[..., None]

    def grain(self, rnd, k=0.025):
        self.img += (noise(rnd, (self.H, self.W))[..., None] - 0.5) * k

    def chrome_title(self, txt, cx, cy, size, font='impact.ttf', shear=-0.28, sx=1.0, depth=10,
                     face=('#fff6d8', '#ffd34d', '#ff7b1c', '#7a1500'), side='#4a0a24', edge='#ffffff', glow='#ff2fa0'):
        """chunky slanted 80s title: an extruded side, a chrome gradient face with a horizon line, a bright rim"""
        for i in range(depth, 0, -1):                       # (the extrusion, darker further back)
            mi = self.text_mask(txt, font, size, cx + i * 0.6, cy + i, shear=shear, sx=sx)
            self.fill(mi, C(side) * (0.6 + 0.4 * (1 - i / depth)))
        m = self.text_mask(txt, font, size, cx, cy, shear=shear, sx=sx)
        ys = np.where(m.max(axis=1) > 0.3)[0]
        y0, y1 = (ys.min(), ys.max()) if len(ys) else (cy - size / 2, cy + size / 2)
        t = np.clip((self.yy - y0) / max(1, y1 - y0), 0, 1)
        f0, f1, f2, f3 = (C(c) for c in face)
        hor = 0.52
        up = (t < hor)[..., None]
        a = (t / hor)[..., None]; b = ((t - hor) / (1 - hor))[..., None]
        col = np.where(up, f0 * (1 - a) + f1 * a, f2 * (1 - b) + f3 * b)
        self.glow(m, C(glow), size * 0.12, 0.9)
        self.fill(m, col)
        e = np.clip(m - nd_shift(m, (2.0, 1.0), order=1), 0, 1)       # (light on the upper-left edges)
        self.add(e, C(edge), 0.9)
        self.add(self.text_mask(txt, font, size, cx, cy, shear=shear, sx=sx) * 0 , C(edge), 0)
        return m

    def save(self, path, scale=1.0):
        im = Image.fromarray((np.clip(self.img, 0, 1) ** (1 / 1.0) * 255 + 0.5).astype(np.uint8), 'RGB')
        if scale != 1.0:
            im = im.resize((int(self.W * scale), int(self.H * scale)), Image.LANCZOS)
        im.save(path, optimize=True)
        return im
