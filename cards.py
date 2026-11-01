"""cards.py - Last Human robot portraits 'as they would look in real life', 80s box-art style (paint.py, boxart.py).

    python site/cards.py [key ...]        -> site/img/art/card_KEY.png
"""
import math, os, random, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paint import Art, C, gf                                     # noqa: E402
from boxart import OUT, rot, ngon, guardian, cross_walker, fighter, human   # noqa: E402


def hulk(a, cx, cy, s, rnd):
    """the Hulk: an indestructible armoured brute (the game's square-shouldered shape)"""
    a.shadow(a.ell(cx, cy + s * 1.35, s * 0.9, s * 0.15), 0, 0, s * 0.1, 0.6)
    for side in (-1, 1):                                               # legs and feet
        m = a.rect(cx + side * s * 0.38 - s * 0.17, cy + s * 0.55, cx + side * s * 0.38 + s * 0.17, cy + s * 1.32, r=s * 0.06)
        a.solid(m, '#4d5532', bevel=s * 0.05, chrome=0.25, rim='#ffb36b', spec=0.5, tex=0.35, rnd=rnd)
        f = a.rect(cx + side * s * 0.38 - s * 0.24, cy + s * 1.2, cx + side * s * 0.38 + s * 0.24, cy + s * 1.36, r=s * 0.05)
        a.solid(f, '#3a3f26', bevel=s * 0.03, spec=0.4)
    body = a.rect(cx - s * 0.7, cy - s * 0.55, cx + s * 0.7, cy + s * 0.65, r=s * 0.12)
    a.shadow(body, 6, 10, 10, 0.4)
    a.solid(body, '#6f7a48', bevel=s * 0.12, chrome=0.3, rim='#ffb36b', spec=0.55, tex=0.4, rnd=rnd)
    for i in range(3):                                                 # (armour seams and a hazard stripe)
        y = cy - s * 0.15 + i * s * 0.25
        a.add(a.lines([(cx - s * 0.6, y), (cx + s * 0.6, y)], 2), C('#1d2010'), -0.6)
    chev = a.rect(cx - s * 0.32, cy + s * 0.32, cx + s * 0.32, cy + s * 0.46, r=3)
    a.solid(chev, '#e8b31c', bevel=2, amb=0.6, spec=0.4)
    for i in range(4):
        x = cx - s * 0.28 + i * s * 0.16
        a.fill(a.poly([(x, cy + s * 0.46), (x + s * 0.07, cy + s * 0.32), (x + s * 0.12, cy + s * 0.32), (x + s * 0.05, cy + s * 0.46)]),
               C('#1d1d1d'), 0.85)
    for side in (-1, 1):                                               # shoulders, arms and fists
        arm = a.rect(cx + side * s * 0.78 - s * 0.17, cy - s * 0.35, cx + side * s * 0.78 + s * 0.17, cy + s * 0.75, r=s * 0.08)
        a.solid(arm, '#59613a', bevel=s * 0.07, chrome=0.3, rim='#ffb36b', spec=0.5, tex=0.35, rnd=rnd)
        fist = a.ell(cx + side * s * 0.78, cy + s * 0.85, s * 0.22, s * 0.2)
        a.solid(fist, '#3e4428', bevel=s * 0.08, spec=0.6)
        sh = a.ell(cx + side * s * 0.78, cy - s * 0.42, s * 0.3, s * 0.24)
        a.solid(sh, '#7e8a52', bevel=s * 0.1, chrome=0.35, rim='#ffb36b', spec=0.7)
    head = a.rect(cx - s * 0.26, cy - s * 0.92, cx + s * 0.26, cy - s * 0.5, r=s * 0.08)
    a.solid(head, '#5d6640', bevel=s * 0.06, chrome=0.3, spec=0.6, rim='#ffb36b')
    vis = a.rect(cx - s * 0.2, cy - s * 0.78, cx + s * 0.2, cy - s * 0.7, r=s * 0.03)
    a.glow(vis, C('#5dff6a'), s * 0.1, 2.0)
    a.fill(vis, C('#d8ffd0'))


