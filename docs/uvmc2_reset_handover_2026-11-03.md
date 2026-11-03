# Handover: UVMC2 edition "resets every few seconds" (2026-11-03)

## Context

- Project: **Last Human** (formerly Robot_Arena / Steel Siege), a Vectrex game with two editions.
  - **6809 cart**: 64 KB, PB6 bank switching. Source in `src/`.
  - **UVMC2 C port**: in `uvmc2/`, built to `.um2` for the RP2350 cartridge.
- Public repos: `hugonl31/Last_Human` (game) and `hugonl31/Vectrex_EMU` (emulator, `G:\AI\Vectrex_EMU`).
- The user works over **SSH and cannot see any UI**.
  - Render emulator frames to PNG and look at them yourself.
  - Never rely on windows or the clipboard.

## The bug report

A user with a real UVMC2 reports that `Last_Human_UVMC2.um2` v1.3.5 keeps resetting every few seconds:

- It happens on the **game's title screen**.
- They already have a calibration config, so the calibration screen isn't involved.

## Diagnosis so far

The likely cause is the UVMC2 SDK's reset-button watch, found by elimination; it is not confirmed on hardware.

**How the watch works** (`uvm2_core1.c` → `reset_poll`, in the starter kit SDK v1.4.5):

- Core 1 reads VIA DDRB between frames. Each frame list sets DDRB=0x9F.
- DDRB==0 counts as a RESET press. After 1 s the SDK restarts the game (`rom_reboot`).
- Some consoles probably read 0 there without anyone pressing RESET.
- Upstream SDK v1.4.6/v1.4.7 do not fix this (checked their CHANGELOG): v1.4.6 only sets DDRB before the first frame's read
  (a reset that opened the calibration wizard), v1.4.7 only shows RESETTING during the 1 s wait.

**What the emulator showed** (Vectrex Studio's Uvm2System, 1400 frames; runner `/mnt/g/AI/VectrexStudio/src/ide/frontend/tools/lh_run.mjs`, env `PROBE=1`):

- 0 reset presses seen.
- Stack peak 1312 of 4096 bytes on core 0.
- 0 dropped commands.
- So there's no software fault such as a stack overflow. A hardfault would show a solid red LED, not a reboot.

## What was shipped today

1. **Pre-release `v1.3.5-resetcount`**: https://github.com/hugonl31/Last_Human/releases/tag/v1.3.5-resetcount
   - Marked as a pre-release; v1.3.5 is still "Latest".
   - Tag on the same commit as v1.3.5 (c280ee1).
   - Asset: `Last_Human_UVMC2_resetcount.um2`, 380,424 bytes, md5 4fe090d4f85f7574fe520b4ed3690525.
   - Build flags: `EXTRA="-DSPEED_TEST -DUVM2_RESET_WATCH_ONLY"`. The watch only counts and never restarts.
   - The **RST** counter is shown on screen. Holding buttons 1 and 4 on the title hides or shows it.
   - `resets=` is logged to `lasthuman/speed.txt` on the SD card every 10 s.
   - Side effect: the console's RESET button does nothing in this build, so the player must power-cycle.
   - Notes source: `build/uvmc2_diag/resetcount_notes.md`.
2. **README commit 48d132a** adds a "Resetting every few seconds?" paragraph to the `## UVMC2 edition` section, linking to the pre-release.

## Waiting on

The reporter's answers to three questions:

1. Does the game keep running now?
2. Does RST climb without anyone touching RESET?
3. Their `speed.txt` file.

Next step depends on the answer:

- **It keeps running and RST climbs:** the watch is confirmed as the cause. Make v1.3.6 in one of two ways:
  - Build with `EXTRA=-DUVM2_NO_RESET_BUTTON`. A test build of this exists: `build/uvmc2_diag/lasthuman_v1.3.5_noresetwatch.um2`.
  - (Rebuilding on SDK v1.4.7 is not a fix: it keeps the same DDRB check. At most it shows RESETTING on screen.)
- **It still resets:** the cause is something else. Look at `speed.txt`.
  - Also ask whether other SDK games reset on their console too.
  - Suspects: power or brown-out, the SD card, the cartridge's own firmware.

## Build facts

- **Release build:**
  - Command: `cd /mnt/g/AI/Robot_Arena/uvmc2 && make -C uvm2 uvm2 < /dev/null`
  - Output: `uvm2/build_uvm2/lasthuman.um2`, md5 `aabc8c3dc9ded383605c798e93af0b85`, the same as the published v1.3.5. That release build is the one currently in the build folder.
- `EXTRA=...` goes into UVM2_CFLAGS. It applies to the SDK sources too; this was verified in `CMakeFiles/lasthuman.dir/flags.make`.
- **SDK:** starter kit in `~/uvmc2-starter-kit`, SDK v1.4.5. Its only local change is the pad2 patch in `uvm2_input.c` (player 2's axes).
- **Uncommitted source change:** `uvmc2/uvm2/speed.c` adds the RST / `resets=` readout.
  - It only takes effect with `-DSPEED_TEST`, so release builds are unaffected (the md5 above proves it).
  - The original file is saved at `build/uvmc2_diag/speed.c.orig`. Keep the change if you make another diagnostic build; otherwise restore the original.
- **Test builds** in `build/uvmc2_diag/`:
  - `_release`
  - `_noresetwatch`
  - `_resetcount` (the same file as the published one)

## Tools

- **Vectrex Studio** (tullulah, v0.4.0):
  - App: `/mnt/g/AI/VectrexStudio/Vectrex.Studio.0.4.0.exe`. Source: `src/`.
  - Headless runners are in `src/ide/frontend/tools/`:
    - `lh_run.mjs` runs a .um2. Args: `img outprefix frames "dumpframes" "f0-f1:BTNS:JX:JY;..."`. Env: `SDDIR`, `PROBE=1`. The probe addresses are hardcoded for the v1.3.5 **release** ELF, so update them for any other build.
    - `lh_run6809.mjs` runs a .bin. The env var `BIOS` needs the real 8 KB BIOS, `/mnt/g/AI/Robot_Arena/ref/bios.bin`. The repo's `public/bios.bin` is a 4 KB stub.
  - Vectrex Studio supports only $DF00 banking, not PB6. So the full 6809 cart can't run there; only bank 1 works.
  - Render the dumped segments with a small numpy segs→PNG script. The Y axis is `H/2 + y`.
- **GitHub:**
  - `gh` is missing in WSL. Use `"/mnt/c/Program Files/GitHub CLI/gh.exe"`; it is logged in as hugonl31 (scopes: repo, gist, read:org).
  - It is a Windows exe: give it files on `/mnt/g/...` and `cd` there, not `/tmp`.
  - If it needs to log in again: run `gh auth login -h github.com -p https -w` **yourself in the background**, read the one-time code from the output file and show it to the user. When the user runs it with `!`, the command goes to the background after 120 s and they never see the code.
