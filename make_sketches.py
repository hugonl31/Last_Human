"""make_sketches.py - the Last Human page's robot sketches, drawn from the game's own vector shapes (tools/genart.py).

Two pictures a robot: a pencil design sheet on graph paper (img/sketch/NAME.svg) and the shape as it glows on the
Vectrex screen (img/screen/NAME.svg).    python site/make_sketches.py
"""
import math, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import genart                                                   # noqa: E402

S, S2 = genart.SHAPES, genart.SHAPES2
OUT = os.path.join(ROOT, 'site', 'img')
HAND = "'Segoe Print', 'Bradley Hand', 'Comic Sans MS', cursive"
UNIT = 1.0                                                      # (the shapes are in game pixels)


def shp(name):
    return S.get(name) or S2[name]


def moved(strokes, dx, dy):
    return [[(x + dx, y + dy) for x, y in s] for s in strokes]


COMPOSITES = {
    '_guard': lambda: S['guard_core'] + sum((S['plate%d' % i] for i in range(8)), []),
    '_ovr': lambda: S['ovr_body'] + moved(S['ovr_eye0'], -6, 0) + moved(S['ovr_eye0'], 6, 0),
    '_hydra': lambda: S2['hyd0'] + moved(S2['hseg0'], -15, -8) + moved(S2['hseg1'], -26, -14),
    '_cent': lambda: moved(S2['chead'], 9, 0) + S2['cseg'] + moved(S2['cseg'], -8, 0),
    '_fence': lambda: moved(S2['post0'], -10, 0) + moved(S2['post0'], 10, 0) + [[(-7, 0), (7, 0)]],
    '_split': lambda: moved(S2['split0'], -7, 0) + moved(S2['shard0'], 7, 3) + moved(S2['shard0'], 7, -3),
}

# (key, shapes, name, one-line note on the sheet)
ROBOTS = [
    ('player', ['player'], 'The fighter', 'your ship: 8-way fire, 1 bomb'),
    ('human', ['hum_a0', 'hum_b0', 'hum_c0'], 'The humans', 'save them: 1,000 .. 5,000'),
    ('cross', ['grunt0'], 'Cross', 'foot soldier, 1 hit'),
    ('hulk', ['hulk0'], 'Hulk', 'indestructible, shots push it'),
    ('bowtie', ['fly0'], 'Small bowtie', 'flaps, aimed shots, 2 hits'),
    ('strongbow', ['diab0'], 'Strong bowtie', '20 hits, leads its double shots'),
    ('killer', ['enf0'], 'Killer', 'homing dart, built by Spheroids'),
    ('brain', ['brain0'], 'Brain', '3 hits, turns humans into Progs'),
    ('prog', ['prog0'], 'Prog', 'a human, turned'),
    ('spheroid', ['sph2'], 'Spheroid', 'builds Killers, flees'),
    ('quark', ['qrk0'], 'Quark', 'builds Tanks, flees'),
    ('tank', ['tank0'], 'Tank', '5 hits, bouncing shells'),
    ('layer', ['layer0'], 'Mine layer', '3 hits, drops 7 electrodes'),
    ('electrode', ['elec0'], 'Electrode', 'a mine'),
    ('praetorian', ['praet0'], 'Praetorian', 'elite guard, 4 hits'),
    ('guardian', ['_guard'], 'The Guardian', 'boss: 8 plates, then the core'),
    ('overseer', ['_ovr'], 'The Overseer', 'final boss of Arena 1, 6 phases'),
    ('splitter', ['_split'], 'Splitter', 'bursts into two homing shards'),
    ('shieldbot', ['shld0'], 'Shield bot', 'shield at the front: flank it'),
    ('phaser', ['phas0'], 'Phaser', 'phases out, reappears beside you'),
    ('sniper', ['snip0'], 'Sniper', 'aiming line, then a fast shot'),
    ('orbiter', ['orb0'], 'Orbiter', 'circles your ship'),
    ('fence', ['_fence'], 'Laser fence', 'lit 2.6 s, dark 1.4 s'),
    ('centipede', ['_cent'], 'Centipede', 'split it by the middle'),
    ('hydra', ['_hydra'], 'The Hydra', 'boss: only the tail ring takes hits'),
    ('architect', ['arch0'], 'The Architect', 'final boss: fences, teleports'),
]


def strokes_of(names):
    """the shapes side by side, in art units (y up), with their extents"""
    groups = []
    for nm in names:
        st = COMPOSITES[nm]() if nm in COMPOSITES else shp(nm)
        pts = [p for s in st for p in s]
        groups.append((st, min(x for x, y in pts), max(x for x, y in pts), min(y for x, y in pts), max(y for x, y in pts)))
    gap = 6
    total = sum(g[2] - g[1] for g in groups) + gap * (len(groups) - 1)
    x = -total / 2
    out = []
    for st, x0, x1, y0, y1 in groups:
        out.append(moved(st, x - x0, -(y0 + y1) / 2))
        x += (x1 - x0) + gap
    allp = [p for st in out for s in st for p in s]
    return out, max(max(abs(px) for px, py in allp), 1), max(max(abs(py) for px, py in allp), 1)


