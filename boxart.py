"""boxart.py - Last Human 'as it would look in real life': 80s cartridge-box style paintings (paint.py).

    python site/boxart.py            -> site/img/art/*.png
"""
import math, os, random, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paint import Art, C, gf                                     # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'art')
STEEL, GUN, DARK = '#9aa3b8', '#5a6278', '#2a2e3c'


def rot(pts, cx, cy, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def ngon(cx, cy, r, n, a0=0.0, sy=1.0):
    return [(cx + r * math.cos(a0 + 2 * math.pi * i / n), cy + r * sy * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]


# ------------------------------------------------------------------ the robots, painted
def guardian(a, cx, cy, s, rnd, eye='#ff3b1f'):
    """the Guardian: a hexagonal armoured core behind eight floating plates, one great eye"""
    a.glow(a.ell(cx, cy, s * 1.5), C('#ff2fa0'), s * 0.5, 0.35)             # (its own light on the haze)
    for i in range(8):                                                     # the eight plates, slightly apart
        a0 = math.radians(i * 45 + 22.5 - 17); a1 = math.radians(i * 45 + 22.5 + 17)
        r0, r1 = s * 1.02, s * 1.42
        pts = [(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)), (cx + r1 * math.cos(a0 - 0.05), cy + r1 * math.sin(a0 - 0.05)),
               (cx + r1 * math.cos(a1 + 0.05), cy + r1 * math.sin(a1 + 0.05)), (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1))]
        m = a.poly(pts)
        a.shadow(m, 6, 10, 8, 0.45)
        a.solid(m, STEEL, bevel=s * 0.06, chrome=0.4, rim='#ff5fd2', spec=0.75, tex=0.25, rnd=rnd)
        am = (a0 + a1) / 2                                                 # (two rivets a plate)
        for f in (0.35, 0.65):
            ang = a0 + (a1 - a0) * f
            rr = (r0 + r1) / 2
            a.solid(a.ell(cx + rr * math.cos(ang), cy + rr * math.sin(ang), s * 0.035), '#d8dde8', bevel=1.5, spec=1.0)
        a.add(a.lines([(cx + (r0 + 6) * math.cos(am), cy + (r0 + 6) * math.sin(am)),
                       (cx + (r1 - 6) * math.cos(am), cy + (r1 - 6) * math.sin(am))], 1.5), C('#20242e'), -0.5)
    hexo = a.poly(ngon(cx, cy, s * 0.86, 6, math.radians(30)))
    a.shadow(hexo, 8, 12, 12, 0.6)
    a.solid(hexo, GUN, bevel=s * 0.08, chrome=0.45, rim='#ff7bd5', spec=0.6, tex=0.3, rnd=rnd)
    hexi = a.poly(ngon(cx, cy, s * 0.62, 6, math.radians(30)))
    a.solid(hexi, DARK, bevel=s * 0.05, chrome=0.2, light=(0.5, 0.6, 0.6), spec=0.3)          # (a recess: lit from below)
    eye_m = a.ell(cx, cy, s * 0.4)
    a.glow(eye_m, C(eye), s * 0.25, 1.2)
    t = np.clip(np.sqrt((a.xx - cx) ** 2 + (a.yy - cy) ** 2) / (s * 0.4), 0, 1)[..., None]
    a.fill(eye_m, C('#fff4c2') * (1 - t) ** 1.5 + C(eye) * (1 - (1 - t) ** 1.5))
    for p0, p1 in (((cx - s * 0.3, cy), (cx + s * 0.3, cy)), ((cx, cy - s * 0.3), (cx, cy + s * 0.3))):
        a.add(a.lines([p0, p1], s * 0.05), C('#3a0500'), -0.7)            # (the game's + in the eye: a dark reticle)
    a.flare(cx - s * 0.12, cy - s * 0.12, s * 0.14, '#fff2d0', 0.8)


