# Atari 2600 Image Optimizer

A Python desktop workbench for turning pictures into **NTSC Atari 2600 cartridge images**. This continues Chris Martin's 2011 Chrono2 converter, using Andrew Davie's original Interleaved Chronocolour display kernel and separate new scanline kernels.

Version **0.4.0** provides seventeen output modes, including MovieCart still frames, DPC+ and CDFJ+ streamed sprites, and 192-row multiplexed sprites. This is a published Python application release. See [ADVANCED-MODES.md](ADVANCED-MODES.md) for formats, hardware limits, provenance, verification and the proposed ultimate-mode design.

## Run

On Windows, double-click **Run Atari 2600 Image Optimizer.cmd**. Python 3.12 or newer with Tkinter is required. The first run creates `.venv`, installs NumPy and Pillow, and retrieves BUS, DPC+ and CDFJ+ cartridge support directly from the original upstream sources. These downloads require Internet access and are verified against pinned checksums. Later runs use the cached support files. No external assembler is required for export. This ZIP contains Python source and a Windows launcher, not a standalone EXE. The owner's local project already has this environment prepared.

Alternatively:

```text
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python run.py
```

Pass an image path to `run.py` or drop it onto the launcher. The application starts with an original calibration image when no file is supplied.

## Image workflow

1. Open PNG, JPEG, BMP, GIF, TIFF or WebP. Animated inputs use their first frame; transparency is composited over black. EXIF orientation is honored.
2. Choose fill/crop (the default), fit or stretch; nearest, box, bilinear, Hamming, bicubic or Lanczos resampling; rotation and horizontal mirror.
3. Adjust brightness, contrast, saturation, gamma, sharpness and individual RGB gains. Changes automatically refresh the conversion.
4. Select a preset or click the color swatches to open the NTSC picker. Presets include original RGB, grayscale, sepia, neon, pink, blue and a CGA-inspired magenta/cyan/black combination. In classic/custom modes these are Atari approximations: the eight output colors are mixtures of three hardware colors and a background. Static modes use solid hardware colors.
5. Select no dithering, ordered 2×2/4×4/8×8, Floyd–Steinberg, Atkinson, Jarvis–Judice–Ninke, Stucki, Sierra or Burkes. Error diffusion supports serpentine traversal and a strength control.
6. Convert with that palette, or choose either search model and press **Optimize palette**. Searches run in the background and support cancellation.
7. Inspect the temporal-blend estimate, quantization targets or individual component frames. Use fit-to-window or fixed zoom, crisp/smooth display and drag-to-pan.
8. Export ASM + BIN. A new export folder contains `image.asm`, `image.bin`, `settings.json`, `preview.png` and attribution/readme text. Export is blocked while conversion is unfinished or settings are stale.

Save/load settings independently, save the selected preview as PNG, or export a deliberately slowed frame/field GIF. **Open in Stella** launches the currently converted ROM in an existing Stella installation.

**Open in Stella** checks the standard Program Files installation folders, or uses your saved custom location. If Stella is missing, it offers to locate **Stella.exe** and explains that you need to install Stella if you do not already have it. A manually selected location is saved in `%LOCALAPPDATA%\Chrono2 Studio\preferences.json` (the retained compatibility location), separate from image settings and exported bundles. It writes the current conversion to a temporary BIN or MVC file and launches Stella in NTSC with the correct cartridge type (4K, F8, F6, BUS, DPC+, CDF or MVC). Use **Locate / change Stella…** in the Palette tab to select another installation. The application does not download Stella.

In **Fill / crop**, click and drag the **Adjusted input** image to move the picture within the crop. Its preview follows the drag and the output reconverts after you release. Movement stops at the source edges, so the crop always remains filled. **Center crop** restores the centered position. Shift-drag pans a zoomed input preview without changing the crop; output-preview dragging continues to pan normally. Crop position is saved in conversion settings and resets when opening a new image or resetting image adjustments.

