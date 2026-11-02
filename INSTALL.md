# Install and use Combat Remnants v0.11.0

## Requirements

- Borderlands 4 on Windows x64; see [tested build and compatibility](COMPATIBILITY.md).
- A working [Borderlands 4 Python SDK installation](https://bl-sdk.github.io/oak2-mod-db/), including its standard mod menu and `mods_base` support.

The SDK is a separate prerequisite and is not bundled. This alpha is distributed for manual installation; a Vortex installer has not been qualified.

## Install

1. Close Borderlands 4. The native library remains loaded until the game exits, so replacing files requires a restart.
2. Download **CombatRemnants-0.11.0.zip** from the [v0.11.0 release](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/releases/tag/v0.11.0). Do not use GitHub's **Source code** archives.
3. If upgrading a development build, move the old `sdk_mods/bl4_persistent_effects` folder to a backup outside `sdk_mods`, preserving its reports. If the older separate `bl4_persistence_probe` exists, move it outside `sdk_mods` as well; diagnostics are now integrated. If a mod manager owns those files, undeploy that copy through the manager first.
4. Extract the ZIP and copy its **bl4_persistent_effects** folder into the game's **sdk_mods** folder. The final path must be:

   ```text
   Borderlands 4/sdk_mods/bl4_persistent_effects/__init__.py
   Borderlands 4/sdk_mods/bl4_persistent_effects/_native/BL4RemovalTrace-abi9.dll
   ```

   Do not add an extra `CombatRemnants-0.11.0` folder between `sdk_mods` and `bl4_persistent_effects`. The root Markdown documents and manifest are for reference; they need not be copied into the game.
5. Launch the game, open the SDK mod menu and enable **BL4 Persistent Combat Effects (Experimental)**. This legacy menu label and internal folder name are retained in this release. They refer to Combat Remnants, not an additional mod.

## Start before combat

Load a character into the world. Open the SDK console using the key configured by the SDK (normally `~`; pressing it twice expands the console), then enter:

```text
bl4_corpses_on --max-corpses 50
```

One corpse and its linked severed parts form one group. Fifty is the default setting, not a measured performance guarantee. The mod protects newly observed eligible enemies; it cannot recover bodies that disappeared before it started.

The count is a maximum, not a spawn amount. You must kill enough eligible enemies to approach it, and world cleanup exceptions can still remove objects.

To change the active limit, run the command again with the desired count, for example:

```text
bl4_corpses_on --max-corpses 100
```

The menu's **Maximum retained corpses** option also changes the active limit. Starting without `--max-corpses` uses that menu setting. The menu provides 0–500; 0 releases all groups. Use `bl4_corpses_off` to stop the controller and reporting completely.

`--max-limbs` and `--multiplier` are retired and ignored. Separate `bl4_effects_on` activation is unnecessary; it aliases the same controller. Read-only diagnostic capture commands are not required for normal use.

## Check and stop

```text
bl4_corpses_status
bl4_corpses_off
```

`status` prints and saves the current state. `off` removes retained linked parts, returns corpses to normal game cleanup and finishes the session report. Let cleanup complete before starting another session. If `release_pending` is true, leave the game running briefly and check status again.

There is no automatic timed stop. Start retention again when needed in a new game session. To uninstall, close the game and move `bl4_persistent_effects` out of `sdk_mods`; leave other SDK files and mods in place.

## Reporting a problem

The mod writes session files automatically under:

```text
Borderlands 4/sdk_mods/bl4_persistent_effects/reports/
```

After reproducing the issue, note what was visible **before** running `bl4_corpses_off`, then stop. Include the matching `retention-*.json` and `retention-*.native.jsonl`, the start command, game build, enemy/death type and visible result in a [GitHub issue](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/issues). Review reports before sharing: runtime diagnostics may include local module paths. Detailed material tracing is off by default and is not needed for ordinary play.

If the command is unknown, check that the SDK loaded the mod and the menu entry is enabled. If it says to enter the game, load a character first. If native build validation fails, that game build is unsupported by this package; attach the error message instead of bypassing its checks.