def brain(a, cx, cy, s, rnd):
    """the Brain: a living brain under a glass dome, on a hovering saucer"""
    a.glow(a.ell(cx, cy + s * 1.2, s * 0.8, s * 0.12), C('#7affc8'), s * 0.15, 0.8)
    for i in range(4):                                                 # tentacles
        x0 = cx + (i - 1.5) * s * 0.28
        pts = [(x0, cy + s * 0.25)] + [(x0 + math.sin(k * 0.9 + i) * s * 0.12, cy + s * 0.25 + k * s * 0.18) for k in range(1, 5)]
        a.solid(a.lines(pts, s * 0.07), '#7a5a8a', bevel=2, chrome=0.3, spec=0.6, rim='#7affc8')
    base = a.ell(cx, cy + s * 0.18, s * 0.9, s * 0.22)
    a.solid(base, '#8f98ae', bevel=s * 0.08, chrome=0.6, rim='#ff9be0', spec=0.8)
    for i in range(7):
        a.glow(a.ell(cx + (i - 3) * s * 0.22, cy + s * 0.24, s * 0.03), C('#ffe066'), s * 0.03, 1.5)
    bm = a.ell(cx, cy - s * 0.25, s * 0.58, s * 0.45) * (a.yy < cy + s * 0.1)
    a.solid(bm, '#e07aa0', bevel=s * 0.1, amb=0.35, spec=0.35, tex=0.6, rnd=rnd, rim='#ffd0e0')
    for k in range(9):                                                 # (its folds)
        y = cy - s * 0.55 + k * s * 0.08
        pts = [(cx - s * 0.5 + j * s * 0.1, y + math.sin(j * 1.3 + k) * s * 0.03) for j in range(11)]
        a.add(a.lines(pts, 1.6) * bm, C('#5a1030'), -0.55)
    a.add(a.lines([(cx, cy - s * 0.68), (cx, cy + s * 0.05)], 2.5) * bm, C('#4a0820'), -0.6)
    dome = a.ell(cx, cy - s * 0.2, s * 0.72, s * 0.62) * (a.yy < cy + s * 0.14)
    a.glow(dome, C('#7affc8'), s * 0.05, 0.25)
    a.add(np.clip(dome - gf(dome, s * 0.05), 0, 1), C('#c8fff0'), 0.9)
    a.add(np.clip(a.ell(cx - s * 0.3, cy - s * 0.5, s * 0.16, s * 0.08) * dome, 0, 1), C('#ffffff'), 0.65)
    for side in (-1, 1):
        a.glow(a.ell(cx + side * s * 0.55, cy + s * 0.13, s * 0.05), C('#ff3030'), s * 0.06, 2.0)


def tank(a, cx, cy, s, rnd):
    """the Tank: tracks, an armoured hull and a turret whose shells bounce off the walls"""
    a.shadow(a.ell(cx, cy + s * 0.72, s * 1.1, s * 0.12), 0, 0, s * 0.1, 0.6)
    tr = a.rect(cx - s * 1.0, cy + s * 0.2, cx + s * 1.0, cy + s * 0.7, r=s * 0.24)
    a.solid(tr, '#2c2f36', bevel=s * 0.08, chrome=0.2, spec=0.4, tex=0.5, rnd=rnd, rim='#ffb36b')
    for i in range(6):
        a.solid(a.ell(cx - s * 0.75 + i * s * 0.3, cy + s * 0.45, s * 0.12), '#7a808e', bevel=s * 0.04, chrome=0.5, spec=0.8)
    hull = a.poly([(cx - s * 0.9, cy + s * 0.22), (cx - s * 0.7, cy - s * 0.18), (cx + s * 0.7, cy - s * 0.18), (cx + s * 0.9, cy + s * 0.22)])
    a.shadow(hull, 4, 8, 8, 0.4)
    a.solid(hull, '#a0482a', bevel=s * 0.08, chrome=0.35, rim='#ffd08a', spec=0.6, tex=0.35, rnd=rnd)
    tur = a.rect(cx - s * 0.38, cy - s * 0.52, cx + s * 0.38, cy - s * 0.14, r=s * 0.1)
    a.solid(tur, '#b3552f', bevel=s * 0.08, chrome=0.4, rim='#ffd08a', spec=0.7)
    gun = a.lines([(cx + s * 0.1, cy - s * 0.42), (cx + s * 0.25, cy - s * 1.05)], s * 0.09)
    a.solid(gun, '#5a5f6c', bevel=2.5, chrome=0.6, spec=0.9)
    a.glow(a.ell(cx + s * 0.26, cy - s * 1.08, s * 0.05), C('#ffcf5a'), s * 0.1, 1.5)
    a.glow(a.rect(cx - s * 0.25, cy - s * 0.4, cx - s * 0.05, cy - s * 0.32), C('#ff3030'), s * 0.04, 2)


