# BUS mode and Atari graphics techniques

Research and implementation: October 3, 2026. Chrono2 Studio 0.2.2-dev.

## What is implemented

Select **Bus stuffing (experimental)**. This is a genuine BUS2 cartridge, with a
cartridge ARM initializer, display RAM, a datastream and stuffed STY writes to
COLUBK. It exports a 32 KiB BIN and self-contained DASM assembly. Open Stella
selects the BUS mapper automatically through its command-line argument.

The image is **16 × 192 independent color samples**, each selectable from all
128 NTSC color codes. Each sample is nine TIA color clocks wide. The picture
occupies x=7 through x=150 of the 160-clock visible line, with black borders.
It repeats identically every frame: no temporal color mixing or brightness loss.
The preview shows the image area at its corresponding 6:5 display aspect ratio;
it omits the black side borders. The full palette is shown instead of editable
Chronocolour components. Palette search has no restricted palette to choose in
this mode; Optimize input and Global optimize can still fit the image controls.

This prioritizes independent color over horizontal detail. Sixteen samples is
the capacity of this particular first kernel, **not the limit of BUS technology**.
It is not a 160 × 192 independently colored bitmap. Playfield Plus currently
provides more horizontal shape detail, while BUS provides much more color freedom.

## Mechanism and verification

A normal immediate load plus zero-page TIA store takes five CPU cycles. BUS2
replaces the operand on a three-cycle STY zero-page write with the next display
byte. Since each CPU cycle is three color clocks, consecutive background writes
make nine-clock color strips. This implementation completes its 16 writes at CPU
cycles 25, 28, ... 70, then clears the background at cycle 73. Three unrolled
64-row ROM banks preserve that schedule, including the bank transitions.

The small generated ARM7TDMI initializer sets stream 0, its one-byte increment,
the COLUBK stream mapping, and copies 3072 bytes of image data into display RAM.
It runs once before the stable video loop. Stream 0 is reset every frame by the
6507. Assembly bytes and the direct binary exporter are checked against DASM.

Stella 7.0 checks compare all image samples, including all bank seams, against
the expected palette for three consecutive frames. The measured frame is 262
scanlines and the picture is 192 lines high. RGB comparison allows two channel
levels for Stella's palette rounding. These are emulator checks. Real console,
Harmony firmware and BUS-driver compatibility have **not** been validated.
Stella itself labels BUS experimental. Do not assume ordinary Harmony ROM loading
or an arbitrary 2600 Jr./7800 will support this driver merely because Stella does.

## Other techniques and realistic targets

“Resolution” needs three separate descriptions: shape detail, color-cell size,
and whether several frames must be blended. The TIA's usual 160-clock visible
line does not provide a framebuffer with 160 arbitrary color writes.

| Technique | Shape/detail or demonstrated format | Color and temporal restrictions | Status here |
|---|---|---|---|
| Asymmetric playfield | 40 independent bits across a line; our kernel is 40 × 192 | Four color clocks per bit; basic kernel chooses foreground/background per line | Implemented |
| Score-mode playfield plus timed colors | Our Playfield Plus: 40 × 192 | Left/right foregrounds and backgrounds; four row colors are spatially restricted, not four freely selectable colors at each pixel; bridge pixel is documented in RESEARCH.md | Implemented |
| Multiplexed player bitmap | A 48-pixel-wide bitmap from repeated player sprites; our existing sprite modes use 128 rows | Fine horizontal shape detail, but color changes consume cycles; static row mode has foreground/background constraints | Implemented; see Michael Martin's kernel explanation |
| Interleaved Chronocolour | Our format: 48 × 128 | Three interleaved temporal components; up to eight estimated mixtures for a chosen component set; flicker and brightness loss | Implemented, including per-line component choices |
| BUS color raster | This kernel: 16 × 192, nine clocks per sample | Any of 128 colors at every sample, same image every frame | Implemented and Stella-verified |
| BUS plus player/playfield multiplexing | Higher-detail composite layouts are possible; no single fixed bitmap resolution follows from BUS | Saved write cycles can update shapes and colors more often; the eventual width and color-cell boundaries depend on a cycle-audited kernel | Research direction; not an implemented high-resolution BUS mode |
| DPC+ / CDF / CDFJ / CDFJ+ | Cartridge-side computation and fast data streams; no intrinsic new display resolution | More time for sprite/playfield composition and animation. The TIA still renders the picture. Cannot promise arbitrary 160 × 192 full color from the cartridge label alone | Stella supports these families; worthwhile next architecture to prototype |
| Frame-alternated wide sprite bitmap | Nick Bild's digital frame demonstrates 64 × 84 and discusses up to 192 rows | Two colors; first 48 pixels and final 16 are displayed on alternate frames | External Pico-cartridge example; illustrates the width/flicker tradeoff |
| MovieCart | Creator advertises 80 × 192; technical description also discusses a 262-line field | Alternating checkerboard fields, ten eight-pixel color cells per line, 128 available colors and 30 combined frames/s; advertised detail is not independent color at every point | Separate cartridge/streaming format; not a conventional Harmony BIN |

