# Last Human overlay: template and brief

A Vectrex screen overlay is a printed, partly see-through plastic sheet laid over the tube. This folder has the
exact layout of the Last Human overlay, so new artwork can be painted for it. The main page
([../README.md](../README.md)) shows the game, its robots, its screenshots and the box-art style.

## The sheet

* **162 x 207 mm, portrait.** The images here are 846 x 1080 px, and 4x that (3384 x 4320) for painting.
* The middle is a see-through **play window**: the shape of the tube, where the game is visible.
* Five **HUD boxes** sit at the window's top and bottom edges. They are tinted see-through filters over the game's
  status line. Top: the score (gold), the level and time bar (white) and the ships left (red). Bottom: the bombs
  (green) and the power cards (white).
* Everything else is **printed artwork**, an opaque frame around the window: a top band of about 7 % of the height,
  side bands of about 10 % (left) and 8 % (right) of the width, and a bottom band of about 14 %. The corners are
  rounded.

| File | What it is |
|---|---|
| [template_guides_4x.png](template_guides_4x.png) | The labelled guide: artwork area, play window, the five HUD boxes and the tube's glass edge (pink dashed line). |
| [template_clean_4x.png](template_clean_4x.png) | The same without text. **Black = artwork area**, blue = play window, coloured boxes = HUD filters. Use this as the canvas. |
| [mask_4x.png](mask_4x.png) | White = printed artwork, black = see-through. |
| [finish.py](finish.py) | `python finish.py ART.png [OUT.png]` crops and scales finished artwork to the sheet, cuts the window and the boxes exactly, and puts the coloured filters back. |
| [make_template.py](make_template.py), [layout5.json](layout5.json) | How the template is made: the tube outline and the HUD boxes, measured from the game running on the emulator. |
| [current_overlay.png](current_overlay.png) | **The final overlay** (1109 x 1418 px): the arena city at night, the LAST HUMAN logo, the five HUD boxes. |

## Brief

Paint arcade-cabinet side art for **LAST HUMAN**, a Vectrex arena shooter (2084: the robots have turned on their
makers; you are a lone fighter ship saving the last humans).

* **Style:** 1980s arcade cabinet art and comic-book / anime illustration: bold ink outlines, rich colour, dramatic
  airbrushed shading, large recognisable objects with detailed backgrounds. Think of the classic Vectrex overlays
  *Vectorblade* and *Telengard*, and of the box art on the main page. **One continuous illustration, no repeating
  tiles, no pixel art.**
* **Subjects:** the robots of the game (see the sketches and real-life paintings on the main page): the Guardian, the
  Overseer, Hulks, Brains, Cross walkers, Tanks, the Hydra. They loom over the corners, their arms reaching down the
  sides. Below them: a landscape, a city skyline or arena stands with a crowd, floodlights, laser beams, explosions. A
  night sky with stars and planets at the top.
* **Title marquee at the bottom:** a great-looking **LAST HUMAN** logo in the bottom band, where there is the most
  room, with the background artwork continuing behind it, not on a plain plate.
* **Colour:** darker tones overall, with bright highlights for depth and 3D shading. Next to the window keep it fairly
  dark, so the bright game lines stand out.
* **The edge of the window:** make a smooth transition from the frame into the play area, as if the scene continues
  into it and fades out, rather than a hard cut. The window itself is cut away by `finish.py`, so anything painted
  inside it disappears; paint up to the edge and let it fade.
* Paint only in the black area of `template_clean_4x.png`. Leave the blue window and the five coloured boxes empty;
  paint there is cut away anyway.
* Art outside the pink dashed line (the glass edge) still shows on the printed sheet. It just lies over the dark
  surround of the tube.
