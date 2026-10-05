# Atari 2600 Image Optimizer 0.5.0 — October 5, 2026

A portable Windows x64 build now runs without a separate Python installation. Extract the whole Windows ZIP and launch the EXE; keep its `_internal` folder beside it. The source-and-launcher ZIP remains available.

- Twenty NTSC output modes. New choices: Hybrid playfield + sprites (Static), 96-pixel interleaved bitmap (Flicker), and Television interlace (experimental, Flicker).
- A simpler workbench: choose Image + colors, Image only, or Colors only before optimizing. Compare and undo optimization; use crop zoom and drag positioning to choose a smaller source area, including with Stretch.
- Shared linear-light temporal blending and CIEDE2000 color matching across all modes. Original Chronocolor image optimization applies the requested fixed 0.47 brightness preset while preserving other controls.
- Corrected error diffusion: preserve signed residuals, bound impossible palette colors before diffusion, and keep exact black source pixels black when the palette contains black.
- Export looping WebP previews with playback speed, persistence and size options. Exports capture the completed conversion and preserve its frame sequence. Static modes export a still image.

## Windows setup

No Python or assembler installation is needed for the standalone. Basic conversions, previews and ordinary cartridge exports work offline. For BUS, DPC+ and CDFJ+ cartridge exports, run **Setup cartridge support.cmd** and click **Download cartridge support**. It retrieves the original upstream bytes, verifies pinned checksums, and caches them in the current user's LocalAppData. These optional driver binaries are not redistributed in either package. Stella must be installed separately if desired.

The Windows application is unsigned. This release targets Windows x64; it is not an ARM64 or macOS executable.

## Validation and limits

Automated conversion, GUI, dithering, color-model and independent DASM parity checks cover the source. The standalone is additionally checked from its extracted folder with system Python absent from PATH, exercising all twenty modes, exported previews, cartridge data, image import and the rendering window. Earlier Stella timing/pixel verification is documented in VALIDATION.md; no new physical Atari, Harmony or MovieCart validation is claimed. Television interlace and BUS remain experimental. Browser preview timing, CRT persistence and colors differ across displays.

Credits remain with Andrew Davie and the other original contributors named in CREDITS.md. No historical sample-image collection is included in the software downloads.

---

# Atari 2600 Image Optimizer 0.4.0 — October 3, 2026

The Python continuation of Chrono2 is now Atari 2600 Image Optimizer. Historical files and existing repository links remain intact.

- 17 NTSC display choices, each labeled Static or Flicker, including two-frame variants of Two Color, scanline color, multiplexed sprites, DPC+ and CDFJ+.
- Flicker-aware input/palette optimization, enabled by default for temporal output; separate input-to-palette fitting includes tone and RGB balance.
- Frame balancing rearranges legal scanline phases or equivalent pixels while preserving the blended picture. Classic RGB and MovieCart keep their existing interleaving patterns; frame-to-frame brightness is included in flicker scoring.
- ATARI Rendering Preview shows the actual frame count; Reset all options keeps the loaded image.
- Crop by dragging, common image adjustments and dithers, saved settings, direct ASM/BIN export, MovieCart MVC export, and Stella launching.

## Run

Install Python 3.12 or newer with Tkinter, extract the ZIP, then double-click **Run Atari 2600 Image Optimizer.cmd**. First launch installs NumPy/Pillow and retrieves optional cartridge support from its original upstream sources, checking pinned SHA-256 values. Subsequent use is offline once setup completes. This is a source-and-launcher package, not a standalone EXE. The old launcher still works.

Third-party BUS/DPC+/CDFJ+ driver bytes are excluded from both Git and the ZIP, including embedded copies. Their upstream attribution and rights remain applicable to locally generated ROMs.

## Validation and limits

Automated tests, GUI checks, independent DASM assembly parity, and Stella pixel/timing checks pass. Stella verifies 262-line NTSC timing and actual alternating frames, including the balanced row phases. This is not physical Atari, Harmony, Melody or MovieCart validation. Preview colors and persistence are estimates; temporal modes still flicker. The optimizer is a bounded heuristic. MovieCart produces a separate still-image stream, not a Harmony BIN.

Original Chronocolour work: Andrew Davie, with acknowledgements to Eckhard Stohlberg and Thomas Jentzsch. Further driver and format credits are in CREDITS.md.