For our converter, a sensible next experiment is a **cartridge-assisted sprite
and playfield image kernel** that preserves more shape detail while allocating
colors to smaller regions. CDFJ deserves investigation for this. MovieCart is
also relevant if we want image slideshows or video, but it is a different export
target. Neither should be described as already implemented.

## Primary sources and provenance

- [Atari's Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html): TIA registers, player copies, playfield, color and timing.
- [Andrew Davie's asymmetric playfield tutorial](https://www.randomterrain.com/atari-2600-memories-tutorial-andrew-davie-20.html): rewriting the playfield during a scanline.
- [Michael Martin's 48-pixel kernel explanation](https://bumbershootsoft.wordpress.com/2018/09/24/atari-2600-a-48px-kernel/): player multiplex timing.
- [Darrell Spice Jr.'s homebrew presentation](https://studylib.net/doc/5631678/bus-stuffing---darrell-spice--jr/) (mirror of the author's slides): DPC/DPC+/BUS cycle comparisons and cartridge assistance. [Author's PDF](https://spiceware.org/downloads/Atari%202600%20Homebrew.pdf).
- [Stella 7.0 BUS implementation](https://github.com/stella-emu/stella/blob/7.0/src/emucore/CartBUS.cxx): BUS revisions, register map, STY interception and Thumb entry.
- [Stella user guide](https://stella-emu.github.io/docs/index.html): BUS experimental status and DPC+/CDF(J)(+) support.
- [Nick Bild's digital frame](https://github.com/nickbild/atari_2600_digital_frame): its creator's resolution, two-color and alternating-frame explanation.
- [MovieCart source and technical specification](https://github.com/lodefmode/moviecart): its creator's field/cell description. The 80 × 192 headline and 262-line technical wording are retained separately rather than pretending they are the same measurement.

`chrono/resources/bus2-driver.bin` is the unchanged first 2048 bytes of
`128bus_20170120.bin`, obtained from the bankswitching test ROMs in the
[official Stella 7.0 source archive](https://github.com/stella-emu/stella/releases/download/7.0/stella-7.0-src.tar.xz).
SHA-256: `2d489398d221bd340e8ea7af129045c0147089a0b17785e6cea87a094cdb81d0`.
No demo images, demo 6507 kernel or demo ARM application are incorporated.
Our initializer and background raster are generated by `chrono/bus_rom.py`.

The driver is a third-party historical binary. Its standalone redistribution
terms have not been established from the archive; do not assume Stella's license
automatically licenses bundled test ROMs. This work is installed locally for
experimentation. Resolve the driver's permission/source/license before a public
release of the driver or ROMs containing it. No public push is part of this task.

Rebuild: `python scripts/rebuild_bus.py <path-to-dasm>`.
Emulator verification: `python scripts/verify_stella_bus.py <path-to-Stella.exe>`.