def killer(a, cx, cy, s, rnd, ang=-0.5):
    """the Killer: a homing dart, chrome fins and a hot exhaust"""
    pts = rot([(cx + s, cy), (cx - s * 0.6, cy - s * 0.55), (cx - s * 0.3, cy), (cx - s * 0.6, cy + s * 0.55)], cx, cy, ang)
    tail = rot([(cx - s * 0.35, cy)], cx, cy, ang)[0]
    far = rot([(cx - s * 1.8, cy)], cx, cy, ang)[0]
    a.beam(tail, far, '#ff7a1a', w=s * 0.22, core='#fff4c2', g=s * 0.12)
    m = a.poly(pts)
    a.shadow(m, 10, 16, 10, 0.4)
    a.solid(m, '#c8cfdc', bevel=s * 0.12, chrome=0.7, rim='#ff5fd2', spec=1.0)
    eye = rot([(cx + s * 0.45, cy)], cx, cy, ang)[0]
    a.glow(a.ell(*eye, s * 0.07), C('#ff2a2a'), s * 0.08, 2.5)


def spheroid(a, cx, cy, s, rnd):
    """the Spheroid: a pulsing diamond of energy that builds Killers"""
    for r, c in ((1.6, '#ff2fa0'), (1.25, '#ffb13b'), (0.95, '#fff6c8')):
        a.glow(a.poly([(cx, cy - s * r), (cx + s * r * 0.8, cy), (cx, cy + s * r), (cx - s * r * 0.8, cy)]), C(c), s * 0.12, 0.5)
    m = a.poly([(cx, cy - s), (cx + s * 0.8, cy), (cx, cy + s), (cx - s * 0.8, cy)])
    a.solid(m, '#ff4fb8', bevel=s * 0.15, amb=0.5, chrome=0.5, sky=('#3a0a50', '#ffe0ff'), ground=('#300010', '#ff9a3a'), spec=1.2)
    a.flare(cx - s * 0.15, cy - s * 0.3, s * 0.25, '#ffffff', 0.9)
    for k in range(3):                                                 # (a Killer being born beside it)
        killer(a, cx + s * 1.25, cy + s * 0.9, s * 0.35, rnd, ang=-2.2) if k == 0 else None


