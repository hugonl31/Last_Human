<p align="center"><img src="img/art/box_front.png" width="560" alt="Last Human box art: the Guardian looms over the arena, Cross walkers march across the grid and the fighter fires"></p>

<h1 align="center">LAST HUMAN</h1>
<p align="center"><b>An arena shooter for the Vectrex · 70 levels · 2 arenas · 4 bosses</b><br>
<sub>6809 assembly · 64 KiB bank-switched cartridge · optional DS2431 save chip</sub></p>

---

<p align="center"><b><i>The machines took everyone. They missed one.</i></b></p>

The war is over, and the machines won it. They took the cities, and then the people in them. Every human left
alive is a captive now, kept for one thing: the games.

Deep in the machine world the robots run their arenas, dark grids of light where captives are thrown in and hunted
for sport while the machines watch. Nobody has ever walked out of one.

You are the last free human, at the controls of a stolen fighting rig. You break into the games. You kill the robots
before they reach the humans, and you pull the captives out, one person taken back at a time.

**Arena 1** runs through the hunters and the factory to the **Overseer**, the machine that runs the games.
**Arena 2** goes deeper into the machine world: through the Foundry and the Wires, down to the **Heart**.

Clear the last arena and the games are over. **Humanity takes the reins once more.**

Last Human started as a love letter to Williams' *Robotron: 2084* and Thomas Sontowski's *Robot Arena*, and grew
into a full campaign built around what the Vectrex does best: sharp, bright vectors moving fast. Every robot has its
own behaviour, every act changes the rules, and the difficulty is something you choose, not something that just
happens to you.

## Download

