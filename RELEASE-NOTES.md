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