### Optimize input

**Adjust input to palette** is a one-shot fit of brightness, contrast, gamma, saturation and RGB balance. It holds the selected palette fixed, including every color in per-row palettes. All resulting adjustments appear in the sliders. It does not enable Optimize input or perform a palette search.

Checking **Optimize input** performs the same kind of input fit. Unchecking freezes the visible adjustments; checking again refits. With this checkbox enabled, **Optimize palette** alternates input fitting, palette search on the adjusted image, and another input fit for up to three passes. It shows completed passes and retains the best measured result. With it unchecked, palette search leaves the input controls alone.

**Flicker-aware optimization** defaults to enabled and is available for temporal modes. It starts its search with darker, higher-contrast candidates and scores the actual frame mixture, color/chroma error, edges, shadow detail, loss of variation and frame-to-frame luminance changes. It does not apply candidate-specific exposure compensation. Naturally solid input may remain solid. Turning it off selects the prior exposure-adapted scoring model; static modes always use that model.

The reference stays fixed during each operation, with neutral tone and RGB gains. The flicker model uses a conservative fixed reference peak: 50% for MovieCart's half-duty cells and 75% for other temporal modes. The latter is a tuning heuristic, not a measured Atari brightness law. The NTSC palette, encoded-RGB mixture and flicker penalty are estimates, not a calibrated CRT model. Darker input is a candidate, not a compulsory result. Classic mode always retains its original RGB output colors.

**Global optimize** runs a broader joint search even if Optimize input is unchecked, including an additional input-control refinement sweep, multiple palette starts in Custom mode and up to four alternating passes per start. It keeps the best measured result including the starting conversion. This is a bounded heuristic, not a guarantee of a mathematical or subjective optimum. Crop, resampling, dither and sharpness remain selected by the user.

**Reset all options**, beside Open image, restores conversion defaults and display zoom, closes the rendering preview, cancels pending optimization and keeps the loaded image. It does not remove the saved Stella location. **Reset image adjustments** remains available for resetting just the image controls.

**Balance flicker frames** defaults to on for temporal modes. For row-based Chronocolour and two-frame sprite modes, it rearranges legal per-row phases to reduce whole-frame and local brightness imbalance without changing the exact blended RGB image. Two-frame row searches use a common background to permit those swaps. Equivalent two-frame pixels can alternate in a checkerboard. It never changes cartridge timing. Turn it off to compare the unbalanced conversion.

Classic RGB already rotates its component order by scanline; that kernel remains unchanged. MovieCart already interleaves fixed alternating cells. Those cells cannot be arbitrarily reassigned; the optimizer penalizes frame imbalance, but the phase balancer does not alter MovieCart's fixed pattern. Equal frame brightness and flicker-free temporal output are not guaranteed.

### Output modes

Select **Output mode** at the top of the Image tab. Cartridge modes export standalone ASM and headerless NTSC BIN files. MovieCart exports a real `.mvc` stream with settings and image data. Sizes and mapper types are shown in the program.

