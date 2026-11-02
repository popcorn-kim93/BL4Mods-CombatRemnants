# Compatibility and validation — v0.11.0 Alpha

## Tested environment

| Item | Observed value |
| --- | --- |
| Game | Borderlands 4, Steam, Windows x64 |
| In-game test date | 2026-11-02 (Korea Standard Time) |
| unrealsdk | v3.2.0, revision b1852aa4 |
| pyunrealsdk | v1.10.0, revision c72c5558 |
| Native module | BL4RemovalTrace-abi9.dll |

These SDK versions describe the test environment, not a compatibility guarantee for all newer or older versions.

The tested executable's SHA-256 is:

```text
ba75f7c2874b16efb5536a5c0cc28918a03efd3e55d790d2e4db57de0c3a353a
```

Its PE timestamp is `4086165580` and image size is `652288000` bytes. The mod validates executable layout and selected code fingerprints before enabling native protection. The SHA-256 above identifies the tested file; the runtime check is not a whole-file hash comparison. Updates to the game may require an updated mod.

## What was observed

The latest in-game test lasted about 213 seconds with `bl4_corpses_on --max-corpses 5`:

- 76 corpses were registered; 71 received count-based cleanup requests.
- All 457 observed severed parts were linked to an owner.
- Five corpses and eight linked parts remained immediately before stop; the final corpse queue matched the latest five deaths.
- No protected corpse destruction was recorded. Twenty-three part removals followed the known out-of-world cleanup call path, which remains permitted.
- The tester reported that bodies and parts generally stayed together on screen.
- No capture errors or dropped events were recorded, and all native hooks were restored on stop.

The final five corpses were only approximately 10–19 seconds old. This test establishes the observed grouping and count policy, not long-idle persistence or complete coverage of all visual effects. Counts are runtime records and are not a substitute for on-screen observation.

The public package preserves the 19 runtime files from the tested build byte for byte. Local grouping/native checks and package-integrity checks are separate from in-game qualification.

## Limits

- Current scope: eligible enemy corpses and severed parts with verified owner links. Blood/bullet/blast decals and general Niagara particles are not retained by this release.
- World changes, explicit forced destruction and out-of-world cleanup remain allowed. Unassociated parts use the game's normal lifetime.
- Long sessions, large counts, all enemies/areas, multiplayer and other storefront builds have not been qualified. Retaining more objects can increase resource use; there is no measured frame-rate guarantee.
- The native watch table has a capacity of 8,192 identities shared by prepared living NPCs, corpses and linked parts. This is an internal capacity, not a separate limb limit. Exceeding it is reported as an error.
- Session diagnostics are written to disk while active. Detailed material tracing is disabled by default.
- Mod updates require exiting the game because the native DLL remains loaded in the process.