def overseer(a, cx, cy, s, rnd):
    """the Overseer: the machine that runs the Arena - a wall-sized face, two eyes and a crown"""
    a.glow(a.ell(cx, cy, s * 1.6, s * 0.9), C('#3ad7ff'), s * 0.4, 0.35)
    for i, h in enumerate((0.75, 1.1, 0.75)):
        x = cx + (i - 1) * s * 0.55
        m = a.poly([(x - s * 0.3, cy - s * 0.42), (x, cy - s * 0.42 - s * h), (x + s * 0.3, cy - s * 0.42)])
        a.solid(m, '#c9a23a', bevel=s * 0.06, chrome=0.7, sky=('#2a1040', '#fff2b0'), ground=('#3a1a00', '#ffb347'),
                spec=1.0, rim='#3ad7ff')
    face = a.poly([(cx - s * 1.45, cy + s * 0.15), (cx - s * 1.0, cy - s * 0.5), (cx + s * 1.0, cy - s * 0.5),
                   (cx + s * 1.45, cy + s * 0.15), (cx + s * 0.95, cy + s * 0.75), (cx - s * 0.95, cy + s * 0.75)])
    a.shadow(face, 10, 14, 14, 0.6)
    a.solid(face, '#59627a', bevel=s * 0.12, chrome=0.5, rim='#3ad7ff', spec=0.7, tex=0.35, rnd=rnd)
    for i in range(5):
        y = cy + s * 0.45 + i * s * 0.05
        a.add(a.lines([(cx - s * 0.6, y), (cx + s * 0.6, y)], 2), C('#10141c'), -0.5)
    for side in (-1, 1):
        ex, ey = cx + side * s * 0.55, cy + s * 0.05
        a.solid(a.poly(ngon(ex, ey, s * 0.36, 6)), '#22283a', bevel=s * 0.05, light=(0.5, 0.6, 0.6), spec=0.2)
        e = a.poly(ngon(ex, ey, s * 0.27, 6))
        a.glow(e, C('#2ad8ff'), s * 0.2, 1.4)
        t = np.clip(np.sqrt((a.xx - ex) ** 2 + (a.yy - ey) ** 2) / (s * 0.27), 0, 1)[..., None]
        a.fill(e, C('#e8ffff') * (1 - t) + C('#18a8e8') * t)
        a.add(a.lines([(ex - s * 0.14, ey), (ex + s * 0.14, ey)], s * 0.05), C('#003050'), -0.8)


def hydra(a, cx, cy, s, rnd):
    """the Hydra: a head dragging a chain of rings - only the glowing tail ring can be hurt"""
    path = [(cx - s * 1.55 + k * s * 0.36, cy + math.sin(k * 0.8) * s * 0.35 + s * 0.3) for k in range(7)]
    for k, (x, y) in enumerate(path[:-1]):                             # rings, tail first (behind)
        r = s * (0.22 + 0.03 * k)
        m = np.clip(a.ell(x, y, r, r * 0.85) - a.ell(x, y, r * 0.5, r * 0.42), 0, 1)
        a.shadow(m, 6, 12, 8, 0.35)
        if k == 0:
            a.glow(m, C('#ffd05a'), r * 0.5, 1.2)
        a.solid(m, '#ff9a2a' if k == 0 else '#4f8a5a', bevel=r * 0.25, chrome=0.5, rim='#c8ff7a', spec=0.8, tex=0.3, rnd=rnd)
    hx, hy = path[-1][0] + s * 0.25, path[-1][1] - s * 0.35
    head = a.poly([(hx - s * 0.5, hy + s * 0.35), (hx - s * 0.45, hy - s * 0.3), (hx - s * 0.15, hy - s * 0.5), (hx + s * 0.3, hy - s * 0.5),
                   (hx + s * 0.6, hy - s * 0.2), (hx + s * 0.62, hy + s * 0.4), (hx + s * 0.3, hy + s * 0.15), (hx, hy + s * 0.4),
                   (hx - s * 0.25, hy + s * 0.15)])
    a.shadow(head, 8, 14, 10, 0.5)
    a.solid(head, '#3d6e4a', bevel=s * 0.1, chrome=0.45, rim='#c8ff7a', spec=0.8, tex=0.35, rnd=rnd)
    for ex in (hx - s * 0.12, hx + s * 0.25):
        e = a.poly([(ex, hy - s * 0.25), (ex + s * 0.08, hy - s * 0.15), (ex, hy - s * 0.05), (ex - s * 0.08, hy - s * 0.15)])
        a.glow(e, C('#ff3030'), s * 0.08, 2.2)
        a.fill(e, C('#ffe0d0'))