| Mode | Image | Colors and temporal behavior |
| --- | --- | --- |
| Chronocolor classic — Flicker | 48×128 | Locks original RGB components and black background; three-frame temporal mixture. |
| Chronocolor custom — Flicker | 48×128 | Custom components/background; original or improved palette search; three-frame mixture. |
| Two Color — Static | 48×128 | One solid foreground and background, identical on every frame; exhaustive legal color-pair search. |
| Chronocolor per line — Flicker | 48×128 | Three component colors chosen independently for each row; one shared background; temporal mixture. |
| Scanline color — Static | 48×128 | A foreground color per row and one shared background; identical frames. |
| No flicker — playfield — Static | 40×192 | A separately selected foreground/background pair per row, full playfield width, identical frames. |
| Playfield Plus — Static | 40×192 | Up to four solid colors per row: left/right score colors plus a timed background change. Static 16 KB F6 ROM. |
| Bus stuffing (experimental) — Static | 16×192 | Independent NTSC colors at coarse horizontal samples; 32 KB BUS2. |
| Multiplexed sprites — Static | 48×192 | Static six-strip sprite raster; one foreground per row, shared background; 4 KB. |
| DPC+ sprites — Static | 48×192 | Two foregrounds per row across alternating sprite strips; shared background; 32 KB DPC+. |
| CDFJ+ sprites — Static | 48×192 | Same static display, driven by CDFJ+ streams and an ARM initializer; 32 KB. |
| MovieCart frame — Flicker | 80×192 | 190 content rows, cell colors and row backgrounds, two alternating fields; 30-second silent MVC stream. |
| Two Color (2 frames) — Flicker | 48×128 | Two independently chosen foreground/background pairs; four temporal mixtures; 8 KB F8. |
| Scanline color (2 frames) — Flicker | 48×128 | Foreground per row in each frame; a background per frame; 8 KB F8. |
| Multiplexed sprites (2 frames) — Flicker | 48×192 | Foreground per row in each frame; a background per frame; 8 KB F8. |
| DPC+ sprites (2 frames) — Flicker | 48×192 | Separate P0/P1 colors per row in each frame; background per frame; 32 KB DPC+. |
| CDFJ+ sprites (2 frames) — Flicker | 48×192 | Same two-frame constraints, with CDFJ+ streams; 32 KB CDFJ+. |

Scanline modes fit their row palettes automatically on initial conversion. Optimize palette refits them after edits. Per-line temporal search uses a bounded coordinate search; static row/pair fitting evaluates all allowed hardware colors. Those mode-specific searches supersede the classic/custom search selector, which is disabled when inapplicable. The playfield mode initially selects Any Atari color for its background search, allowing both colors to change per row; Black and Black or white constraints remain available. Sprite modes select a shared background before fitting individual rows.

Scanline palettes are saved with settings. Swatches display the middle row; they are not a claim that the entire raster has one palette. Flicker-free means the image data and colors repeat each television frame: normal CRT refresh and display characteristics still apply. The finer-resolution modes constrain colors by row or region; the experimental BUS raster instead allows arbitrary NTSC colors at just 16 samples across. See [RESEARCH.md](RESEARCH.md) for source material, cycle budgets, trade-offs and verification.

### Playfield Plus

This mode fits separate left and right color pairs on every row. **Score mode** routes the left foreground through COLUP0 and the right through COLUP1. A timed COLUBK write changes the background during the line. The result repeats every frame, with no temporal color cycling.

The background changes at television x=76 and the score foreground changes at x=80. That one-playfield-pixel offset is intentional: exact CPU timing cannot put this COLUBK write at x=80. Logical pixel 19 therefore chooses between the left foreground and right background. Preview, dithering and exports use that same constraint, avoiding a partial-pixel seam. Other pixels choose from their side's pair; this is not unrestricted four-color selection at every pixel.

Entering the mode selects **Any Atari color** for background search. Black or Black/white restrictions remain available. Input fitting, Global optimize, crop, resampling and all dithers work with the spatial palette. Color swatches are read-only samples of the middle row, labeled L FG, L BG, R FG and R BG.

Exports are standard **16,384-byte F6** cartridges. Open in Stella automatically selects F6. Other emulators or cartridges must support F6; do not force the older 4K format. Hardware/Harmony validation remains outstanding.

### Editing palette colors

Manual component editing applies to Chronocolor custom and Two Color. Classic locks RGB; scanline-mode swatches are read-only middle-row samples, with colors fitted independently by the optimizer.

The eight output swatches **0–7** are followed by **Component 1, 2, 3 and Background** previews. Click a component to choose from the 128 valid NTSC colors. Clicking an output mixture opens the picker with its contributing components. The dialog previews all eight resulting mixtures; **Apply colors** commits the changes, while Cancel leaves the current palette untouched. Output colors cannot be edited independently because the cartridge derives them from the same four hardware colors.