def cross_walker(a, cx, cy, s, rnd, eye='#ff2a2a', phase=0.0):
    """the Cross: a ball-bodied droid on four legs splayed in an X"""
    a.shadow(a.ell(cx, cy + s * 1.05, s * 0.9, s * 0.18), 0, 0, s * 0.12, 0.55)
    legs = []
    for i, ang in enumerate((-2.3, -0.84, 2.3, 0.84)):
        sw = math.sin(phase + i * 1.7) * 0.12
        kx = cx + math.cos(ang + sw) * s * 0.78
        ky = cy + math.sin(ang + sw) * s * 0.5 - s * 0.2
        fx = cx + math.cos(ang + sw) * s * 1.05
        fy = cy + s * 1.0 - (0.0 if ang > 0 else s * 0.05)
        legs.append(((cx, cy), (kx, ky), (fx, fy)))
    back = [legs[0], legs[2]]; front = [legs[1], legs[3]]
    for lg in back:
        m = a.lines(lg, s * 0.17)
        a.solid(m, '#4a5163', bevel=s * 0.03, chrome=0.4, rim='#ff9be0')
    body = a.ell(cx, cy, s * 0.55)
    a.solid(body, '#8d97ad', bevel=s * 0.12, chrome=0.6, rim='#ff7bd5', spec=0.8, tex=0.2, rnd=rnd)
    band = a.ell(cx, cy, s * 0.56, s * 0.11)
    a.solid(band * (a.yy > cy - 2), '#30364a', bevel=2)
    for lg in front:
        m = a.lines(lg, s * 0.19)
        a.solid(m, '#6d768c', bevel=s * 0.035, chrome=0.55, rim='#ff9be0', spec=0.7)
        a.solid(a.ell(*lg[1], s * 0.1), '#aab3c7', bevel=2.5, spec=0.9)  # (knee joints)
    visor = a.ell(cx, cy - s * 0.12, s * 0.34, s * 0.1)
    a.glow(visor, C(eye), s * 0.22, 2.6)
    a.fill(visor, C('#e8180c'))
    a.add(a.ell(cx, cy - s * 0.12, s * 0.22, s * 0.035), C('#fff0c8'), 0.95)   # (its hot core)


def fighter(a, cx, cy, s, rnd, tilt=0.55):
    """your ship: an octagonal fighter, seen from above and behind, its core glowing"""
    a.glow(a.ell(cx, cy + s * 0.15, s * 1.1, s * 0.6 * tilt), C('#3ad7ff'), s * 0.35, 0.5)
    hull = a.poly(ngon(cx, cy, s, 8, math.radians(22.5), sy=tilt))
    a.shadow(hull, 0, s * 0.6, s * 0.2, 0.5)
    a.solid(hull, '#c9d4e8', bevel=s * 0.12, chrome=0.7, sky=('#1a1440', '#7fe3ff'), ground=('#1a0a20', '#ff8ad8'),
            rim='#7fe3ff', spec=0.9, tex=0.15, rnd=rnd)
    ring = a.poly(ngon(cx, cy, s * 0.72, 8, math.radians(22.5), sy=tilt)) - a.poly(ngon(cx, cy, s * 0.64, 8, math.radians(22.5), sy=tilt))
    a.add(np.clip(ring, 0, 1), C('#203048'), -0.6)
    dome = a.ell(cx, cy - s * 0.18 * tilt, s * 0.34, s * 0.34 * tilt * 1.3)
    a.glow(dome, C('#3ad7ff'), s * 0.12, 0.9)
    a.solid(dome, '#3fa8e8', bevel=s * 0.14, amb=0.45, chrome=0.6, sky=('#1a3a80', '#d8fbff'), ground=('#0a2050', '#5fd0ff'), spec=1.2, shin=40)
    for side in (-1, 1):                                                    # (twin cannons)
        m = a.lines([(cx + side * s * 0.55, cy - s * 0.05), (cx + side * s * 0.62, cy - s * 0.55 * tilt - s * 0.25)], s * 0.08)
        a.solid(m, '#7d889e', bevel=2, chrome=0.5, spec=0.8)
    a.glow(a.ell(cx, cy + s * 0.55 * tilt, s * 0.3, s * 0.08), C('#5ff0ff'), s * 0.12, 2.0)


def human(a, x, y, h, col='#0c0a14', rim='#ffb36b', run=0.0):
    """a fleeing human: a dark painted figure with the sunset on its edge"""
    hd = a.ell(x, y - h * 0.86, h * 0.09)
    tor = a.poly([(x - h * 0.1, y - h * 0.74), (x + h * 0.1, y - h * 0.74), (x + h * 0.07, y - h * 0.42), (x - h * 0.07, y - h * 0.42)])
    l1 = a.lines([(x, y - h * 0.44), (x - h * 0.16 - run * h * 0.1, y - h * 0.2), (x - h * 0.22, y)], h * 0.07)
    l2 = a.lines([(x, y - h * 0.44), (x + h * 0.12, y - h * 0.22), (x + h * 0.24 + run * h * 0.1, y - h * 0.08)], h * 0.07)
    ar = a.lines([(x - h * 0.08, y - h * 0.7), (x - h * 0.24, y - h * 0.55), (x - h * 0.3, y - h * 0.66)], h * 0.05)
    ar2 = a.lines([(x + h * 0.08, y - h * 0.7), (x + h * 0.25, y - h * 0.78), (x + h * 0.34, y - h * 0.9)], h * 0.05)
    m = np.clip(hd + tor + l1 + l2 + ar + ar2, 0, 1)
    a.shadow(a.ell(x, y, h * 0.25, h * 0.04), 0, 0, 3, 0.5)
    a.solid(m, col, bevel=2, amb=0.6, spec=0.1, rim=rim, rim_w=2.5, light=(0.8, -0.3, 0.5))


