# Validation record — 2026-10-02

Initial Python development build 0.1.0, Windows, Python 3.12, NumPy 2.5.3, Pillow 12.3.0.

- 12 automated tests passed, including every preset/dither combination, scaling filters, image adjustments, settings round-trip, transparent image import, cancellation, deterministic weighted optimization and a complete legacy search.
- Independent DASM assembly matched the generated BIN byte for byte for all seven presets plus twelve deterministic randomized four-color sets and randomized pixel data. Every output was exactly 4096 bytes with valid cartridge reset vectors.
- Bit-order tests and an independent unpacking round-trip checked all three frames, bottom-up rows, six sprite strips, component rotation and frame headers. Estimated temporal colors matched the average of the three component frames.
- GUI event-loop smoke check passed import, all presets, adjustment, dither, optimization, five views, zoom, export, settings reload and reset. Window-size checks keep the export controls visible at 1000×700 and 1320×850.
- A native desktop visual inspection revealed an export-row problem at high display scaling. Settings panels were made scrollable and export/status rows reserved. The revised layout passed the programmatic GUI checks.
- **Stella visual execution is not yet verified.** Desktop control was stopped by the user during visual testing. No physical Atari or Harmony test is claimed. The ROM kernel and format are preserved, but emulator/hardware validation remains an explicit next check.

Run the tests again after changing conversion or cartridge code. The optional assembler test requires `DASM_PATH`; a skipped assembler test is not an assembler pass. The GUI smoke test requires a desktop and creates a temporary application window.

## Animated preview and input optimization update

20 automated tests now pass, including DASM parity. New checks cover elapsed-time animation phase, dropped callbacks, pause/resume, speed changes, stepping, raw component-frame identity, optional persistence weighting, input-tone range matching, preservation of image detail, flat channels, cancellation and repeat-click stability.

The GUI smoke check additionally exercises the animated window's playback, pause, step, speed, persistence, resizing, reuse, closing and reopening; it also runs input optimization and verifies that Undo restores the exact preceding brightness/contrast values. These are application event-loop checks, not monitor-refresh, CRT or hardware measurements. The emulator/hardware limits above still apply.

## Legacy search background extension

23 automated tests pass. Added checks verify a colored-background exact match using real scoring, all 128 candidate background codes, restricted Black and Black or white selections, preservation of diversity scoring, and cancellation after startup. The GUI smoke check selects Legacy exhaustive plus Any Atari color and completes a conversion. Candidate totals are computed from compact component ranges and progress callbacks are throttled so the expanded search does not stall during counting or flood the GUI queue. No exhaustive full-image benchmark for all background colors is claimed.

## Draggable Fill / crop

28 automated tests pass, including source-region selection at both crop edges, horizontal/vertical movement and clamping, rotated geometry, prepared 48×128 inputs, unchanged Fit/Stretch behavior, saved crop settings and compatibility with old settings files. The GUI smoke check sends mouse press/drag/release events through the actual input-preview bindings, verifies the completed conversion retains the new crop, and checks Center crop. Drag offsets are used by the common preparation path, so conversion and both optimization controls use the same selected source region.

## Palette-dependent Optimize input selector and defaults

32 automated tests pass. Tests verify that each candidate's tonal transform exactly matches final image preparation, both search models pass candidate-specific tone context into scoring, a collapsed black palette is penalized for lost detail, and toggling/saving/loading the option preserves manual controls. The GUI smoke check enables the selector, runs a joint palette/input search, verifies the displayed input equals preparation with the winning settings, and disables the option again. Default settings select Fill / crop, and a newly opened animated preview starts at 60% persistence. The selector replaces the previous one-shot input-optimization and Undo buttons; its automatic adjustment is applied after the unchanged manual sliders.

## Visible input adjustments and palette picker (supersedes selector behavior above)

Optimize input now fits the visible brightness/contrast controls. There is no automatic filter in preparation: turning the checkbox off keeps identical adjusted pixels and output indices. Re-enabling fits the current palette from a neutral brightness/contrast baseline. Palette search still scores candidate-specific tonal targets, then fits the winning palette with actual controls; the range estimate is approximate, not identical to the fitted result.