### Animated cartridge preview

**ATARI Rendering Preview** opens a separate window using the completed conversion’s actual stored frames in cartridge order. Nominal NTSC pace is approximately 60 frames per second: a three-frame cycle is about 20 Hz, a two-frame cycle about 30 Hz. It displays the frames themselves, with optional persistence, rather than only their static average.

Static modes show one image and identify themselves as static. Two-frame modes show two frames; Chronocolor modes show three. The main output selector follows the same frame count.

Use Pause/Play, Next frame, or slower 30/10/3 fps playback. Space toggles playback, Right Arrow steps one frame, and Escape closes this preview window. Phosphor persistence starts at **60%** and adds an illustrative trail from preceding frames; set it to zero for raw frame cycling. Resizing preserves the chosen image geometry and crisp pixels. Reopening the preview loads the latest completed conversion into the same window.

This remains a desktop simulation, not an emulator or a prediction of an exact CRT. Timing is not synchronized to monitor refresh. The window reports software frame updates and skipped phases; it cannot measure which frames your display actually presents. Slow motion deliberately changes the timing. Use the existing Stella action or hardware to validate the cartridge's real execution.

### Geometry and preview meaning

The default **Atari pixels 2:1** follows the historical instructions: 48×128 logical pixels occupy roughly a 96×128 image area. The entire television screen is not filled by that image. Existing 48×128 inputs are treated as already prepared logical pixels. Raw-pixel view and a 4:3 stretched image view are also available; they do not change the cartridge dimensions.

The temporal preview averages the stored NTSC frame values; it is not a CRT simulation. Real phosphors, emulator phosphor blending and frame capture timing affect brightness and flicker. The original RGB target option uses ideal RGB values to choose indices while the temporal preview still shows the estimated Atari blend. This distinction is intentional.

### Palette search

New sessions default to **Improved weighted** with a **Black** background. Loading saved settings retains their selected search and background.

**Legacy exhaustive** retains the historical C-mode representative-color method, Euclidean palette objective and descending component traversal. The background selector offers **Black**, **Black or white**, and **Any Atari color** in both search models. Any Atari color extends the legacy search to all 128 NTSC background codes, evaluating 128 times as many candidates as black-only (64 times as many as black/white). Progress and cancellation remain available; a zero-error palette can finish early because it is already an exact match. The optional diversity preference favors use of more mixture colors. Unsafe array bounds and short-color-image behavior are corrected. Floating-point diffusion and corrected edge cases mean this is not a promise of pixel-for-pixel identity with every old executable.

**Improved weighted** uses a bounded color histogram and deterministic multi-start coordinate search over valid Atari colors. Frequent colors influence the score; all four hardware colors can be searched, including arbitrary background colors. This is a heuristic, not a globally optimal result or a guarantee that every picture will look better. Compare both approaches using the same image.

The historical dither-every-candidate brute-force mode is not implemented. New scanline kernels are independent implementations, not a claim to reproduce every historical Chrono3 experiment.

## Cartridge output

The BIN is a headerless **NTSC ROM: 4096 bytes / 4K**, **8192 bytes / F8 for ordinary two-frame sprites**, **16384 bytes / F6 for Playfield Plus**, or **32768 bytes / BUS for the experimental color raster**. No assembler installation is needed to export it: the program inserts image data and colors into the selected, integrity-checked kernel template. The accompanying ASM is self-contained and can be rebuilt with DASM:

```text
dasm image.asm -f3 -oimage.bin
```

Automated tests independently assemble exports with DASM and compare every byte of each cartridge format. Classic/custom/two-color output retains the original kernel. Separate raster templates have also been exercised in Stella with exact pixel-plane and 262-line timing checks. PAL/SECAM output is not offered. Physical Atari/Harmony testing remains outstanding.

