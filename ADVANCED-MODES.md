# Advanced image modes — 0.5.0 development

The three spatial modes below are local 0.5.0 development additions. The other advanced modes shipped in 0.4.0. Optional cartridge support is retrieved from upstream during setup; third-party driver bytes are not redistributed in this package.

## New spatial modes

| Mode | Image and constraints | Export |
| --- | --- | --- |
| Hybrid playfield + sprites — Static | 160 × 192 preview grid: 40 four-clock playfield cells, overlaid with two independently patterned eight-clock sprite windows. PF foreground/background vary per row; each sprite has one color and one horizontal position for the whole image. | 32 KB F4 ROM + self-contained DASM |
| 96-pixel interleaved bitmap — Flicker | 96 × 192 samples across two fields. Each field displays six eight-pixel sprite copies, covering three alternating 16-pixel bands. One foreground and background per row, shared by both fields. | 32 KB F4 ROM + self-contained DASM |
| Television interlace (experimental) — Flicker | 48 × 384 logical rows; each field draws 192 alternating rows using the existing six-strip sprite kernel. Foreground varies per logical row; background is shared. | 8 KB F8 ROM + self-contained DASM |

### Hybrid detail placement

The hybrid is a constrained overlay, not 160 freely colored pixels across every line. Colors optimization first fits the coarse playfield, then searches for two non-overlapping eight-pixel windows and constant sprite colors that reduce its residual error. Window 1 starts at x=32–144; window 2 at x=48–152 and to its right. Their selected locations are shown beneath the output. Crop/zoom helps put the interesting subject in this usable region. All dither choices operate on legal four-clock cells before fitting sprite overlays.

Colors-only optimization may change these output windows and their colors. Image-only preserves them, along with all row palettes. Settings retain the four row colors followed by the two hexadecimal positions in each hybrid row record. The export validates those constraints. No manual window positioning is included in this version.

### Wider bitmap and brightness

The 96-pixel raster uses NUSIZ=6, three medium-spaced copies of each player. Its second field moves both players 16 clocks to fill the gaps. It occupies the center 96 of the television line's 160 color clocks. Inactive bands display the row background, so the optimizer scores `(foreground + background) / 2` for lit pixels, and the background itself for unlit pixels. This is fixed spatial interleaving; arbitrary phase balancing would break the cartridge layout. A bright background can reduce field contrast, with a corresponding loss of dark range.

### Genuine vertical interlace

Interlace alternates the vertical-sync edge between CPU cycle 3 and 41: a 38-cycle half-line offset. Successive sync edges are 19,950 CPU cycles apart, or **262.5 scanlines**. The full pair has 525 total lines and 384 image rows. This changes television field placement, unlike modes that only alternate colors on the same scanlines. The kernel is informed by Billy Eno and Glenn Saunders's [2002 interlace proof of concept](https://www.biglist.com/lists/stella/archives/200208/msg00110.html), with new field packing and the existing credited sprite kernel.

The application preview places the two fields on alternate logical rows and uses an estimated temporal blend/persistence. Stella validates each 192-row field and the emitted sync timing; its captures are not proof of a particular television's interlacing or deinterlacing behavior. CRT, capture-device, modern-display and physical Harmony compatibility remain untested. This mode is deliberately marked experimental.

### Validation and rebuilding

`tests/test_extended_modes.py` checks legal conversion/dithering, saved settings, fixed-color input optimization, field coverage, malformed export rejection and DASM-to-BIN parity. `tests/gui_extended_smoke.py` exercises the GUI workflows for all three. `scripts/verify_stella_extended.py` compares every displayed pixel in consecutive fields, including hybrid positioning extremes and colored backgrounds; static/wide frames contain 262 lines and interlace alternates 262/263. `scripts/verify_interlace_sync.py` separately measures exact VSYNC edge spacing and half-line phases in Stella.