33 automated tests pass, including DASM parity, off-state preservation, refitting a different palette and repeat stability. The GUI smoke check verifies slider updates after input and palette optimization, frozen pixels/indices when unchecked, refitting, component picker apply/cancel, derived-background editing, and swatch layout at 1000 and 1320 pixels. It also checks default Legacy exhaustive / Black selection; Fill / crop and 60% persistence remain defaults. Prior export, crop, animation and settings checks remain in the suite. Emulator and physical hardware limitations above still apply.

## Stella discovery and revised palette default

The default is now Improved weighted / Black. Open in Stella uses a saved custom location or checks standard Program Files installation folders; if none is found, it offers Locate Stella and installation guidance. Custom selections are stored in machine-local preferences.

37 automated tests and the GUI smoke check pass. New coverage checks default and 32-bit installation paths, saved custom paths, moved executables, malformed preferences, invalid selections, install guidance/cancel, first selection and remembered reuse, the temporary 4096-byte ROM and NTSC / 4K launch arguments, and launch failure handling. GUI launch checks mock the external process; this does not establish actual Stella rendering or hardware validation. DASM parity still passes.

## Optimization request handling regression

Reproduced two lost-operation bugs: changing a slider after queuing Optimize palette replaced the search with a plain conversion (zero search calls); changing a control during input fitting discarded the fitted result and never retried, leaving brightness at 1.0 instead of the returned 0.45. Pending search/input-fit requests now survive preview refreshes. Changed settings cancel stale work and restart the requested operation against current controls. Turning Optimize input off suppresses refitting, and Cancel clears pending operations.

The 37 core tests and existing GUI smoke check pass. `tests/gui_optimization_regression.py` additionally invokes actual buttons/checkboxes with controlled worker timing and verifies queued palette search, input-fit retry after edits, disabling during a fit, and cancellation. These tests cover request handling; they do not establish subjective image quality for every input.

## Six output modes and perceptual optimizer — 2026-10-03

This section supersedes the earlier unverified-Stella status for the new raster kernels and the earlier candidate-specific range estimate in the active optimizer. The original kernel files remain unchanged.

- 44 unit tests pass with DASM enabled. Independent assembly matches direct 4,096-byte BIN output for both new raster templates as well as the original kernel.
- The standard GUI smoke test, pending-operation regression test, and six-mode GUI test pass. Coverage includes row-palette save/reload identity, all six output selections, preview/animation, ASM/BIN exports, and Global optimize.
- Joint input/palette search uses actual slider values and retains the best result against a fixed reference. Tests check alternating passes, non-regression against the starting score, cancellation, and detail retention. Solid black, gray and white score worse than a dim but detailed version of the calibration image. This verifies the intended scoring behavior, not subjective superiority for every image.
- Stella 7.0 executes randomized 48×128 static, 48×128 temporal and 40×192 playfield ROMs through isolated debugger scripts. All have exactly 262 scanlines. Three saved frames match expected bitmap planes, including edges and register boundaries; temporal planes cycle and static planes repeat.
- Per-row foreground colors and playfield background changes also match. The verifier supplies the project's NTSC palette, applies Stella 7.0's documented-in-source default gamma transform, and permits one RGB level for its hue/saturation rounding. Pixel masks remain exact. This tests cartridge color selection, not agreement between all real displays.
- A too-late playfield register write was found and corrected during emulator testing. The final schedule is documented in RESEARCH.md.

No physical Atari, CRT or Harmony-cartridge validation is claimed. The desktop animated preview is illustrative; Stella checks use actual emulated TIA output. Development files are installed locally; no release or website deployment is implied.

## Playfield Plus — 2026-10-03