# ------------------------------------------------------------------ the box
def scene_guardian(W, H, rnd):
    a = Art(W, H)
    hz = int(H * 0.60)
    a.vgrad([(0, '#07031a'), (0.45, '#2a0b52'), (0.8, '#8a1f78'), (1.0, '#ff6a3d')], 0, hz)
    a.nebula(rnd, '#5a2ad8', 0.45, 50, region=np.clip(1 - a.yy / hz, 0, 1))
    a.nebula(rnd, '#ff3aa8', 0.25, 30, region=np.clip(1 - a.yy / hz, 0, 1) ** 2)
    a.stars(rnd, 650, (0, 0, W, int(hz * 0.8)))
    pl = a.ell(W * 0.16, H * 0.17, W * 0.07)                               # (a ringed planet, low in the corner)
    a.solid(pl, '#c86a3a', bevel=W * 0.03, amb=0.15, spec=0.15, light=(0.7, -0.4, 0.5))
    a.add(np.clip(a.lines([(W * 0.06, H * 0.19), (W * 0.27, H * 0.145)], 3) - pl * 0.0, 0, 1), C('#ffd8a8'), 0.7)
    a.sun(W * 0.5, hz - W * 0.02, W * 0.26, horizon=hz)
    mm = a.mountains(rnd, hz + 2, H * 0.03, H * 0.09, '#1a0830', edge='#ff5fae', n=7)
    a.vgrad([(0, '#1a0430'), (1, '#05010c')], hz, H, m=(a.yy >= hz).astype(np.float32))
    a.grid(hz, W * 0.5, '#ff3ad6', n_v=18, n_h=12, w=1.8, k=0.9, glow=4)
    a.glow((a.yy > hz - 3).astype(np.float32) * (a.yy < hz + 3), C('#ff9a5a'), 6, 0.6)   # (the horizon's line of light)
    guardian(a, W * 0.5, H * 0.33, W * 0.2, rnd)
    for i, (x, y, s) in enumerate([(0.17, 0.74, 0.075), (0.31, 0.70, 0.055), (0.80, 0.72, 0.065), (0.67, 0.67, 0.045),
                                   (0.42, 0.665, 0.04), (0.9, 0.82, 0.09)]):
        cross_walker(a, W * x, H * y, W * s, rnd, phase=i * 1.3)
    for x, y, h in ((0.55, 0.82, 0.11), (0.62, 0.80, 0.09)):
        human(a, W * x, H * y, H * h, run=0.5)
    sx, sy = W * 0.30, H * 0.88
    a.beam((sx - W * 0.04, sy - H * 0.05), (W * 0.465, H * 0.36), '#ff3060', w=4, g=6)
    a.beam((sx + W * 0.03, sy - H * 0.06), (W * 0.52, H * 0.37), '#ff3060', w=4, g=6)
    a.burst(W * 0.49, H * 0.365, W * 0.045, rnd)
    a.burst(W * 0.80, H * 0.69, W * 0.05, rnd, cols=('#ffffff', '#fff07a', '#ff9a2a', '#d81b60'))
    fighter(a, sx, sy, W * 0.15, rnd)
    a.vignette(0.45)
    a.grain(rnd, 0.03)
    return a


def box_front(path):
    rnd = random.Random(2084)
    W, H = 1000, 1320
    a = Art(W, H, '#050505')
    for i, c in enumerate(('#ffd23f', '#ff8a1f', '#ff3d2e', '#c2185b')):    # (the stripes across the top)
        y = 18 + i * 11
        a.fill(a.rect(0, y, W, y + 7), C(c))
    a.chrome_title('LAST HUMAN', W / 2, 150, 150, shear=-0.22, sx=0.92, depth=12)
    sw, sh = W - 70, 900
    scene = scene_guardian(sw, sh, rnd)
    x0, y0 = 35, 250
    frame = a.rect(x0 - 6, y0 - 6, x0 + sw + 6, y0 + sh + 6, r=10)
    a.fill(frame, C('#d83a2a'))
    a.img[y0:y0 + sh, x0:x0 + sw] = scene.img
    a.fill(a.text_mask('VIDEO GAME CARTRIDGE', 'ariblk.ttf', 30, 40, 1210, anchor='lm'), C('#f2f2f2'))
    a.fill(a.text_mask('FOR THE VECTREX ARCADE SYSTEM', 'bahnschrift.ttf', 22, 40, 1250, anchor='lm'), C('#bdbdbd'))
    a.fill(a.text_mask('1 PLAYER', 'ariblk.ttf', 30, W - 40, 1210, anchor='rm'), C('#ffd23f'))
    a.fill(a.text_mask('70 LEVELS  ·  2 ARENAS', 'bahnschrift.ttf', 22, W - 40, 1250, anchor='rm'), C('#ff8a1f'))
    for i, c in enumerate(('#c2185b', '#ff3d2e', '#ff8a1f', '#ffd23f')):
        y = 1278 + i * 9
        a.fill(a.rect(0, y, W, y + 5), C(c))
    a.save(path)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    box_front(os.path.join(OUT, 'box_front.png'))
    print('box front done')
