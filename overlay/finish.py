"""finish.py ART.png [OUT.png] - turn artwork made on the template (by an artist or an image generator) into the
Last Human overlay: scaled to the sheet (846 x 1080, cropped to 162:207 if needed), the play window and the HUD boxes
cut out exactly (whatever was painted there is dropped), the see-through colour filters put back (field blue, score
gold, level white, lives red, bombs green, cards white), the sheet's rounded corners. Default OUT: overlay.png
is NOT touched - writes ART_overlay.png next to ART unless OUT is given."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, RAD, FILT = 846, 1080, 7, 70
FIELD = (70, 150, 255)
lay = json.load(open(os.path.join(HERE, 'layout5.json')))
COLS = [(255, 190, 40), (255, 255, 255), (255, 50, 40), (60, 255, 90), (255, 255, 255)]
src = Image.open(sys.argv[1]).convert('RGB')
r = W / H
if abs(src.width / src.height - r) > 0.002:                   # crop to the sheet's shape, centred
    if src.width / src.height > r:
        w = round(src.height * r); x = (src.width - w) // 2; src = src.crop((x, 0, x + w, src.height))
    else:
        h = round(src.width / r); y = (src.height - h) // 2; src = src.crop((0, y, src.width, y + h))
art = src.resize((W, H), Image.LANCZOS).convert('RGBA')
art_mask = Image.open(os.path.join(HERE, 'mask_4x.png')).convert('L').resize((W, H), Image.LANCZOS)   # white = printed
ov = Image.new('RGBA', (W, H), FIELD + (FILT,)); d = ImageDraw.Draw(ov)
for (x0, y0, x1, y1), c in zip(lay['top'] + lay['bottom'], COLS):
    d.rounded_rectangle([x0, y0, x1, y1], radius=RAD, fill=c + (FILT,))
out = Image.composite(art, ov, art_mask)
corners = Image.new('L', (W * 4, H * 4), 0); ImageDraw.Draw(corners).rounded_rectangle([0, 0, W * 4 - 1, H * 4 - 1], radius=64, fill=255)
out.putalpha(ImageChops.multiply(out.split()[3], corners.resize((W, H), Image.LANCZOS)))
dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(sys.argv[1])[0] + '_overlay.png'
out.save(dst); print('saved', dst)