- 46 unit tests pass (44 existing/extended tests plus two Playfield Plus tests), with DASM parity enabled. The new tests verify spatial color constraints, all dither methods, four-color static output, invalid export data, and ordered dithering with duplicate palette entries. Ordered dithering now selects a second distinct color, fixing its use with solid two-color modes as well.
- All seven GUI modes pass, including settings save/reload, preview, animation, export, Global optimize and the F6 argument for Open in Stella. The standard GUI smoke and pending-operation regression checks also pass.
- The 16,384-byte F6 ROM passes Stella's 262-line timing test and three-frame identity. Every captured pixel matches the spatial palette/bitmap model across all rows, including the 64/128-row bank transitions and the midline background change. Color comparison permits two RGB levels for Stella's rounding, superseding the earlier one-level tolerance.
- The center timing seam found during development is eliminated by aligning the background change to x=76; the score foreground split stays at x=80. Preview and quantization use that exact layout.

No GitHub release, website deployment or physical hardware validation is implied by this local development update.


## BUS color raster — 2026-10-03

- 51 unit tests pass with DASM parity enabled. The five new BUS tests check every dither against all NTSC colors, static frame identity, settings round-trip, cancellation, invalid dimensions/indices, stream-byte packing, independent assembly/export parity, and Global optimize detail preservation.
- Standard GUI smoke and all-eight-mode GUI checks pass. BUS conversion, palette chart, all preview views, animated/static window, settings restore, ASM/BIN export and Global optimize are exercised. Open in Stella uses the BUS mapper. Existing 4K and F6 modes retain their formats.
- `scripts/verify_stella_bus.py` runs the actual 32 KiB BUS2 ROM in Stella 7.0, with randomized colors. Three consecutive captured frames match all 3072 samples across the 192 rows and both bank transitions. Active bounds in Stella's 2x horizontal capture are x=14..301 (144 TIA clocks), y=15..206. Frame timing is exactly 262 lines; RGB tolerance is two channel levels for Stella palette rounding.
- The 6507 loop performs stuffed STY COLUBK writes; its data is initialized in cartridge RAM by the generated Thumb routine. This does not merely label an ordinary ROM as BUS. A reserved-register-space startup issue was found and fixed before verification; code starts at F040.
- Preview geometry reflects the cropped 144-clock-wide image area, whose display aspect is 6:5 inside the usual 4:3 full raster. The preview omits the ROM's black side borders.

Physical console/Harmony BUS support remains unverified. The historical driver has recorded provenance but its redistribution terms need confirmation before public release. No GitHub push, release, or website change was performed.


## 0.3.0-dev advanced modes (2026-10-03)

- 55 unit tests passed with DASM_PATH configured, including all assembler parity checks (no skips).
- Existing desktop GUI smoke passed, including image adjustment fitting, freeze/refit, joint search, palette picker, crop, animation and exports.
- All twelve mode GUI smoke passed, including MovieCart settings reload, two-field animation, MVC export, input/global optimization, and correct Stella mapper/file routing.
- New ordinary multiplexed sprites, DPC+ sprites and CDFJ+ sprites: all pixels matched Stella 7.0 over three successive static frames; each frame measured 262 lines. Random bit patterns, different row colors and sprite-strip boundaries were checked.
- MovieCart: both alternating fields matched all expected pixels in separate Stella runs with random graphics, cell colors and row backgrounds. Each field measured 262 lines. 80 x 192 samples with 190 safe content rows; two blank boundary rows and a black first-content-row background are enforced.
- The visible kernels are emulator-verified, not validated on physical Atari, Harmony, Melody or MovieCart hardware. CDFJ+ is the implemented CDF-family variant.
- See ADVANCED-MODES.md for driver provenance, stream geometry and reproducible validation commands. No public GitHub release or website update was performed.


## 0.4.0-dev flicker optimization and two-frame modes (2026-10-03)