def pencil(strokes, cx, cy, k, rnd, col='#2d2a26'):
    out = []
    for s in strokes:
        if len(s) == 1:
            x, y = s[0]
            out.append(f'<circle cx="{cx + x * k:.1f}" cy="{cy - y * k:.1f}" r="2.2" fill="{col}" opacity="0.7"/>')
            continue
        for p in range(3):                                  # (three light passes, each a little off: a pencil line)
            ox, oy = rnd.uniform(-0.9, 0.9), rnd.uniform(-0.9, 0.9)
            pts = ' '.join(f'{cx + x * k + ox + rnd.uniform(-0.5, 0.5):.1f},{cy - y * k + oy + rnd.uniform(-0.5, 0.5):.1f}'
                           for x, y in s)
            op = (0.55, 0.35, 0.25)[p]
            out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{1.5 - p * 0.3:.1f}" '
                       f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')
    return ''.join(out)


def sketch(key, names, title, note, n):
    rnd = random.Random(key)
    W, H = 340, 280
    st, ex, ey = strokes_of(names)
    k = min(120 / ex, 85 / ey, 9.0)
    cx, cy = W / 2, 132
    grid = []
    for x in range(0, W + 1, 10):
        grid.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#9cc3e6" stroke-width="{0.9 if x % 50 == 0 else 0.4}" opacity="0.6"/>')
    for y in range(0, H + 1, 10):
        grid.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#9cc3e6" stroke-width="{0.9 if y % 50 == 0 else 0.4}" opacity="0.6"/>')
    r = max(ex, ey) * k * 1.12
    wpx = ex * 2 / UNIT
    con = (f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="#c0392b" stroke-width="0.8" stroke-dasharray="4 3" opacity="0.55"/>'
           f'<line x1="{cx - r - 12:.1f}" y1="{cy}" x2="{cx + r + 12:.1f}" y2="{cy}" stroke="#c0392b" stroke-width="0.6" stroke-dasharray="6 2 1 2" opacity="0.5"/>'
           f'<line x1="{cx}" y1="{cy - r - 12:.1f}" x2="{cx}" y2="{cy + r + 12:.1f}" stroke="#c0392b" stroke-width="0.6" stroke-dasharray="6 2 1 2" opacity="0.5"/>')
    dy = cy + ey * k + 22                                  # (a dimension line under the drawing: its width on the screen)
    x0, x1 = cx - ex * k, cx + ex * k
    dim = (f'<line x1="{x0:.1f}" y1="{dy:.1f}" x2="{x1:.1f}" y2="{dy:.1f}" stroke="#2d2a26" stroke-width="0.8" opacity="0.6"/>'
           f'<line x1="{x0:.1f}" y1="{dy - 5:.1f}" x2="{x0:.1f}" y2="{dy + 5:.1f}" stroke="#2d2a26" stroke-width="0.8" opacity="0.6"/>'
           f'<line x1="{x1:.1f}" y1="{dy - 5:.1f}" x2="{x1:.1f}" y2="{dy + 5:.1f}" stroke="#2d2a26" stroke-width="0.8" opacity="0.6"/>'
           f'<text x="{cx}" y="{dy - 4:.1f}" font-family="{HAND}" font-size="10" fill="#2d2a26" text-anchor="middle" opacity="0.8">'
           f'{wpx:.0f} px</text>')
    txt = (f'<text x="14" y="26" font-family="{HAND}" font-size="17" fill="#1d1b18" font-weight="bold">{title}</text>'
           f'<text x="{W - 12}" y="24" font-family="{HAND}" font-size="10" fill="#7a6f5f" text-anchor="end">sheet {n:02d}</text>'
           f'<text x="14" y="{H - 14}" font-family="{HAND}" font-size="12" fill="#3b3631">{note}</text>')
    paper = (f'<defs><radialGradient id="p" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#fbf6e9"/>'
             f'<stop offset="1" stop-color="#e9dfc6"/></radialGradient></defs><rect width="{W}" height="{H}" fill="url(#p)"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{paper}'
           f'{"".join(grid)}{con}{pencil([s for g in st for s in g], cx, cy, k, rnd)}{dim}{txt}'
           f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="#b9ab8c"/></svg>')
    open(os.path.join(OUT, 'sketch', key + '.svg'), 'w', encoding='utf-8').write(svg)


def screen(key, names):
    W, H = 200, 150
    st, ex, ey = strokes_of(names)
    k = min(70 / ex, 48 / ey, 6.0)
    cx, cy = W / 2, H / 2
    lines = []
    for s in [s for g in st for s in g]:
        if len(s) == 1:
            x, y = s[0]
            lines.append(f'<circle cx="{cx + x * k:.1f}" cy="{cy - y * k:.1f}" r="1.8" fill="#e6f3ff"/>')
        else:
            pts = ' '.join(f'{cx + x * k:.1f},{cy - y * k:.1f}' for x, y in s)
            lines.append(f'<polyline points="{pts}" fill="none" stroke="#e6f3ff" stroke-width="1.6" '
                         f'stroke-linecap="round" stroke-linejoin="round"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           '<defs><filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.2" result="a"/>'
           '<feGaussianBlur in="SourceGraphic" stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="a"/>'
           '<feMergeNode in="SourceGraphic"/></feMerge></filter>'
           '<radialGradient id="t" cx="50%" cy="50%" r="70%"><stop offset="0" stop-color="#0c1220"/><stop offset="1" stop-color="#020306"/></radialGradient></defs>'
           f'<rect width="{W}" height="{H}" rx="14" fill="url(#t)"/><g filter="url(#g)">{"".join(lines)}</g></svg>')
    open(os.path.join(OUT, 'screen', key + '.svg'), 'w', encoding='utf-8').write(svg)


def main():
    for d in ('sketch', 'screen'):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for n, (key, names, title, note) in enumerate(ROBOTS, 1):
        sketch(key, names, title, note, n)
        screen(key, names)
    print(len(ROBOTS), 'robots drawn')


if __name__ == '__main__':
    main()