**[Last Human v1.3.9](https://github.com/hugonl31/Last_Human/releases/latest)**: the 64 KB cartridge ROM
(`Last_Human.bin`), the screen overlay (`Last_Human_overlay.png`) and the UVMC2 edition (`Last_Human_UVMC2.um2`,
see [below](#uvmc2-edition)). To try it right away, the release also has
[Vectrex_EMU](https://github.com/hugonl31/Vectrex_EMU) for Windows, macOS and Linux, with Last Human and its overlay
already in it.

**New in v1.3.9:** calibrated for a standard Vectrex out of the box: the ship closes and the small text stands
straight with the defaults. Your own console may want a step either way on the CALIBRATION screen (button 1 on the
title): up / down ZERO REF, left / right TEXT.

**v1.3.8:** a faster title screen, and the stick chooses the difficulty (left / right) and the arena (up / down).

On a real Vectrex the ROM needs a cartridge with a 64 KB EPROM banked by PB6, or a flash cartridge that supports
it. Saves need the optional DS2431 chip; without it the game runs the same, without saves.

**Make your own cartridge:** the [64K board](https://github.com/hugonl31/Vectrex_Cart_PCB/tree/main/boards/v1_27c512_64k)
on [Vectrex_Cart_PCB](https://github.com/hugonl31/Vectrex_Cart_PCB) is made for this: a 27C512 EPROM, PB6 bank
switching and a place for the DS2431. It has Gerbers ready to order from a board maker, the parts list, and a
3D-printed shell. Burn `Last_Human.bin` into the EPROM and it plugs into any Vectrex.

**About the emulator:** [Vectrex_EMU](https://github.com/hugonl31/Vectrex_EMU) has the full story: the real tube
look, overlays, the settings, online play, and newer versions.

## UVMC2 edition

**It draws exactly like the cartridge.** The game's own 6809 drawing code runs on the UVMC2, so the
Vectrex gets the very same register writes as from the 6809 cartridge, at the same moments: text, boxes and shapes
look as they do on the cartridge, on every console. (It reads the console's own BIOS at start-up for that; if the
read fails it draws the older way.)

Last Human comes in two editions. The 6809 cartridge is the purist version: the game as it runs on a stock
Vectrex, nothing added. The UVMC2 edition (`Last_Human_UVMC2.um2`) is for the Ultimate Vectrex Multicart 2: the
same game, written again in C, running natively on the cartridge's RP2350 processor. It plays the same game frame
for frame (checked against the 6809 version on more than 170,000 frames), and adds what the 6809 has no room for:

* **Cinematics and music:** short animated story scenes with their own music at the big moments. No spoilers here:
  play it and see.
* **A steady frame rate:** 50 frames a second in play and on every title page, and about 48 even in the busiest levels, where the 6809
  version drops to about 43. The game logic runs on the RP2350, so the Vectrex only draws.
* **Saves on the SD card:** high scores, the Arena 2 unlock and the options.
* **Saved calibration:** hold buttons 2 and 3 while you launch the game: first the UVMC2 calibration screen (every
  UVMC2 game uses it), then the game's own CALIBRATION screen (up / down ZERO REF: until the ships close; left / right TEXT:
  until the small text stands straight), saved with the
  scores.
* **2-player co-op:** press button 1 on the title to choose two players. Player 2 plays on the second controller.
  Each player has their own lives, bombs and power-ups, and the score is the team's. Co-op can also be played
  online with [Vectrex_EMU](https://github.com/hugonl31/Vectrex_EMU).

Copy `Last_Human_UVMC2.um2` to the UVMC2's SD card and start it from the cartridge's menu.
Vectrex_EMU runs it too.

**Resetting every few seconds?** On at least one console the UVMC2 edition restarted by itself on the title.
Since v1.3.6 the UVMC2 SDK's watch for the console's RESET button, the likely cause, is switched off: the game should
now stay up (please tell us if it does not). The console's RESET button then no longer restarts the game; switch the
Vectrex off and on instead.

<p align="center"><img src="img/gif/coop.gif" width="380" alt="Two players on the UVMC2 edition: the cages open, both ships fire into the robots of level 4"><br>
<sub>Two players on the UVMC2 edition. The whole clip with sound, levels 4 to 6:
<a href="https://github.com/hugonl31/Last_Human/releases/download/v1.2/Last_Human_UVMC2_coop.mp4">Last_Human_UVMC2_coop.mp4</a> (66 s).</sub></p>

## Screenshots

Every shot and GIF here was made on **[Vectrex_EMU](https://github.com/hugonl31/Vectrex_EMU)**, the Vectrex emulator with the real tube look: phosphor afterglow, the curved glass, room light and the overlay.

<p align="center">
<img src="img/gif/overseer.gif" width="380" alt="The fighter dodges and fires at the Overseer as it drifts across the arena laying mines">
<img src="img/gif/guardian.gif" width="380" alt="With the overlay: the fighter circles the Guardian, breaking off its armour plates while crosses swarm in"><br>
<sub>Played live: the Overseer on the bare tube, and the Guardian with the overlay, both in evening light.</sub>
</p>

**The same two fights at full size, with sound** (press play):

https://github.com/user-attachments/assets/4b206af0-47f6-42b7-ad2d-a2391636e614

https://github.com/user-attachments/assets/e7de0e81-f87a-4ee3-b5ff-c61b148093c0

**With the overlay**

| | |
|:-:|:-:|
| <img src="img/promo/harvest_overlay_day.png" width="400"><br><sub>Daylight · Level 15: crosses and Hulks close in, a Brain fires a cruise missile</sub> | <img src="img/promo/overseer_overlay_day.png" width="400"><br><sub>Daylight · Level 37: inside the Overseer's spark ring</sub> |
| <img src="img/promo/factory_overlay_evening.png" width="400"><br><sub>Evening · Level 25: a Quark builds Tanks, Killers fire homing arrows</sub> | <img src="img/promo/overseer_overlay_evening.png" width="400"><br><sub>Evening · the Overseer's homing missiles curve after you</sub> |

**The bare tube**

| | |
|:-:|:-:|
| <img src="img/promo/bowties_glass_day.png" width="400"><br><sub>Daylight · Level 13: bowties fire double-dot bullets</sub> | <img src="img/promo/snipers_glass_day.png" width="400"><br><sub>Daylight · Arena 2: a Sniper locks on, laser fences, a centipede</sub> |
| <img src="img/promo/bomb_glass_evening.png" width="400"><br><sub>Evening · Level 27: a bomb's shock wave sweeps the arena</sub> | <img src="img/promo/core_glass_evening.png" width="400"><br><sub>Evening · Arena 2: Orbiters circle the ship, a Splitter bursts</sub> |

**More of the game**

| | | | |
|:-:|:-:|:-:|:-:|
| <img src="img/snaps/title.png" width="190"><br><sub>The title</sub> | <img src="img/snaps/level_intro.png" width="190"><br><sub>Robots caged before the countdown</sub> | <img src="img/snaps/guardian.png" width="190"><br><sub>Level 20: the Guardian</sub> | <img src="img/snaps/quarks.png" width="190"><br><sub>Act III: Quarks build Tanks</sub> |
| <img src="img/snaps/swarm.png" width="190"><br><sub>A swarm ring closing in</sub> | <img src="img/snaps/last_stand.png" width="190"><br><sub>Act IV: everything at once</sub> | <img src="img/snaps/hydra.png" width="190"><br><sub>Arena 2: the Hydra</sub> | <img src="img/snaps/architect.png" width="190"><br><sub>The Architect builds a fence</sub> |

<sub>The GIFs are real play by the game's balancing bot.
The stills are staged: test cartridges freeze a composed moment, drawn by the game's own code.</sub>

**Full size:** the [release](https://github.com/hugonl31/Last_Human/releases/latest) has all 16 screenshots at
1493 x 1865 px (`Last_Human_screenshots.zip`), both gameplay clips as videos with the game's sound
(`Last_Human_guardian.mp4`, `Last_Human_overseer.mp4`) and the board turning (`Last_Human_board_spin.mp4`).

---

## The cartridge

<p align="center">
<img src="img/pcb/board_spin.gif" width="400" alt="The Last Human cartridge board turning: the W27C512 EPROM, the gold LAST HUMAN title on the front, the Vectrex logo on the back">
<img src="img/art/cart_render.jpg" width="400" alt="The Last Human cartridge: a clear amber shell with the LAST HUMAN label, the board visible inside"><br>
<img src="img/art/cart_render_back.jpg" width="400" alt="The Last Human cartridge from the other end: the gold edge fingers through the clear shell, the label on top"><br>
<sub>The cartridge board (KiCad 3D render) and the finished cartridge from both ends.</sub>
</p>

**The board at full size** (press play):

https://github.com/user-attachments/assets/a718eb27-3821-4aa5-8db4-0ca8c197b10e

* **Pure Vectrex.** The game runs on the console's own 6809 at 1.5 MHz with its 1 KB of RAM. No UVMC2, PiTrex or
  other extra hardware: it plugs into any Vectrex like a 1982 cartridge.
* **64 KB, full.** The board carries one W27C512 EPROM, a resistor and a capacitor, plus an optional DS2431 for the
  saves. The VIA's PB6 line drives A15 and switches between the two 32 KB banks. Of the 65,536 bytes, 251 are free
  (99.6 % used): there is no room for another robot, boss or arena.
* **The board:** 54 × 66 mm, two layers, gold (ENIG) edge fingers. The LAST HUMAN title on the front and the Vectrex
  logo on the back are openings in the solder mask, so they come out in gold. The board is based on the open
  [Vectrex_Cart_PCB](https://github.com/hugonl31/Vectrex_Cart_PCB) design.

---

## The robots

**Arena 1**

| | | | | |
|:-:|:-:|:-:|:-:|:-:|
| <img src="img/art/card_cross.png" width="160"><br><sub>Cross</sub> | <img src="img/art/card_hulk.png" width="160"><br><sub>Hulk</sub> | <img src="img/art/card_brain.png" width="160"><br><sub>Brain</sub> | <img src="img/art/card_prog.png" width="160"><br><sub>Prog</sub> | <img src="img/art/card_tank.png" width="160"><br><sub>Tank</sub> |
| <img src="img/art/card_killer.png" width="160"><br><sub>Killer</sub> | <img src="img/art/card_spheroid.png" width="160"><br><sub>Spheroid</sub> | <img src="img/art/card_quark.png" width="160"><br><sub>Quark</sub> | <img src="img/art/card_bowtie.png" width="160"><br><sub>Small bowtie</sub> | <img src="img/art/card_strongbow.png" width="160"><br><sub>Strong bowtie</sub> |
| <img src="img/art/card_layer.png" width="160"><br><sub>Mine layer</sub> | <img src="img/art/card_electrode.png" width="160"><br><sub>Electrode</sub> | <img src="img/art/card_praetorian.png" width="160"><br><sub>Praetorian</sub> | <img src="img/art/card_guardian.png" width="160"><br><sub>The Guardian</sub> | <img src="img/art/card_overseer.png" width="160"><br><sub>The Overseer</sub> |

**Arena 2, The Core**

| | | | | |
|:-:|:-:|:-:|:-:|:-:|
| <img src="img/art/card_splitter.png" width="160"><br><sub>Splitter</sub> | <img src="img/art/card_shieldbot.png" width="160"><br><sub>Shield bot</sub> | <img src="img/art/card_phaser.png" width="160"><br><sub>Phaser</sub> | <img src="img/art/card_sniper.png" width="160"><br><sub>Sniper</sub> | <img src="img/art/card_orbiter.png" width="160"><br><sub>Orbiter</sub> |
| <img src="img/art/card_fence.png" width="160"><br><sub>Laser fence</sub> | <img src="img/art/card_centipede.png" width="160"><br><sub>Centipede</sub> | <img src="img/art/card_hydra.png" width="160"><br><sub>The Hydra</sub> | <img src="img/art/card_architect.png" width="160"><br><sub>The Architect</sub> |  |

## Contents

[Download](#download) · [UVMC2 edition](#uvmc2-edition) · [Screenshots](#screenshots) · [The cartridge](#the-cartridge) · [The robots](#the-robots) · [Features](#features) · [Gameplay](#gameplay) · [The cast](#the-cast) ·
[The bosses](#the-bosses) · [How the robots think](#how-the-robots-think) · [Under the hood](#under-the-hood) ·
[Overlay artwork](overlay/README.md)

---

## Features

* **Two arenas, 70 levels.** Arena 1 is 37 levels in four acts. Finish it to open **Arena 2, The Core**: 33 levels
  with new robots, laser fences, power-ups and dark levels lit only by lightning.
* **Move one way, shoot another.** The four buttons fire in four directions, two neighbouring buttons fire
  diagonally, and holding a button gives autofire. All four at once sets off a bomb.
* **Twenty kinds of robot** that think differently: hunters, cowards, builders, snipers, shield bearers, mine layers,
  centipedes that split in two.
* **Four bosses**, each with phases and its own weak point.
* **Four kinds of level:** elimination, survival against the clock, swarm rings, and boss fights.
* **Three difficulties that change how robots think,** not how much they can take. On HARD they get more turns to
  act - and finishing a campaign on HARD earns a title the cartridge keeps.
* **Saves on the cartridge:** high scores, the Arena 2 unlock, the difficulty and the KING titles, on an optional
  DS2431 chip.
* **Built-in calibration** to straighten the picture of your own Vectrex.

---

## Gameplay

| Control | Action |
|---|---|
| Joystick | Move. Half a push is slow, a full push is full speed (about 3 px a frame). |
| Buttons 1 2 3 4 | Fire left, up, down, right. Two neighbouring buttons fire diagonally. |
| Hold a button | Autofire, about 7 shots a second. A fresh press fires at once. |
| Hold all four | **Bomb**: a shock wave rings out from the ship and sweeps the arena in two seconds. |

On the title, button 2 sets the difficulty (EASY, MEDIUM, HARD) and button 1 opens the calibration screen. Once Arena
1 has been finished, the joystick picks **< ARENA 2 >**. A game starts with 3 ships and 1 bomb.

### The levels

* **Elimination:** destroy every robot - hulks and electrodes excepted. What is left on the clock becomes the time
  bonus. When the clock runs out you still have to finish the job, just without the bonus.
* **Survival:** stay alive until the clock runs out while robots stream in from the edges.
* **Swarm:** a ring of crosses closes in from every side. Swarm crosses take two hits.
* **Boss:** a giant robot with its own weapons and a hit bar under the clock.

Each level opens with its name and a hint while the robots wait in dotted cages. After the countdown the cages drop
and they burst out.

### Humans, ships and points

Saving humans pays in a run: 1,000 points for the first, then 2,000, 3,000, 4,000, and 5,000 for every one after
that. Losing a ship resets the run. Save every human in a level for the **savior bonus** - which is harder than it
sounds, since Hulks trample them and Brains turn them into Progs.

Anything that touches your ship destroys it, and a robot that rams you goes down with you. Extra ships come every
50,000 points on EASY, 100,000 on MEDIUM and 200,000 on HARD, up to 9. A Guardian or a Hydra drops an extra bomb.

### The campaign

**Arena 1** introduces its robots one at a time, mixes them with the ones you know, twists the rules, and ends each act
with a swarm or a boss.

| Act | Levels | |
|---|---|---|
| I · The arena awakens | 1-10 | crosses, hulks, bowties, the first swarm |
| II · The hunters | 11-20 | killers, brains, mine fields; boss: **the Guardian** |
| III · The factory | 21-30 | spheroids, quarks, tanks; the Guardian returns |
| IV · The Overseer | 31-37 | praetorians, everything at once; **the Overseer** |

**Arena 2, The Core** runs in three acts - The Foundry, The Wires, The Heart - and ends with the Hydra and the
Architect.

Finish Arena 1 on HARD to become **KING OF THE ARENA**, and Arena 2 on HARD for **KING OF THE GALAXY**. Finish on EASY
or MEDIUM and the game offers to raise the difficulty for the next run.

---

## The cast

Each robot's vector shape at its real size on screen, in pixels, and as it glows on the tube. Points are EASY /
MEDIUM / HARD. Anything that takes more than one hit flashes when struck and is knocked back 2 px.

### Arena 1

<p><img src="img/sketch/player.svg" width="260" align="left"><img src="img/screen/player.svg" width="130" align="right"><b>The fighter.</b> Fires in 8 directions: shots fly at 6 px a frame for 45 frames, at most 8 at a time. After a lost ship it returns with 2.4 s of safety, and robots near the start point are moved away.</p><br clear="all">

<p><img src="img/sketch/human.svg" width="260" align="left"><img src="img/screen/human.svg" width="130" align="right"><b>Humans</b> wander at about 12 px a second and change direction every second or so.</p><br clear="all">

<p><img src="img/sketch/cross.svg" width="260" align="left"><img src="img/screen/cross.svg" width="130" align="right"><b>Cross</b> · 100 / 150 / 200 · 1 hit. The foot soldier. Each one keeps its own pace, re-rolled now and then, and turns every few tenths of a second: 60 % of the time roughly toward you (exactly, or 45° off), 40 % at random.</p><br clear="all">

<p><img src="img/sketch/hulk.svg" width="260" align="left"><img src="img/screen/hulk.svg" width="130" align="right"><b>Hulk</b> · indestructible. Plods at half a pixel a step and, three times in four, heads for the nearest human. Your shots shove it 3 px and break its plans. Only a bomb kills it, and no level requires it.</p><br clear="all">

<p><img src="img/sketch/bowtie.svg" width="260" align="left"><img src="img/screen/bowtie.svg" width="130" align="right"><b>Small bowtie</b> · 200 / 300 / 400 · 2 hits. Alternates fast flapping and slow gliding, turns toward you half the time, and fires one aimed dot about every 3.4 s.</p><br clear="all">

<p><img src="img/sketch/strongbow.svg" width="260" align="left"><img src="img/screen/strongbow.svg" width="130" align="right"><b>Strong bowtie</b> · 5,000 / 7,500 / 10,000 · 20 hits. Tumbles slowly. Every 1-2 s it fires a fast double shot aimed <b>where you are heading</b> - up to 32 px along your stick - plus a second on a random diagonal.</p><br clear="all">

<p><img src="img/sketch/killer.svg" width="260" align="left"><img src="img/screen/killer.svg" width="130" align="right"><b>Killer</b> · 150 / 250 / 300 · 1 hit. Closes in diagonally on a spot beside you, each with its own offset, and <b>stays out of your four straight firing lines</b>. Fires homing arrows. Built by Spheroids.</p><br clear="all">

<p><img src="img/sketch/brain.svg" width="260" align="left"><img src="img/screen/brain.svg" width="130" align="right"><b>Brain</b> · 500 / 750 / 1,000 · 3 hits. Hunts humans and turns them into Progs. Backs off when you come within 44 px and fires a homing missile every 4-6 s. With no humans left, it comes for you and fires more often.</p><br clear="all">

<p><img src="img/sketch/prog.svg" width="260" align="left"><img src="img/screen/prog.svg" width="130" align="right"><b>Prog</b> · 100 / 150 / 200 · 1 hit. What a Brain makes of a human. Walks straight at you and <b>lunges at double speed</b> over the last 48 px.</p><br clear="all">

<p><img src="img/sketch/spheroid.svg" width="260" align="left"><img src="img/screen/spheroid.svg" width="130" align="right"><b>Spheroid</b> · 1,000 / 1,500 / 2,000 · 1 hit. Zips around at 2 px a step and <b>runs</b> when you get close. Builds a Killer every 4.8 s (1.8 s in later acts), 4 of them (6 later on), then vanishes. Kill it first.</p><br clear="all">

<p><img src="img/sketch/quark.svg" width="260" align="left"><img src="img/screen/quark.svg" width="130" align="right"><b>Quark</b> · 1,000 / 1,500 / 2,000 · 1 hit. Faster still at 3 px a step, just as shy, and builds Tanks a little more slowly than a Spheroid builds Killers.</p><br clear="all">

<p><img src="img/sketch/tank.svg" width="260" align="left"><img src="img/screen/tank.svg" width="130" align="right"><b>Tank</b> · 200 / 300 / 400 · 5 hits. Slow, with shells <b>led toward where you are going</b>. They bounce off the walls with a random kick each time, so no two paths repeat, and last 2.4-5 s.</p><br clear="all">

<p><img src="img/sketch/layer.svg" width="260" align="left"><img src="img/screen/layer.svg" width="130" align="right"><b>Mine layer</b> · 300 / 450 / 600 · 3 hits. Wanders, drops one of its 7 electrodes every second or so, and scuttles away from you.</p><br clear="all">

<p><img src="img/sketch/electrode.svg" width="260" align="left"><img src="img/screen/electrode.svg" width="130" align="right"><b>Electrode</b> · 30 / 50 / 60 · 1 hit. A mine. Never moves, kills on contact, and doesn't count toward a clear.</p><br clear="all">

<p><img src="img/sketch/praetorian.svg" width="260" align="left"><img src="img/screen/praetorian.svg" width="130" align="right"><b>Praetorian</b> · 500 / 750 / 1,000 · 4 hits. The elite guard of the late levels. Charges straight at you - faster sideways than up and down - and fires an aimed spark every 0.8 s.</p><br clear="all">

### Arena 2

<p><img src="img/sketch/splitter.svg" width="260" align="left"><img src="img/screen/splitter.svg" width="130" align="right"><b>Splitter</b> · 150, shards 50 (EASY). Weaves toward you. Shot, it bursts into two shards that fly off sideways, turn, and home in one 45° step at a time.</p><br clear="all">

<p><img src="img/sketch/shieldbot.svg" width="260" align="left"><img src="img/screen/shieldbot.svg" width="130" align="right"><b>Shield bot</b> · 300 / 450 / 600. Swings its shield toward you every 0.6 s. Anything within 45° of head-on bounces off; one shot in the flank kills it.</p><br clear="all">

<p><img src="img/sketch/phaser.svg" width="260" align="left"><img src="img/screen/phaser.svg" width="130" align="right"><b>Phaser</b> · 250 / 400 / 500. Solid for 1.5-2 s, fires one led shot, then <b>phases out and reappears 64 px from you</b> - harmless and untouchable while it materialises.</p><br clear="all">

<p><img src="img/sketch/sniper.svg" width="260" align="left"><img src="img/screen/sniper.svg" width="130" align="right"><b>Sniper</b> · 200 / 300 / 400. Takes up a position, locks an aiming line on you and fires down it a second later at 7 px a frame. It never re-aims: one step aside is enough, if you see it coming.</p><br clear="all">

<p><img src="img/sketch/orbiter.svg" width="260" align="left"><img src="img/screen/orbiter.svg" width="130" align="right"><b>Orbiter</b> · 200 / 300 / 400. Circles you once every 2.6 s on an orbit that breathes between 64 and 22 px. It never fires. It only has to touch you.</p><br clear="all">

<p><img src="img/sketch/fence.svg" width="260" align="left"><img src="img/screen/fence.svg" width="130" align="right"><b>Laser fence</b> · 200 / 300 / 400. Two posts and a lethal beam: on for 2.6 s, off for 1.4 s, flickering just before it fires. Some sweep across the arena. Shoot a post to break it.</p><br clear="all">

<p><img src="img/sketch/centipede.svg" width="260" align="left"><img src="img/screen/centipede.svg" width="130" align="right"><b>Centipede</b> · 100 / 150 / 200 a segment. A head and up to 8 segments, each 7 px behind the one ahead. Hit one in the middle and the segment behind it becomes a new head: <b>two centipedes</b>.</p><br clear="all">

**Power cells:** every 15th robot destroyed in Arena 2 drops a cell that lasts 8 s - **rapid fire** (double rate,
10 s), **triple shot** (two extra shots at ±45°, 10 s) or a **shield** that takes one hit. Active powers show as cards
bottom right.

**Dark levels** show robots only within about 42 px of your ship, until lightning lights up the whole arena for an
instant.

---

## The bosses

<p><img src="img/sketch/guardian.svg" width="260" align="left"><img src="img/art/card_guardian.png" width="150" align="right"><b>The Guardian</b> · levels 20 and 30 · 25,000 / 37,500 / 50,000. A hexagonal core behind <b>eight armour plates</b> of 14 hits each, then the open core: 44 hits, 50 the second time. It keeps off your firing lines and sidesteps shots that would land, while it cycles through 4-way volleys, straight and diagonal, a spawn of a homing missile, a mine and two crosses, and a <b>shield</b> that reflects your fire and regrows a lost plate. A mine drops every 2.6 s throughout.</p><br clear="all">

<p><img src="img/sketch/overseer.svg" width="260" align="left"><img src="img/art/card_overseer.png" width="150" align="right"><b>The Overseer</b> · level 37. The mind of the Arena: six phases and 262 hits on its eye, with points for every one. It switches attack every 8 s and at each phase change, clearing the screen and leaving a mine behind: a 4-way volley, an 8-way spread, bouncing shells, crosses, homing missiles, and a faster spread. Worth 50,000 / 75,000 / 100,000. A bomb takes 10 hits off it.</p><br clear="all">

<p><img src="img/sketch/hydra.svg" width="260" align="left"><img src="img/art/card_hydra.png" width="150" align="right"><b>The Hydra</b> · Arena 2 levels 11 and 22 · 25,000 / 37,500 / 50,000. A head dragging 5 rings, 7 the second time. <b>Only the glowing tail ring takes damage</b> - 7 hits, then the next ring glows. Everything else bounces. Strip the body and the head opens and <b>rages</b>: twice as fast, 5-way volleys, 30-36 hits to finish. The second Hydra spits shards as well.</p><br clear="all">

<p><img src="img/sketch/architect.svg" width="260" align="left"><img src="img/art/card_architect.png" width="150" align="right"><b>The Architect</b> · the final level · three phases of 40, 45 and 50 hits. It raises <b>sweeping laser fences</b> right on top of you and fires 3-way volleys. From phase 2 it teleports, returning in a ring of 8 sparks with an orbiter in tow. In phase 3 it locks an aiming line on you before a fast 3-shot burst. Worth 50,000 / 75,000 / 100,000.</p><br clear="all">

---

## How the robots think

* **Difficulty is thinking speed.** The game runs at 50 frames a second, but each robot gets an AI turn on only
  **70 % of the frames on EASY, 88 % on MEDIUM and 110 % on HARD**, spread evenly across them. Shots, fences and
  centipedes always move at full speed: on HARD the robots react and fire sooner, but the bullets stay fair.
* **Every level has a tier** (0-7) that raises fire rates, shot speeds, build times and missile steering, on top of
  the difficulty.
* **A shot cap** of 4 to 12 enemy shots on screen, rising with the tier, minus 2 on EASY and 1 on MEDIUM. A robot whose
  turn to fire comes while the screen is full skips it.
* **They watch your trigger.** Killers, brains, spheroids, quarks, tanks, mine layers, praetorians, splitters and
  phasers react while you hold fire: one standing in your firing line, ahead of you and within about 10 px of it,
  steps 2 px aside.
* **Homing missiles** steer every 8th frame (every 4th later on), nudging each axis 0.3 px/frame toward you up to 1.5.
  They live 4 s, so they can be outrun or tricked into overshooting.
* **Every enemy shot can be shot down,** for a few points. Losing a ship clears all enemy fire.
* **The cage burst:** for the first second after the cages open, each robot fires outward in a direction set by its
  slot. Then its own logic takes over.
* **Swarm rings** start roughly square around you. Every 4 frames each cross re-aims, and the ring accelerates over the
  first 15 seconds to almost your top speed.
* **Survival levels** bring a robot in every 1-1.4 s from a random edge: the level's featured robot three times in
  four, otherwise a cross. Spawning pauses at 30 robots on screen, and when the clock runs out everything left explodes.

---

## Under the hood

* **The cartridge:** a W27C512 EPROM with the VIA's PB6 line driving A15, giving two 32 KiB banks. Bank 1 holds the
  title, Arena 1, all the screens and the saves; bank 0 holds The Core. Banks switch only between screens. The code
  that runs during a switch - the 1-Wire driver included - sits at identical addresses in both banks, and the build
  checks those bytes, since a low PB6 also selects bank 0.
* **Saves:** an optional DS2431 1-Wire EEPROM keeps two copies of a 64-byte record, written at the end of each game
  and after calibration.
* **The frame budget:** the game holds the Vectrex's 30,000-cycle frame almost all the time. The design rule from the
  start: fewer, smarter robots rather than many dumb ones.
* **Balancing by simulation:** a bot plays every level many times in a cycle-exact emulator at three skill levels.
  Recorded human sessions were replayed against it, so the targets come from how real players actually do.
* **Calibration:** every Vectrex drifts a little at its zero reference. The calibration screen trims it, and the
  setting is saved.

---

## Overlay artwork

The exact layout of the screen overlay, with a brief for new artwork: [overlay/](overlay/README.md).

<p align="center"><sub>Last Human · a Vectrex homebrew by Hugo Bokhorst · 2026</sub></p>
