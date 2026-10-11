# BUS mode and Atari graphics techniques

Research and implementation: October 3, 2026. Chrono2 Studio 0.2.2-dev.

## What is implemented

Select **Bus Stuffing - 16x192 Color Raster — Static**. This is a genuine BUS2 cartridge, with a
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


## 128x200 Single Color (October 10, 2026, local development)

`chrono/bus128_rom.py` adapts the cycle-exact sprite schedule from cd-w / Chris Walton and SpiceWare / Darrell Spice Jr.'s `128bus_20170120.bin`, preserved in the official Stella 7.0 source archive. The source demo and discussion are at https://forums.atariage.com/topic/258191-bus-stuffing-demos/page/4/#findComment-3676378 . The original driver remains an optional external dependency; its checksum and retrieval are unchanged. No demo artwork, menus, or original ARM application is included. No additional redistribution rights are asserted over the derivative timing code.

The new fixed-image initializer copies 3200 bytes to BUS display RAM, maps GRP0 and GRP1 to stream 0, and initializes the stream increment. Two 1600-byte streams each encode 200 rows of eight sprite bytes. The 6507 selects the appropriate stream and alternates the original sprite layouts. Both sprite colors are set to one chosen foreground; COLUBK holds one chosen background throughout the picture. A position self-test retains the original B0/C0 HMP0 compatibility handling.

Visible image: 128 color clocks by 200 lines, centered at x=16..143. Normal preview aspect is 256:200; Raw pixels is 128:200. This is spatially interleaved flicker at a steady 262 scanlines per field, not half-line television interlace. Each logical pixel is visible in one of the two fields; the other field supplies background light. Foreground targets are therefore the linear-light mixture of foreground and background, while background pixels remain background.

The two row layouts cover strips starting at `(0,16,32,48,64,88,96,120)` and `(8,24,40,56,72,80,104,112)`. Successive rows swap layouts; successive fields reverse them. The chronological stream byte order differs from spatial order because of sprite resets: `(32,0,16,48,64,88,96,120)` and `(40,8,24,80,56,72,104,112)`.

Verification: DASM export parity; exact random-bitmap packing roundtrip; settings migration; shared palette/field-light agreement; GUI manual color, crop, optimization, rendering preview and exports. `scripts/verify_stella_bus128.py` compares all 25,600 logical pixels in each of three consecutive snapshots with the generated preview, including first/last rows and both phases. Both white-on-black and cyan-on-colored-background fixtures pass, each with 262/262/262 scanlines. This is emulator verification, not physical console validation. `scripts/build_bus128.py` rebuilds the public template with a zero-filled 2 KiB driver slot.


## 128x200 Color per Line (October 10, 2026, local development)

`chrono/bus128_line_rom.py` preserves the preceding mode's 128x200 coverage and stream ordering, but writes COLUP0 and COLUP1 for each row. The background remains global. A 4000-byte stream holds two 2000-byte fields: two identical foreground bytes followed by eight sprite bytes per row. The ARM initializer copies the stream from ROM offset $1000 to display RAM and maps both color registers plus GRP0/GRP1 to stream 0.

The kernel unrolls each field into three banks (2/3/4 and 5/6/7). At the A/B boundary, the original seven-cycle counter/branch becomes six cycles of zero-page STY color writes plus one extra cycle in the following LDX (RAM instead of immediate). NUSIZ1 moves one cycle earlier inside HBLANK; all subsequent visible writes and sprite resets retain their timing. Absolute STY is deliberately avoided: the BUS2 driver intercepts zero-page STY only. At the B/A boundary, two STY instructions plus NOP replace the eight-cycle counter/branch.

Fixed-address bank bridges replace a four-cycle delay with BIT at the bank hotspot. The incoming bank supplies the same row tail at the same address. A three-cycle RAM LDX plus three-cycle JMP replaces the original two-cycle immediate LDX plus four-cycle NOP delay. This keeps both bank transitions pixel-aligned. The first and last rows are included; fields remain 262 scanlines.

Palette fitting searches all allowed global backgrounds and all 128 foregrounds for each row. Weighted 32-level RGB histogram centroids bound the CIEDE2000 calculations while retaining separate row distributions; it is a histogram approximation, not an exact fit to every original RGB sample. The targets include the true 50% foreground duty. The chosen row colors remain fixed for Image only optimization and ordinary image adjustments.

Rebuild with `python scripts/build_bus128_line.py <DASM>`. Verify with `python scripts/verify_stella_bus128_line.py <Stella.exe>`. The test compares every pixel across three consecutive fields with 200 changing row colors, using both black and colored backgrounds, and checks 262/262/262 scanlines. Unit tests also cover stream reconstruction, matching, black-border dithering, invalid row palettes, settings persistence, animated export, and byte-for-byte DASM parity. `tests/gui_bus128_line_smoke.py` exercises selection, row inspection, crop, any-background search, preserved row colors during Image only optimization, previews and ASM/BIN export. Driver slots in the public template are zero-filled. Physical console/Harmony testing remains outstanding.


### Paired-row palette fitting

`chrono/bus128_pairs.py` implements the optional strict two-row palette fit. Each pair uses foreground A on its upper row, foreground B on its lower row, and the same global background. The two foregrounds must differ from each other and the background in actual palette RGB, not just code value. Each pixel still uses one bit and the existing two-field 50% duty cycle.

After screening shared backgrounds with independent row fits, the search evaluates up to four backgrounds. Per-pair foreground candidates include the best four fits for each original row and their linear-light average plus a best candidate from each TIA hue family. For each ordered foreground pair, it constructs the two undithered row outputs using their actual temporal target colors. The score is 80% CIEDE2000 error of the linear-light row average and 20% mean error at the original rows. Both color assignments are considered. Existing perceptual input optimization uses the same 80/20 spatial emphasis, retaining its detail and temporal-flicker terms. The final selected dither still runs on the full 128x200 image with its row palettes; no extra error is routed downward.

This is a color-variety heuristic with deliberate stripe/detail tradeoffs, not a new display mode or new kernel. Unit and GUI checks cover strict pair uniqueness, flat fields, clean black borders, local pair fitting, linear averaging, settings compatibility, scoring, toggle/refit behavior, reset and exports.


### Full-raster dither refinement and random tables

`chrono/bus128_line.propose` and `chrono/bus128_pairs.propose` provide bounded candidate tables from their original undithered searches. Independent fitting includes alternate foreground rankings; paired fitting includes the next-best ordered color pairs. `chrono/bus128_dither.refine` then runs complete 128x200 candidates through the same `core.quantize` function used by final conversion, with the selected method, strength and serpentine setting. Every trial starts at the top of the original image, so error crossing row boundaries is recalculated for that candidate's actual palettes. Selection uses the real temporal render and the existing perceptual/flicker score, including paired spatial scoring when enabled.

Standard considers two unique initial tables plus a valid current table and one residual-feedback proposal; Thorough considers four initial tables and two feedback proposals. Feedback smooths actual linear-light residuals horizontally over eight-pixel cells (and over each row pair when paired fitting is active), solely to guide another palette proposal. Every proposal is rescored against the same original image. The best evaluated table survives, so this pass cannot regress its starting table under the selected score. None and zero-strength searches bypass refinement.

Random row generation samples unique physical palette RGB colors, excluding the background and preceding row, then stores the resulting 200-row table. It respects the strict paired-row constraint as well. No new cartridge format, driver, TIA timing or packing changes are involved.
