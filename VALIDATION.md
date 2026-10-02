# Validation record — 2026-10-02

Initial Python development build 0.1.0, Windows, Python 3.12, NumPy 2.5.3, Pillow 12.3.0.

- 12 automated tests passed, including every preset/dither combination, scaling filters, image adjustments, settings round-trip, transparent image import, cancellation, deterministic weighted optimization and a complete legacy search.
- Independent DASM assembly matched the generated BIN byte for byte for all seven presets plus twelve deterministic randomized four-color sets and randomized pixel data. Every output was exactly 4096 bytes with valid cartridge reset vectors.
- Bit-order tests and an independent unpacking round-trip checked all three frames, bottom-up rows, six sprite strips, component rotation and frame headers. Estimated temporal colors matched the average of the three component frames.
- GUI event-loop smoke check passed import, all presets, adjustment, dither, optimization, five views, zoom, export, settings reload and reset. Window-size checks keep the export controls visible at 1000×700 and 1320×850.
- A native desktop visual inspection revealed an export-row problem at high display scaling. Settings panels were made scrollable and export/status rows reserved. The revised layout passed the programmatic GUI checks.
- **Stella visual execution is not yet verified.** Desktop control was stopped by the user during visual testing. No physical Atari or Harmony test is claimed. The ROM kernel and format are preserved, but emulator/hardware validation remains an explicit next check.

Run the tests again after changing conversion or cartridge code. The optional assembler test requires `DASM_PATH`; a skipped assembler test is not an assembler pass. The GUI smoke test requires a desktop and creates a temporary application window.
