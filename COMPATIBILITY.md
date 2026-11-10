# Compatibility and validation — v0.18.2 Alpha

## Tested environment

Borderlands 4 Steam, Windows x64; native module `BL4RemovalTrace-abi12.dll`, original-pool API 2. Requires a separately installed Borderlands 4 Python SDK. Validation used the locally installed SDK; alternate SDK versions are not qualified.

Tested game executable SHA256:

```text
ba75f7c2874b16efb5536a5c0cc28918a03efd3e55d790d2e4db57de0c3a353a
```

PE timestamp: 4086165580; image size: 652288000 bytes. Startup checks PE layout and selected function fingerprints. It does not hash the entire executable at runtime. Patches can require a mod update.

## Evidence for this release

- 26 local runtime regression suites pass, including native gateways, FIFO category isolation, lifetime arguments, world reset, startup/shutdown and localization. The 10 localization tests cover auto Korean/English fallback, manual selection, saved-value migration/preservation, complete menu descriptions and deferred menu refresh without gameplay callbacks.
- 2026-11-10, v0.18.1: world change cleared 371 bullet, 571 blood and 254 blast entries to zero; the new world populated independently. All 5,515 reconstructable FIFO replacements matched the oldest item in their category.
- 2026-11-10 10:59–11:06 KST, v0.18.2: the tester deliberately selected limits of 1,571 / 2,009 / 2,009, not the new defaults. Final counts matched those limits. All 4,865 reconstructable post-cap replacements matched FIFO. All 12,233 recorded selections returned objects; the one missing selection record had a successful return in the independent trace. Overlap checks passed 9,914 times, with no recorded rejection.
- Durations were zero (unlimited). The 12 final sampled components were visible/not hidden with no timed fade; this is component state, not proof of every rendered mark.
- The latest diagnostics dropped 1 pool-selection, 15 shot-path and 2 general native records. FIFO analysis resets history at a sequence gap. Retention callback delivery had no overflow or failed delivery; this is separate from optional diagnostic loss.
- The 51 earlier attached requests without pool acquisition are consistent with game target validation: 3 null targets and 48 primitive meshes inferred to reject decals. Their call sequences had no gaps. No global receives-decals override was added.
- Earlier v0.14.3 gameplay confirmed automatic start and menu-exit cleanup with process exit code 0. This is historical evidence, not a claim that the current DLL is byte-identical to that version.

## Remaining coverage and limits

Finite decal durations and competition from unmanaged requests in the same pool passed local tests but need broader in-game coverage. No full long-session, high-count frame-time, multiplayer or every-enemy/area qualification is claimed. English/Korean localization has local SDK-adapter coverage; all menu layouts were not visually rechecked in this release pass.

Supported decal materials are explicitly allowlisted (103). Damage areas, puddles, warning markers and unknown materials are left to the game. Niagara renderer decals and general dust, ash, ice and particle residue are not generally retained. World teardown and forced destruction remain allowed. No remnants are saved across sessions.

More or larger visible marks can cost memory and rendering time. The default combined decal cap of 704 is not a measured performance guarantee. Detailed diagnostic capture adds work and large logs; leave it off during normal play. Public packages omit developer source, captures and personal settings. Updating requires a new game process.
