# Chrono2 Studio

A Python desktop workbench for turning pictures into **48×128 NTSC Atari 2600 cartridge images**. This continues Chris Martin's 2011 Chrono2 converter, using Andrew Davie's original Interleaved Chronocolour display kernel.

Version **0.1.0** is an initial development build. It preserves the original 4 KB cartridge layout and adds a modern image preparation and preview interface. It is not a FreeBASIC restoration.

## Run

On Windows, double-click **Run Chrono2.cmd**. Python 3.12 or newer with Tkinter is required. The first run creates `.venv` and installs NumPy and Pillow. Subsequent runs use that environment. The owner's local project already has this environment prepared.

Alternatively:

```text
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python run.py
```

Pass an image path to `run.py` or drop it onto the launcher. The application starts with an original calibration image when no file is supplied.

## Image workflow

1. Open PNG, JPEG, BMP, GIF, TIFF or WebP. Animated inputs use their first frame; transparency is composited over black. EXIF orientation is honored.
2. Choose fit, fill/crop or stretch; nearest, box, bilinear, Hamming, bicubic or Lanczos resampling; rotation and horizontal mirror.
3. Adjust brightness, contrast, saturation, gamma, sharpness and individual RGB gains. Changes automatically refresh the conversion.
4. Select a preset or four NTSC color codes. Presets include original RGB, grayscale, sepia, neon, pink, blue and a CGA-inspired magenta/cyan/black combination. These are Atari approximations: all eight output colors are mixtures of three hardware colors and a background.
5. Select no dithering, ordered 2×2/4×4/8×8, Floyd–Steinberg, Atkinson, Jarvis–Judice–Ninke, Stucki, Sierra or Burkes. Error diffusion supports serpentine traversal and a strength control.
6. Convert with that palette, or choose either search model and press **Optimize palette**. Searches run in the background and support cancellation.
7. Inspect the temporal-blend estimate, quantization targets or individual component frames. Use fit-to-window or fixed zoom, crisp/smooth display and drag-to-pan.
8. Export ASM + BIN. A new export folder contains `image.asm`, `image.bin`, `settings.json`, `preview.png` and attribution/readme text. Export is blocked while conversion is unfinished or settings are stale.

Save/load settings independently, save the selected preview as PNG, or export a deliberately slowed three-frame GIF. **Open in Stella** launches the currently converted ROM in an existing Stella installation.

### Geometry and preview meaning

The default **Atari pixels 2:1** follows the historical instructions: 48×128 logical pixels occupy roughly a 96×128 image area. The entire television screen is not filled by that image. Existing 48×128 inputs are treated as already prepared logical pixels. Raw-pixel view and a 4:3 stretched image view are also available; they do not change the cartridge dimensions.

The preview averages the three stored NTSC palette values; it is not a CRT simulation. Real phosphors, emulator phosphor blending and frame capture timing affect brightness and flicker. The original RGB target option uses ideal RGB values to choose indices while the temporal preview still shows the estimated Atari blend. This distinction is intentional.

### Palette search

**Legacy exhaustive** retains the historical C-mode representative-color method, Euclidean palette objective, descending traversal and black/white background choices. The optional diversity preference favors use of more mixture colors. Unsafe array bounds and short-color-image behavior are corrected. Floating-point diffusion and corrected edge cases mean this is not a promise of pixel-for-pixel identity with every old executable.

**Improved weighted** uses a bounded color histogram and deterministic multi-start coordinate search over valid Atari colors. Frequent colors influence the score; all four hardware colors can be searched, including arbitrary background colors. This is a heuristic, not a globally optimal result or a guarantee that every picture will look better. Compare both approaches using the same image.

The historical dither-every-candidate brute-force mode and later Chrono3 per-scanline experiments are not implemented in this version.

## Cartridge output

The BIN is a headerless standard **4096-byte NTSC / 4K ROM**. No assembler installation is needed to export it: the program inserts image data and four verified color operands into the bundled original kernel. The accompanying ASM is self-contained and can be rebuilt with DASM:

```text
dasm image.asm -f3 -oimage.bin
```

Automated tests independently assemble exports with DASM and compare all 4096 bytes. The original sprite kernel, frame ordering, scanline timing and reset vectors are retained. PAL/SECAM output is not offered. Physical Atari/Harmony compatibility still needs hardware testing; a valid 4K ROM and emulator testing do not establish that every cartridge setup has been tested.

## Development and checks

```text
python -m unittest discover -s tests -v
python tests/gui_smoke.py
```

Set `DASM_PATH` to a DASM executable to enable the independent assembler parity test. `scripts/rebuild_kernel.py` rebuilds the bundled template and discovers the color operand offsets using DASM. Do this only when intentionally changing the kernel, then rerun parity tests.

Historical originals and ZIP releases are preserved outside this source checkout. Private research, old image collections, virtual environments, outputs and assembler binaries are not part of this public repository.

## Credits and history

- Chris Martin: original Chrono2 image converter and project direction.
- **Andrew Davie:** 2003 Interleaved Chronocolour sprite technology and cartridge kernel. His full notice remains in `chrono/resources/kernel.asm` and every exported ASM.
- **Eckhard Stohlberg and Thomas Jentzsch:** foundational sprite work and contributions acknowledged by Andrew's original source.
- Python GUI and conversion implementation developed with Codex in 2026, following the recovered FreeBASIC source and the owner's requirements.

Original discussion: [Chronocolour Enhancement](https://forums.atariage.com/topic/174658-chronocolour-enhancement/) and [New Graphics for 2600](https://forums.atariage.com/topic/175649-new-graphics-for-2600/).

No new license is asserted over third-party historical code. Retain the original notices and credit Andrew's contribution in documentation accompanying ROMs made with this kernel. See [CREDITS.md](CREDITS.md).