- 62 unit tests passed with DASM enabled, with no skips. New tests cover saved flicker opt-out, temporal-difference cost, resistance to collapsed images, fixed-palette tone/RGB fitting, full row-table preservation, cancellation, Classic RGB preservation and non-regression against the same scoring objective.
- All five two-frame modes round-trip settings and reproduce their exact mean palette. Generated ASM matches direct BIN byte for byte with randomized graphics and nonblack backgrounds in both frames.
- Stella 7.0 verifies all pixels in three successive alternating frames for Two Color, Scanline color, Multiplexed sprites, DPC+ sprites and CDFJ+ sprites. Every captured frame has 262 scanlines. Tests permit at most two RGB levels of palette-rounding difference. The first three modes captured B/A/B; DPC+/CDFJ+ captured A/B/A.
- Standard GUI smoke, all-seventeen-mode GUI/export checks, pending-operation regression checks and the new flicker-controls GUI check passed. New GUI coverage includes actual one-shot button invocation, visible RGB gains, unchanged row palettes, static/two-frame preview counts, checkbox applicability, and Reset all options during an active worker. Reset preserves the loaded image and discards stale results.
- The optimizer's fixed reference budgets (50% MovieCart; 75% other temporal modes) and temporal-luminance penalty are explicit heuristics. Tests establish the intended behavior, not a claim that the result is subjectively best on every image or a calibrated simulation of a CRT.
- Installed as a local development build. Physical Atari/Harmony/MovieCart operation remains unverified. No GitHub push, release or website deployment is included.


## 0.4.0 public release preparation — October 3, 2026

Application renamed to Atari 2600 Image Optimizer; legacy launcher, saved mode IDs and Stella preference location are retained. All mode descriptions now explicitly say Static or Flicker.

69 unit tests pass with DASM enabled. New temporal tests verify exact preservation of every pixel's averaged RGB, reduced phase imbalance in controlled two-/three-frame fixtures, static/disabled behavior, and settings compatibility. Palette canonicalization before quantization fixes a save/reload tie-order discrepancy. The full GUI smoke, all-17-mode export checks and flicker-controls checks pass.

Stella re-verification with the interleaved row data passes for all five two-frame modes and the static/temporal raster kernels: every pixel matches, every frame has 262 scanlines, and temporal frames alternate. No physical hardware validation is claimed.

Public packaging contains zero-filled external-driver slots, with tests to reject embedded driver bytes. All three upstream download paths independently reproduced the expected driver SHA-256 values. Locally fetched drivers and generated driver-bearing ASM are ignored; setup obtains these from the original upstream sources. Export after restoration continues to match independent DASM output exactly.

## Universal light and color model — October 5, 2026 (0.5.0 development)

This supersedes the encoded-RGB averages, palette-dependent target remapping, exposure adaptation, fixed flicker reference budgets and Classic 0.30 rule described in earlier records. Palette RGB is explicitly assumed display-referred sRGB. Temporal blending, duty cycles, persistence and diffusion operate in linear light; both palette searches, quantization and input fitting use D65 CIEDE2000. Classic still fits brightness only. Optional flicker scoring adds a separate linear-luminance cost and never darkens the input by itself.

- All 92 automated tests passed with DASM enabled and no skipped assembler checks. Coverage includes 34 published CIEDE2000 reference vectors, scalar/vector nearest-color agreement, all 256 transfer-function round trips, known half-duty and three-primary light levels, all twenty mode palettes versus actual frame light, linear-gray dither energy, fixed-reference scoring and old settings loading.
- GUI smoke checks passed ordinary editing/optimization, palette picker, crop, comparison, animation, export and settings. A separate twenty-mode GUI run passed mode selection, palette search, row-palette reload, ASM/BIN/MVC export, animation and joint optimization. Flicker GUI checks passed brightness-only Classic fitting, visible tone/RGB controls, fixed row palettes and reset during a worker.
- After deduplicating identical wide-mode color mixtures to reduce search memory/work, all eight extended-mode tests passed again, including independent DASM parity. Every legal foreground/background candidate remains in the ranking.
- Kernel templates, cartridge packing and raw hardware frame colors were not changed. Previous Stella execution checks remain historical evidence; this change was checked through math, conversion, GUI and assembler tests, not a new physical CRT or Harmony session.
- Old settings retain manual adjustments but now render through the new model. Saved settings identify `srgb-linear-light-d65-ciede2000-v1`. Reset old compensating image adjustments before evaluating the new defaults. Existing exported ROMs remain untouched.