def architect(a, cx, cy, s, rnd):
    """the Architect: the builder of the Core, a turning diamond in its frame, spanning laser fences"""
    for side in (-1, 1):                                               # (a fence it is building)
        px = cx + side * s * 1.5
        a.solid(a.rect(px - s * 0.07, cy + s * 0.5, px + s * 0.07, cy + s * 1.2, r=s * 0.03), '#9aa3b8', bevel=3, chrome=0.6, spec=0.9)
        a.glow(a.ell(px, cy + s * 0.5, s * 0.08), C('#ff3030'), s * 0.08, 2)
    a.beam((cx - s * 1.5, cy + s * 0.55), (cx + s * 1.5, cy + s * 0.55), '#ff2a4a', w=5, g=8)
    fr = np.clip(a.rect(cx - s * 0.9, cy - s * 0.9, cx + s * 0.9, cy + s * 0.9, r=s * 0.05) -
                 a.rect(cx - s * 0.74, cy - s * 0.74, cx + s * 0.74, cy + s * 0.74, r=s * 0.03), 0, 1)
    a.shadow(fr, 8, 12, 10, 0.5)
    a.solid(fr, '#7d6a9a', bevel=s * 0.05, chrome=0.6, rim='#ff7bd5', spec=0.8, tex=0.2, rnd=rnd)
    d = a.poly(rot([(cx - s * 0.5, cy - s * 0.5), (cx + s * 0.5, cy - s * 0.5), (cx + s * 0.5, cy + s * 0.5), (cx - s * 0.5, cy + s * 0.5)],
                   cx, cy, 0.35))
    a.glow(d, C('#b04aff'), s * 0.2, 0.8)
    a.solid(d, '#c8b8ff', bevel=s * 0.1, chrome=0.65, sky=('#200a40', '#f0e0ff'), ground=('#100020', '#ff7bd5'), spec=1.0)
    a.add(a.lines([(cx - s * 0.3, cy), (cx + s * 0.3, cy)], s * 0.06), C('#ffffff'), 0.9)
    a.add(a.lines([(cx, cy - s * 0.3), (cx, cy + s * 0.3)], s * 0.06), C('#ffffff'), 0.9)
    a.glow(a.ell(cx, cy, s * 0.12), C('#ff5fd2'), s * 0.15, 2.0)


def backdrop(a, kind, rnd):
    W, H = a.W, a.H
    if kind == 'arena':
        hz = int(H * 0.62)
        a.vgrad([(0, '#05031a'), (0.6, '#2a0b52'), (1.0, '#b0307a')], 0, hz)
        a.stars(rnd, 300, (0, 0, W, int(hz * 0.85)))
        a.vgrad([(0, '#1a0430'), (1, '#05010c')], hz, H, m=(a.yy >= hz).astype(np.float32))
        a.grid(hz, W * 0.5, '#ff3ad6', n_v=14, n_h=10, w=1.6, k=0.8)
    elif kind == 'desert':
        hz = int(H * 0.64)
        a.vgrad([(0, '#160a30'), (0.5, '#7a1f5a'), (0.85, '#ff6a3d'), (1.0, '#ffc15a')], 0, hz)
        a.stars(rnd, 160, (0, 0, W, int(hz * 0.4)))
        a.sun(W * 0.62, hz - W * 0.05, W * 0.24, top='#fff27a', bot='#ff3d6a', horizon=hz)
        a.mountains(rnd, hz + 2, H * 0.03, H * 0.1, '#2a0a2a', edge='#ff9a5a', n=5)
        a.vgrad([(0, '#3a1030'), (1, '#0c0410')], hz, H, m=(a.yy >= hz).astype(np.float32))
        a.grid(hz, W * 0.62, '#ff8a3a', n_v=12, n_h=9, w=1.4, k=0.55)
    elif kind == 'factory':
        a.vgrad([(0, '#0a0606'), (0.6, '#3a1206'), (1.0, '#ff6a1a')], 0, H)
        for _ in range(7):                                             # (girders and pipes in the glow)
            x = rnd.uniform(0, W)
            a.fill(a.rect(x, 0, x + rnd.uniform(14, 40), H), C('#120806'), 0.85)
        for _ in range(5):
            y = rnd.uniform(H * 0.1, H * 0.6)
            a.solid(a.rect(-10, y, W + 10, y + rnd.uniform(10, 22), r=8), '#3a2a24', bevel=4, chrome=0.3, spec=0.5)
        a.nebula(rnd, '#ff8a2a', 0.35, 25)
        for _ in range(50):                                            # (sparks)
            x, y = rnd.uniform(0, W), rnd.uniform(H * 0.3, H)
            a.glow(a.lines([(x, y), (x + rnd.uniform(-12, 12), y + rnd.uniform(4, 16))], 1.2), C('#ffd05a'), 2, 1.2)
    elif kind == 'space':
        a.vgrad([(0, '#02020a'), (1, '#0a0624')], 0, H)
        a.nebula(rnd, '#3a5aff', 0.5, 45)
        a.nebula(rnd, '#ff3aa8', 0.35, 30)
        a.stars(rnd, 600)
        a.solid(a.ell(W * 0.82, H * 0.2, W * 0.12), '#3a7ad8', bevel=W * 0.05, amb=0.1, spec=0.2, light=(-0.7, -0.3, 0.5))
    elif kind == 'core':
        a.vgrad([(0, '#020a08'), (0.7, '#0a2a1c'), (1.0, '#1a5a3a')], 0, H)
        a.nebula(rnd, '#2affa0', 0.25, 30)
        for _ in range(9):                                             # (lightning in the dark)
            x = rnd.uniform(0, W)
            pts = [(x, 0)]
            for k in range(8):
                x += rnd.uniform(-30, 30)
                pts.append((x, (k + 1) * H * 0.08))
            a.glow(a.lines(pts, 1.4), C('#9affd8'), 4, 0.6)
        a.grid(int(H * 0.66), W * 0.5, '#2affa0', n_v=14, n_h=10, w=1.4, k=0.5)