## Development and checks

```text
python -m unittest discover -s tests -v
python tests/gui_smoke.py
python tests/gui_optimization_regression.py
python tests/gui_modes_smoke.py
```

Set `DASM_PATH` to a DASM executable to enable the independent assembler parity test. `scripts/rebuild_kernel.py` rebuilds the bundled template and discovers the color operand offsets using DASM. Do this only when intentionally changing the kernel, then rerun parity tests.

`scripts/rebuild_raster.py` rebuilds all three new raster templates. `scripts/verify_stella_raster.py path/to/Stella.exe` uses isolated debugger scripts to capture three frames, check image masks, per-row colors and NTSC timing. Test output and emulator preferences stay under ignored `test-output/`.

Historical originals and ZIP releases are preserved outside this source checkout. Private research, old image collections, virtual environments, outputs and assembler binaries are not part of this public repository.

## Credits and history

- Chris Martin: original Chrono2 image converter and project direction.
- **Andrew Davie:** 2003 Interleaved Chronocolour sprite technology and cartridge kernel. His full notice remains in `chrono/resources/kernel.asm` and classic/custom/two-color exported ASM. New raster ASM acknowledges the sprite technique separately.
- **Eckhard Stohlberg and Thomas Jentzsch:** foundational sprite work and contributions acknowledged by Andrew's original source.
- Python GUI and conversion implementation developed with Codex in 2026, following the recovered FreeBASIC source and the owner's requirements.

Original discussion: [Chronocolour Enhancement](https://forums.atariage.com/topic/174658-chronocolour-enhancement/) and [New Graphics for 2600](https://forums.atariage.com/topic/175649-new-graphics-for-2600/).

No new license is asserted over third-party historical code. Retain the original notices and credit Andrew's contribution in documentation accompanying ROMs made with this kernel. See [CREDITS.md](CREDITS.md).


## Bus stuffing (experimental) — 0.2.2-dev

Choose **Bus stuffing (experimental)** under Output mode. It exports a genuine BUS2 cartridge and displays **16 × 192 independent color samples**, each free to select any of the 128 NTSC colors. Samples are nine color clocks wide; this is deliberately coarse horizontally but has no temporal flicker. All scaling, cropping, input controls and dithering remain available. The full NTSC color chart replaces component swatches. There is no restricted palette to search; Optimize input and Global optimize still adjust the image.

Open in Stella selects BUS. The 32 KiB BIN includes its cartridge driver, ARM initializer, image and timed kernel. Generated ASM rebuilds the same BIN with DASM. **Stella rendering and timing are verified; physical console/Harmony compatibility is not.** The mode is experimental and should not be treated as a portable ordinary 4K cartridge.

See [BUS-RESEARCH.md](BUS-RESEARCH.md) for exact geometry, verification, reference-driver provenance and a comparison with playfields, sprite bitmaps, Chronocolour, DPC+/CDF and MovieCart. The historical BUS driver's redistribution terms still need to be established before public release; this is currently a local experimental build.


## Cartridge support and public packaging

Third-party BUS, DPC+ and CDFJ+ driver bytes are **not included** in this repository or the release ZIP, including inside generated templates. The public templates contain zero-filled driver slots. Setup downloads the tested drivers from pinned upstream sources and validates SHA-256; BIN export inserts the locally fetched support bytes. Normal first launch handles setup; `Setup cartridge support.cmd` retries it. Other modes remain usable if that optional download fails.

The original authors retain their rights. CREDITS.md and ADVANCED-MODES.md link the sources. The fetch mechanism does not grant a new license to redistribute those drivers or ROMs containing them. Their redistribution terms remain an upstream matter.

The historical `Run Chrono2.cmd` remains a compatibility launcher. Existing settings, repository URLs and machine-local Stella preferences continue to work. Historical Chrono2 files are not renamed.
