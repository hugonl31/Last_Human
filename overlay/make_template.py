"""make_template.py - Last Human overlay TEMPLATE for an artist / image generator (2026-10-28).

The overlay sheet is 162 x 207 mm (846 x 1080 px in the emulator). Outputs (this folder, each at 1x and 4x):
  template_guides*.png  - labelled: artwork area, play window, HUD boxes with their names and colours, the glass edge
  template_clean*.png   - the same without text or guides: black artwork area, window and boxes as flat colours
  mask*.png             - white = artwork (printed), black = window (see-through); to cut finished art
Geometry from layout5.json (the measured tube, the HUD boxes centred on their items)."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r'G:\AI\Vectrex_EMU\src\frontend')
import vecrender as V
W, H, RAD = 846, 1080, 7
lay = json.load(open(os.path.join(HERE, 'layout5.json')))
T, B = lay['top'], lay['bottom']
NAMES = [('SCORE', (255, 190, 40)), ('LEVEL + TIME', (235, 235, 235)), ('LIVES', (255, 60, 50)),
         ('BOMBS', (60, 230, 90)), ('POWER CARDS', (235, 235, 235))]
BOXES = T + B

def window(S):
    m = Image.new('L', (W * S, H * S), 0); d = ImageDraw.Draw(m)
    win = [tuple(p) for p in lay['play_top']] + [tuple(p) for p in lay['play_r']][::-1] + \
          [tuple(p) for p in lay['play_bot']][::-1] + [tuple(p) for p in lay['play_l']]
    d.polygon([(x * S, y * S) for x, y in win], fill=255)
    ptop = max(p[1] for p in lay['play_top']) + 6; pbot = min(p[1] for p in lay['play_bot']) - 6
    for b in T:
        d.rounded_rectangle([b[0] * S, b[1] * S, b[2] * S, ptop * S], radius=RAD * S, fill=255)
    for b in B:
        d.rounded_rectangle([b[0] * S, pbot * S, b[2] * S, b[3] * S], radius=RAD * S, fill=255)
    from scipy import ndimage
    a = np.array(m) > 127; R = 6 * S
    a = ndimage.distance_transform_edt(~a) <= R
    a = ndimage.distance_transform_edt(a) > R
    return Image.fromarray((a * 255).astype(np.uint8), 'L')

def sheet_corners(S):
    m = Image.new('L', (W * S, H * S), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, W * S - 1, H * S - 1], radius=16 * S, fill=255)
    return m

def glass_outline(S):
    """the tube's glass edge on the sheet (the glass is centred on the frame)"""
    import math
    G = V.GLASS_LUT; pts = []
    for k in range(361):
        a = math.radians(k); i = min(90, int(round(abs(math.degrees(math.atan2(abs(math.sin(a)), abs(math.cos(a))))))))
        r = G[i]
        sx, sy = r * math.cos(a), r * math.sin(a)
        pts.append(((W / 2 + sx / V.ART_AW * W / 2) * S, (H / 2 + sy / V.ART_TUBE_K * H / 2) * S))
    return pts

def build(S):
    win = window(S); corners = sheet_corners(S)
    font = lambda sz: ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', int(sz * S))
    # ---- clean
    im = Image.new('RGB', (W * S, H * S), (0, 0, 0))
    im.paste((40, 70, 120), (0, 0), win)
    d = ImageDraw.Draw(im)
    for (x0, y0, x1, y1), (n, c) in zip(BOXES, NAMES):
        d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=RAD * S, fill=c)
    clean = im.copy(); clean.putalpha(corners)
    # ---- guides
    g = Image.new('RGB', (W * S, H * S), (28, 28, 34))
    gd = ImageDraw.Draw(g)
    step = 20 * S                                                     # (a faint grid on the artwork area)
    for x in range(0, W * S, step):
        gd.line([(x, 0), (x, H * S)], fill=(38, 38, 46), width=1)
    for y in range(0, H * S, step):
        gd.line([(0, y), (W * S, y)], fill=(38, 38, 46), width=1)
    g.paste((40, 70, 120), (0, 0), win)
    gd = ImageDraw.Draw(g)
    edge = ImageChops.subtract(win.filter(ImageFilter.MaxFilter(2 * S + 1)), win)
    g.paste((255, 255, 255), (0, 0), edge)
    for (x0, y0, x1, y1), (n, c) in zip(BOXES, NAMES):
        gd.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=RAD * S, fill=c, outline=(255, 255, 255), width=S)
        f = font(11 if len(n) < 9 else 10)
        tw = gd.textlength(n, font=f)
        gd.text(((x0 + x1) / 2 * S - tw / 2, (y0 + y1) / 2 * S - 8 * S), n, font=f, fill=(0, 0, 0))
    gl = glass_outline(S)
    for i in range(0, len(gl) - 1, 2):
        gd.line([gl[i], gl[i + 1]], fill=(255, 120, 200), width=max(1, S))
    def label(txt, cx, cy, sz, col=(255, 255, 255)):
        f = font(sz)
        for k, line in enumerate(txt.split('\n')):
            tw = gd.textlength(line, font=f)
            gd.text((cx * S - tw / 2, (cy + k * sz * 1.3) * S), line, font=f, fill=col)
    label('PLAY WINDOW - see-through\n(the game is drawn here: no artwork)', W / 2, 470, 22, (200, 220, 255))
    label('the coloured boxes are see-through colour filters over the HUD:\nkeep them clear, same place, size and colour', W / 2, 560, 14, (200, 220, 255))
    label('ARTWORK\n(printed,\nopaque)', 44, 470, 12, (230, 230, 230))
    label('ARTWORK', W - 36, 490, 12, (230, 230, 230))
    label('ARTWORK: top band', W / 2, 18, 14, (230, 230, 230))
    label('ARTWORK: bottom band', W / 2, 1040, 14, (230, 230, 230))
    label('pink dashes = the edge of the tube glass (art outside it is still seen on the sheet)', W / 2, 1060, 10, (255, 150, 210))
    label('sheet 162 x 207 mm, rounded corners - 846 x 1080 px', W / 2, 912, 11, (200, 220, 255))
    guides = g.copy(); guides.putalpha(corners)
    mask = Image.eval(win, lambda v: 255 - v)
    mask = ImageChops.multiply(mask, corners)
    suf = '' if S == 1 else '_%dx' % S
    clean.save(os.path.join(HERE, 'template_clean%s.png' % suf))
    guides.save(os.path.join(HERE, 'template_guides%s.png' % suf))
    mask.save(os.path.join(HERE, 'mask%s.png' % suf))
    print('saved', S, flush=True)

if __name__ == '__main__':
    for S in (1, 4):
        build(S)