def card(path, name, sub, draw, kind, seed, scale, cy):
    rnd = random.Random(seed)
    W, H = 640, 820
    a = Art(W, H, '#000000')
    backdrop(a, kind, rnd)
    draw(a, W / 2, H * cy, W * scale, rnd)
    a.vignette(0.5)
    a.img *= (1 - 0.78 * np.clip((a.yy - (H - 200)) / 70, 0, 1))[..., None]    # (dark under the name plate)
    a.chrome_title(name, W / 2, H - 92, 74 if len(name) <= 9 else int(74 * 9.5 / len(name)), shear=-0.2, sx=0.95, depth=7)
    a.fill(a.text_mask(sub, 'bahnschrift.ttf', 22, W / 2, H - 34), C('#ffd23f'))
    a.fill(np.clip(a.rect(0, 0, W, H) - a.rect(6, 6, W - 6, H - 6, r=14), 0, 1), C('#d83a2a'))
    a.grain(rnd, 0.025)
    a.save(path)


CARDS = [
    ('cross', 'CROSS', 'THE FOOT SOLDIER', lambda a, x, y, s, r: cross_walker(a, x, y, s, r, phase=0.8), 'arena', 1, 0.33, 0.40),
    ('hulk', 'HULK', 'CANNOT BE DESTROYED', hulk, 'desert', 2, 0.3, 0.38),
    ('brain', 'BRAIN', 'IT TURNS HUMANS INTO PROGS', brain, 'space', 3, 0.33, 0.42),
    ('tank', 'TANK', 'SHELLS THAT BOUNCE', tank, 'factory', 4, 0.3, 0.48),
    ('killer', 'KILLER', 'IT HOMES IN ON YOU', killer, 'space', 5, 0.28, 0.42),
    ('spheroid', 'SPHEROID', 'IT BUILDS KILLERS', spheroid, 'factory', 6, 0.2, 0.38),
    ('guardian', 'GUARDIAN', 'BOSS OF LEVELS 20 AND 30', guardian, 'desert', 7, 0.24, 0.4),
    ('overseer', 'OVERSEER', 'THE MACHINE THAT RUNS IT ALL', overseer, 'factory', 8, 0.24, 0.44),
    ('hydra', 'HYDRA', 'ONLY THE TAIL RING TAKES HITS', hydra, 'core', 9, 0.26, 0.4),
    ('architect', 'ARCHITECT', 'BUILDER OF THE CORE', architect, 'core', 10, 0.22, 0.38),
]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:]
    for key, name, sub, fn, kind, seed, sc, cy in CARDS:
        if not which or key in which:
            card(os.path.join(OUT, 'card_%s.png' % key), name, sub, fn, kind, seed, sc, cy)
            print(key, 'done', flush=True)
