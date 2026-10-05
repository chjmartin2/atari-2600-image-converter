# Atari output modes and perceptual optimization

Research and implementation notes, October 3, 2026. These describe the local 0.2.0 development build.

## Hardware findings

The TIA has no framebuffer. Software supplies graphics and color-register changes while the display scans. An NTSC frame normally has 262 lines, each allowing 76 CPU cycles. Color registers retain their values until rewritten. That permits different colors on successive scanlines, but does not permit an arbitrary color at every bitmap pixel. The four color registers are shared among the background, playfield/ball, and two player/missile groups. These constraints come from Atari's [Stella Programmer's Guide, Steve Wright](https://www.atariage.com/2600/programming/2600_101/docs/stella.html).

The six-copy sprite technique can produce a 48-pixel-wide bitmap by rewriting the two player graphics registers and exploiting their delayed copies. Andrew Davie's original kernel in this repository uses this technique with three interleaved color frames. Michael Martin's [48-pixel kernel analysis](https://bumbershootsoft.wordpress.com/2018/09/24/atari-2600-a-48px-kernel/) is a useful independent explanation of the register pipeline, positioning and write deadlines. The implementation here derives the multiplexing sequence from the project's existing credited Davie code; it does not copy the article's game implementation.

For a stable image that spans the screen, an asymmetric playfield provides 40 independently controlled bits per row. It requires updating PF0/PF1/PF2 for the right half after the left half has used them. Andrew Davie's [asymmetric playfield tutorial](https://www.randomterrain.com/atari-2600-memories-tutorial-andrew-davie-20.html) explains that scheduling constraint. This is a useful trade-off: fewer horizontal samples than the 48-pixel sprite, but a full-width picture, 192 image rows, and time for two independently chosen colors per row.

Other kernels can mix player, missile, ball and playfield objects, change colors during a line, or trade vertical resolution for more updates. Those possibilities do not create a general unrestricted four-color-per-pixel bitmap. This build implements two concrete, validated raster formats rather than claiming an absolute best mode for every image. Compare 48-pixel scanline color against the 40-pixel playfield for each source.

## New 48-pixel raster kernel

`raster_rom.py` emits three fixed-address drawing loops and a full three-frame data set. Each frame stores six strips of 128 bytes followed by 128 foreground color codes. Every table begins at an address ending in $00 or $80, so indexing rows 0–127 never adds a page-crossing cycle. All loop branches stay within a page. A taken row loop is exactly 76 cycles.

The color write is moved into the line schedule, and six fixed-address indexed graphics reads replace the original indirect reads. The final graphics-register write sequence retains the required multiplex timing. The CPU uses the stable NMOS LAX instruction, as the historical kernel also does. Sprite positions remain fixed and the background is constant across rows. Temporal mode supplies the appropriate component color for each row and phase; static scanline mode uses the same foreground and on/off pixels in all three frames.

The bitmap/color payload is 2,689 bytes. Drawing loops occupy $FB00, $FC00 and $FD00; initialization and frame control begin at $FE00. The entire cartridge is 4,096 bytes. Original `kernel.asm` and its template are unchanged.

## New 40-pixel playfield kernel

Eight 256-byte-aligned tables hold six playfield strips and foreground/background colors for 192 rows. PF0's four bits and PF2's eight bits are packed in their hardware scan order; PF1 uses the opposite bit order. The row loop writes left PF0/PF1/PF2 at CPU-cycle completion counts 17/24/31 and the right values at 44/51/58. The next foreground code is prefetched into X near the end of the preceding line, so color updates do not delay the left PF1 write.

The first test exposed a one-pixel boundary error when PF1 was written too late. Prefetching the foreground removed that error. Stella now produces exact matches for random asymmetric bitmaps, including the register boundaries. All static frames repeat; there is no temporal mixing. The 4K ROM uses 2,048 bytes for the aligned data tables.

## Joint and global optimization

The active optimizer is `optimization.py`; the compatibility entry point in `core.py` delegates to the same visible-control fitter. The reference image remains fixed throughout a search. Ordinary joint optimization alternates actual brightness/contrast fitting, hardware-constrained palette fitting on that adjusted image, and a second control fit. It tries up to three passes, displays completed passes and returns the best measured state, including the initial conversion as a fallback.

Global optimize tries up to four passes per starting point. In custom mode it also starts from the original RGB, grayscale and neon presets. It searches gamma and saturation as well as brightness/contrast. Other image settings remain under user control. Static row fitting exhaustively compares legal foreground/background pairs; per-row temporal fitting uses multi-start coordinate descent. Legacy exhaustive remains available for the custom global palette, although its arbitrary-background option is expensive.

The universal color model (October 5, 2026) uses the [sRGB transfer function and color-space conversions](https://www.w3.org/TR/css-color-4/) and an independently implemented [CIEDE2000 formula](https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/). All 34 Sharma/Wu/Dalal reference vectors verify the formula, including zero-chroma and hue-wrap boundaries. A scalar diffusion implementation is cross-checked against the vectorized implementation.

NTSC palette RGB is assumed display-referred sRGB, not measured CRT drive voltage. Decode to linear light before temporal mixing, duty-cycle scaling and persistence. Encode for the 8-bit preview/target palette, then compare in D65 Lab with DE00. Both source and output use the same white and absolute reference scale. No exposure gain, per-mode reference budget, extra CRT gamma, or Classic 0.30 reference remains. Color error is supplemented with L* edge/detail error and, when enabled, linear-luminance temporal variation. Diffusion propagates linear-RGB error; nearest choices and both palette search models use DE00. This does not model full spatiotemporal visual perception or establish a calibrated CRT match.

This is an explicit, inspectable perceptual heuristic, not a guarantee of an optimum and not a measured CRT transfer function. The bundled palette differs from some Stella palette settings. Gamma, phosphor response and composite color vary between displays. No artificial brightness correction is written to the ROM beyond the selected hardware colors and image bits.

## Verification method

Independent DASM builds are compared byte-for-byte with direct template exports. Stella 7.0's [documented debugger scripting commands](https://stella-emu.github.io/docs/debugger.html) advance frames, save TIA snapshots and dump the observed frame-line count. Each test uses its own configuration/output directory and does not alter the owner's emulator settings. Randomized edge-marked bitmaps verify strip order, row order, register boundaries, temporal plane cycling and identical static frames. Exact 262-line frame lengths are checked from the emulator's `_scanEnd` value. Per-row color checks supply an explicit external palette and account for Stella 7.0's default TV/PC gamma adjustment in [PaletteHandler.cxx](https://github.com/stella-emu/stella/blob/7.0/src/common/PaletteHandler.cxx). A one-level RGB tolerance covers hue/saturation rounding; bitmap masks must match exactly. The playfield test changes both foreground and background across rows.

Emulator results do not establish physical Atari/Harmony validation. That remains a separate check on the user's hardware.

## Playfield Plus (0.2.1 development)

Playfield Plus is a static 40x192 mode with up to four colors across each row. The four saved row values are left foreground, left background, right foreground and right background. Score mode (CTRLPF bit 1) supplies separate left/right foregrounds. A timed COLUBK write supplies different backgrounds. Atari's programmer guide describes both score-mode routing and writable color registers; [Stella's cartridge documentation](https://stella-emu.github.io/docs/index.html) identifies the standard 16K F6 format.

Ten immediate color/graphics writes per row avoid indexed-load overhead. Three F6 banks hold 64 unrolled rows each; a fourth holds reset, sync, blanking and overscan. Identical trampolines in all banks read the F6 hotspots and continue execution at the same address in the selected bank. Every reset vector points to a trampoline selecting the control bank. There are no extra RAM requirements or unsupported CPU instructions.

Within each row, foreground writes complete at CPU cycles 5/10, left background at 15, left PF0/PF1/PF2 at 20/25/30, right PF0/PF1 at 35/40, right background at 48 and right PF2 at 53. The initial cycle-49 background write produced a one-color-clock seam. Cycle 48 instead changes at a whole playfield pixel boundary: television x=76. Score mode still changes foreground at x=80, so logical pixel 19 uses left foreground/right background. Quantization and rendering explicitly use this spatial constraint. Three-cycle BIT padding controls the transition without changing flags that affect rendering.

The fitter searches all allowed pairs for the 19 regular left pixels and 20 right pixels; the boundary pixel is quantized using the resulting legal cross-pair. This is a practical heuristic, not exhaustive joint optimization of all four colors including the boundary cell. Global optimize uses the rendered result, including that cell, when choosing input adjustments.

DASM assembly is byte-identical to direct 16KB exports. Stella verifies three identical full-width frames, per-row colors, both bank boundaries, all pixel boundaries and 262-line timing. The verifier now checks every captured pixel rather than one sample per logical pixel. Up to two RGB levels are allowed for Stella's hue/saturation and gamma rounding; placement and bitmap masks are exact. Actual Atari/Harmony checks remain outstanding.

## Diffusion spill correction — October 5, 2026

The source target is bounded to attainable local palette mixtures before error diffusion. Channel bounds are followed by a bounded, 64-iteration Frank–Wolfe convex projection in linear RGB. Each intermediate result is a feasible mixture; the nearest projection is approximate. This is gamut clipping, not an output-index decision: final quantization still uses CIEDE2000. It prevents unavailable highlight/color energy from persistently accumulating into adjacent pixels.

Accumulated error stays signed; only the nearest-color lookup clamps to the physical RGB range. Previously clamping before residual calculation discarded negative error and introduced a brightness bias. Exact source black is an absorbing boundary when the pixel's palette can reproduce black, intentionally dropping incoming error there to preserve borders. This does not protect near-black pixels or invent a color absent from a local palette. Kernel weights and serpentine direction were already correct; Atkinson intentionally distributes only 75% of the residual. Ordered and no-dither branches are unchanged.