The new kernels need no ARM driver or external assembler at runtime. Developers can rebuild the checked templates using `scripts/build_extended_templates.py <path-to-dasm>`. Templates are hashed and only their declared immediate/data operands are changed on export. Physical hardware validation remains a separate step.

## Implemented outputs

| Mode | Logical image | Color constraints | Export |
| --- | --- | --- | --- |
| Multiplexed sprites | 48 × 192 | One foreground per scanline, one background shared by the image | 4 KB ordinary cartridge, self-contained DASM |
| DPC+ sprites | 48 × 192 | P0 and P1 have separate foregrounds per scanline; six eight-pixel strips alternate between them; shared background | 32 KB DPC+ cartridge, self-contained DASM with driver |
| CDFJ+ sprites | 48 × 192 | Same display constraints as DPC+; ARM prepares eight CDFJ+ data streams | 32 KB CDFJ+ cartridge, self-contained DASM including Thumb initializer and driver |
| MovieCart frame | 80 × 192, 190 content rows | Ten eight-pixel cell foregrounds plus a background per row, distributed across two alternating fields | 30-second silent `.mvc` stream, settings, packed image data and preview |

The CDF implementation uses **CDFJ+**, the later member of the CDF/CDFJ family. It is explicitly labeled CDFJ+; it is not an original CDFJ driver or a generic bankswitched ROM. Stella's `CDF` mapper selects the subtype from the embedded driver. DPC+ and CDFJ+ currently use the same visible kernel geometry, making their output directly comparable. Their extra cartridge capability does not remove the TIA's sprite and color-write timing limits.

The 48-pixel sprite picture occupies a narrow, centered portion of the 160-color-clock television line. The preview preserves that raster's proportions; it is not presented as a full-width 160-pixel bitmap. MovieCart occupies 80 color clocks, also centered. Raw-pixel geometry remains available for image preparation.

## MovieCart behavior

The exporter implements the original NTSC MovieCart field format from Rob Bairos's source: `MVC\0`, a three-byte field counter, 262 audio bytes, 960 graphics bytes, 60 timecode bytes, 960 foreground-color bytes, 192 background-color bytes, and padding to 4096 bytes per field. The output contains 1,800 fields; the audio and timecode payloads are silent/blank. This is still-image mode, not a video importer.

Each field draws five alternating eight-pixel cells per scanline. The other cells are black on that field. The following field draws the complementary cells, with the reference kernel's one-line field offset accounted for during packing. Two boundary rows are deliberately black. The first content row has a black background because the reference reader clears the first background sample of one field.

The optimizer searches all legal foreground choices per cell and allowed backgrounds per row. It compares the source to the **two-field average**, accounting for the approximately half-duty brightness. Dithering uses the same spatial palette. The animated preview shows both actual fields and supports the existing optional phosphor-persistence approximation. Screen scheduling and CRT appearance remain approximations; the raw field data is independently checked in Stella.

**Export MovieCart** writes `image.mvc`, not `image.bin` or a fictitious assembly ROM. Open it with Stella 7 or newer using the MVC mapper. Physical playback requires MovieCart hardware and its storage workflow; it is not a Harmony cartridge image. The 30-second file is approximately 7 MiB. At the end, Stella's MovieCart implementation holds/repeats the final field pair. The saved `image-data.npz` and settings can reproduce the stream using `chrono.moviecart.binary(indices, line_codes)`.

## Sprite kernels and cartridge drivers

The ordinary sprite kernel extends the existing Andrew Davie-style six-strip multiplexing from 128 to 192 rows without temporal color mixing. Page-aligned graphics and color tables avoid indexed-read page penalties. The visible loop is 76 CPU cycles per scanline.

DPC+ uses authentic immediate-load fast fetch: streams 0–5 provide graphics and streams 6–7 provide P0/P1 colors. Display data resides at ROM offset `$6C00`, copied by the mapper/driver into display RAM. The 6507 resets stream pointers during vertical blank and enables fast fetch only around the picture loop. The standard DPC+ driver is included unchanged.