## Original Chronocolor fixed brightness preset — October 5, 2026

At the owner's request, Original Chronocolor image optimization now sets brightness to the absolute value 0.47. It preserves contrast, input gamma, saturation, RGB gains, sharpness, geometry and the fixed Classic palette. Repeated optimization reapplies 0.47; manual brightness edits remain available. Neither search effort nor the flicker-scoring option changes this preset. Classic's search-effort control is disabled and its help text explains the fixed preset.

This replaces Classic's automatic brightness search only. The nineteen other modes and the shared light/color model remain unchanged. Code comparison confirmed that all other optimizer functions are identical apart from Classic's progress message; the nineteen remaining application modules are byte-identical. GUI checks verified the actual 0.47 slider value, retained controls, other modes' image fitting and reset behavior.

All 92 automated tests passed with DASM enabled, followed by successful Classic/flicker and general GUI smoke checks. No skipped assembler checks.

## Website animation export — October 5, 2026

Added Export animated preview above Atari Output, in File, and inside ATARI Rendering Preview. The new dialog saves lossless looping WebP with adjustable rate (60/30/10/3 fps), persistence (0–80%) and longest side (320/640/960 pixels). Main-window defaults are 60 fps, 60% persistence and 640 pixels; rendering-window export inherits that window's speed/persistence. The completed conversion is captured when the dialog opens. Static modes save a still WebP; no extra motion is invented. The older slowed GIF export is retained.

New format checks decode saved files and verify exact lossless frame colors, phase order, persistence, proportions, infinite loop metadata and 50 ms/100 ms complete cycles for three/two-frame 60 fps output. Separate checks cover static output, all modes' geometry, invalid settings and atomic-save failure preserving an existing destination. GUI checks invoke the new buttons, verify visibility at 1000x700 and 1320x850, preserve the export snapshot during later edits, and save from both windows. General GUI smoke also passed. Browser scheduling and physical CRT playback are not measured by these checks.

All 96 automated tests passed with DASM enabled and no skipped checks. New export GUI and general GUI smoke checks passed.

## Diffusion spill correction — October 5, 2026

All 103 automated tests passed with DASM enabled. Seven new regressions cover kernel normalization, unsupported highlights, signed-error energy balance, local palette bounds, exact-black preservation for all six diffusers in both scan directions, palettes without black, and an impossible hue inside the palette's RGB bounding box. General GUI smoke and the new dither GUI check passed; the latter exercises all six diffusion selections and verifies raw animated frames as well as the static output.

A reproducible comparison using the prepared Britney image at brightness 0.47 with an added black border found 214 incorrectly lit black pixels before the fix and zero afterward, across 1,667 black source pixels. This is a software regression example, not a physical CRT measurement. Classic's 0.47 preset, palette search, temporal blending, kernel templates and cartridge packing remain unchanged.

## Windows standalone release 0.5.0 — October 5, 2026

The Windows x64 folder bundle includes Python, NumPy, Pillow and Tk through PyInstaller 6.22.3. A clean-user smoke run with system Python absent from PATH passed conversion and WebP export for all twenty modes, ordinary cartridge/MVC exports, image import, the GUI and rendering window. Missing optional driver exports reported the setup instructions. A second run with the private, checksum-verified driver cache passed exports for all twenty modes as well. Neither the cache nor test exports enter the distribution. The EXE is unsigned; physical Atari/cartridge validation remains outstanding.

Source GUI and animated-export GUI checks passed. Public packaging checks preserve zero-filled driver slots and omit driver binaries and driver-bearing ASM. The new standalone caches optional cartridge support in LocalAppData; source checkouts retain their existing resource location.

Release gate: all 105 unit tests passed with DASM enabled; general GUI and animated-export GUI checks passed. Both packaged standalone self-tests passed with system Python absent from PATH.
