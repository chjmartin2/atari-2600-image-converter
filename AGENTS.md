# Atari 2600 Image Optimizer

Project ID: `atari-2600-image-converter`.

Preserve the original historical source and releases outside this checkout. This Python repository is the maintained implementation. Do not alter the NTSC kernel or cartridge packing without assembler parity tests and Stella verification. Never describe emulator checks as physical Harmony validation.

Whenever asked to push to GitHub or publish a release, read the current universal instructions at `D:\RetroComputerist\Website\PROJECT-UPDATE-WORKFLOW.md` and follow them. Keep this pointer instead of copying the evolving website workflow. Website content requires the owner's approval before public deployment.

Run `python -m unittest discover -s tests -v`. The optional assembler parity check uses `DASM_PATH`; keep assembler tools outside Git. Use `python tests/gui_smoke.py` for a desktop smoke check. Verify new features through the GUI as well as core tests.

Before public packaging, verify that optional cartridge driver binaries and driver-bearing generated ASM remain ignored, and that public BIN templates have zero-filled driver slots. Use chrono.drivers.strip_template when rebuilding templates. Never include private backups or locally fetched drivers in a release.