CDFJ+ uses the same eight-stream schedule. A small generated Thumb routine at `$1800` copies the image into display RAM and resets stream pointers/increments during timed vertical blank. The routine preserves r4 and returns through LR. The included version-48 driver has LDX/LDY fast fetch disabled and a zero fast-fetch offset, following its published template configuration. The 6507 starts in bank 0; its footer specifies the ARM entry and stack.

Both stream kernels fit foreground colors separately for the three copies of P0 and the three copies of P1 on each row. They jointly choose one allowed background for the image. The generic input optimizer, global optimizer, scaling, crop, dithering, settings and cancellation remain available.

## Verification and reproducibility

- Unit coverage checks mode geometry, saved settings, frame averages, cancellation, MovieCart field structure, illegal inputs and two-field persistence.
- With `DASM_PATH` set, assembled sources must match direct binary exports byte for byte, including varied colors and a nonblack background.
- `scripts/build_sprite_templates.py <dasm>` rebuilds the three sprite templates from their source generators. Binary exports verify each template's SHA-256 before patching image data.
- `scripts/verify_stella_sprites.py <Stella.exe> 4K DPC+ CDFJ+` checks every pixel in three successive captured frames and requires 262 scanlines.
- Run `scripts/verify_stella_movie.py <Stella.exe> 700` and again with `701`. Both fields must match every predicted pixel, with 262 scanlines. These use separate emulator processes deliberately: Stella 7.0's `CartridgeMVC::peek` advances its streaming state even for debugger reads, so intermediate debugger inspection can disturb the next field. The first capture after uninterrupted playback avoids this issue.
- Captures use an explicit test palette and allow two RGB levels of rounding difference from Stella's palette transformation. No physical Atari/Harmony/MovieCart validation is claimed.
- `tests/gui_modes_smoke.py` exercises all modes, animation, settings reload, export, MovieCart input/global optimization and Stella routing.

## Ultimate mode: proposed direction, not an implemented kernel

The strongest next step is an **image-specific kernel planner**, with a CDFJ+ backend for a future mixed sprite/playfield kernel. It should not pretend BUS, DPC+, CDFJ+ and MovieCart are one cartridge type. Each has its own bus/driver contract.

1. Start with one fixed crop and a common simulated television canvas. Compare existing modes under the same geometry, rather than rewarding whichever one stretched or cropped away difficult content.
2. Score color error, edges, recognizable detail, temporal modulation and luminance loss. Keep separate rankings for no-flicker and flicker-allowed output; let the user decide that tradeoff.
3. Use the current modes as legal baseline candidates. Fine line art may favor sprite detail, broad color areas may favor Playfield Plus, photographs may benefit from MovieCart's local colors, and coarse low-frequency artwork may suit the BUS raster. More colors alone should not win.
4. For the proposed CDFJ+ hybrid, use a playfield to represent broad areas and repositioned/multiplexed sprites for finer detail. Choose row palettes, masks, sprite placement and priority together. Include a calibrated penalty for visible seams and flicker.
5. Build each row only from a library of cycle-verified schedules. Every schedule must document horizontal coverage, register deadlines, sprite-latch behavior, playfield priority, data-stream count and the 76-cycle limit. Switching schedules must also be verified. Score-mode foregrounds share COLUP0/COLUP1 with sprites, so their colors are not independent.
6. Export only after the planner's predicted image and every field match Stella. Keep a fallback to the best already-proven mode if the hybrid performs worse.

The first useful deliverable would be a side-by-side automatic comparison of existing modes. The new hybrid kernel would then earn its place through measured improvement, rather than an unsupported promise of full-color high-resolution output.

## Primary sources and attribution

