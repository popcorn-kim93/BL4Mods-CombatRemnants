# Compatibility and validation — v0.14.4 Alpha

## Tested environment

Borderlands 4 Steam, Windows x64. Latest menu-exit test: 2026-11-09 (Korea Standard Time). Native module: `BL4RemovalTrace-abi11.dll`; shutdown API 2.

Tested executable SHA256:

```text
ba75f7c2874b16efb5536a5c0cc28918a03efd3e55d790d2e4db57de0c3a353a
```

PE timestamp: `4086165580`; image size: `652288000` bytes. Native protection validates PE layout and selected function fingerprints before starting, including the two exit routes. It does not compute a whole-file hash at runtime. Game patches may require an updated mod.

## Evidence for this release

- 25 local checks passed, covering retention, boss/elemental policies, bounded queues, startup, shutdown and native detours.
- The Release build native DLL matches the game-tested v0.14.3 DLL byte for byte. v0.14.4 changes the version and default elemental option; its 29 runtime files passed local and package checks.
- Automatic start, timer dispatch and exit cleanup ran on the same game thread.
- Menu exit entered `gbx_delayed_game_exit`; protection stopped, the Windows timer was removed, and the three SDK callback groups had zero remaining hooks with no detach errors.
- Both recording workers finished. Mod cleanup took about 4.33ms. The original exit state machine advanced through 0, 2, 3 and 4. Steam recorded exit code 0 about nine seconds later.
- The final summary had 42 tracked corpses and 382 tracked parts. These are bookkeeping counts, not proof that every object was visible.

This confirms one automatic-start/combat/menu-exit session. It does not verify every exit route, save-file integrity, long sessions, every enemy/elemental combination or multiplayer. Earlier gameplay observations supported corpse and linked-part retention; coverage remains experimental.

## Limits

- Only eligible NPC corpses and verified owner-linked severed parts are supported. Decals and general particle residue are not implemented.
- World teardown, forced destruction, out-of-world cleanup and unassociated parts retain game behavior.
- Large corpse limits can increase resource use; no frame-rate guarantee is made.
- Native hooks remain in pass-through state during game exit to avoid code patching during teardown. DLL and callback memory remain until the process ends. Manual off restores hooks and performs normal group cleanup.
- Periodic full reports and periodic state diagnostics are opt-in; event capture still writes session evidence.
- Other storefront builds and game updates are not qualified. Updating the mod requires a game restart.