- Rob Bairos: [MovieCart source](https://github.com/lodefmode/moviecart), especially `firmware/frame.c`, `firmware/update.c`, `kernel/core.asm`, and `encoder/cpu/ColorizeTOP.cpp`. The repository carries GPL-2.0; its TouchDesigner SDK files have their own notices. This implementation reads the documented format and retains attribution; no SDK is bundled.
- Chris Walton, Fred Quimby and Darrell Spice Jr.: [batari Basic DPC+ driver and definitions](https://github.com/batari-Basic/batari-Basic/tree/master/includes). Bundled `DPCplus.arm` MD5: `5f80b5a5adbe483addc3f6e6f1b472f8`.
- Chris Walton, Fred Quimby, Darrell Spice Jr., John Champeau; template by Craig Daniels/Gamax Software: [CDFJ+ template and version-48 driver](https://github.com/Aganarr/CDFJplus-template). Driver configuration and SHA-256 are recorded beside the binary.
- Darrell Spice Jr.: [CDFJ technical discussion](https://forums.atariage.com/topic/299221-part-2-cdfj-details/).
- [Stella 7.0 source](https://github.com/stella-emu/stella/tree/7.0/src/emucore): `CartDPCPlus.cxx`, `CartCDF.cxx`, `CartMVC.cxx` and Thumbulator configuration.
- Andrew Davie, with Eckhard Stohlberg and Thomas Jentzsch: the credited 48-pixel sprite multiplexing technique retained in the original Chrono2 source.

The CDFJ+ template does not include an explicit redistribution license, and DPC+ driver terms should be distinguished from the compiler license. Consequently this release includes neither driver bytes nor copies embedded in template binaries/ASM. Setup retrieves pinned upstream files and verifies checksums. Local exports incorporate the retrieved drivers; attribution and upstream rights remain applicable.


## Two-frame sprite modes — 0.4.0

The five explicit `(2 frames)` selections preserve the original static choices. Each pixel chooses one of four combinations: foreground/foreground, foreground/background, background/foreground, background/background. Two Color uses two global palettes. With frame balancing enabled (the default), its search requires a common background and the two palettes alternate A/B/A/B by scanline; the following frame reverses them. Pixel assignments are exchanged along with the palettes, preserving each pixel's exact temporal color sum. Identical palettes additionally allow checkerboard assignment of half-intensity pixels. This spreads the two images spatially rather than flashing one whole palette at a time; it cannot remove all flicker. Existing saved palettes with different backgrounds remain intact and show a prompt to optimize colors for the new shared-background constraint. Disabling balancing restores uniform frame assignment and permits independent backgrounds during palette search.

Scanline and ordinary multiplexed modes allow a foreground per row per frame. DPC+ and CDFJ+ additionally separate P0/P1 colors across their alternating strips. Each frame has a spatially constant background. The Two Color change reuses the existing verified per-row foreground tables in the F8 kernel; it does not alter scanline timing.

The two frames are fitted jointly to their actual average; they are not duplicate copies of a static image. Saved row palettes contain eight codes (four for A, four for B). The frame index map is 0–3. The background restriction applies to both frames.

- Ordinary 128- and 192-row kernels use F8: two 4 KB banks, alternating at a shared bank-switch trampoline once per television frame. The 128-row version retains blank borders and 262-line timing.
- DPC+ stores two 2048-byte display planes. A frame-phase byte selects the fetcher pages and frame background during vertical blank.
- CDFJ+ passes its phase through the communication stream to the Thumb routine, which loads the selected plane and resets the data streams each frame.
- The ROM templates have integrity hashes. `scripts/build_pair_templates.py <dasm>` rebuilds them. Generated ASM assembles byte-for-byte to the direct BIN export, including nonblack backgrounds.
- `scripts/verify_stella_pairs.py <Stella.exe> 12 13 14 15 16` verifies all pixels and 262-line timing across A/B/A or B/A/B sequences. This establishes emulator behavior, not physical cartridge compatibility.

Flicker-aware input/global optimization evaluates the actual frames as well as their blend. See README for the adjustable policy and its brightness/reference assumptions.
