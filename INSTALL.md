# Combat Remnants 0.18.2 installation and usage

## Install or update

1. Install the [Borderlands 4 Python SDK](https://bl-sdk.github.io/oak2-mod-db/) for Windows x64. Check [compatibility](COMPATIBILITY.md).
2. Close the game completely. The native DLL and loaded Python code require a new game process for updates.
3. Use **CombatRemnants-0.18.2.zip** from [Releases](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/releases) when published, not a Source code archive.
4. Back up the old `sdk_mods/bl4_persistent_effects` folder outside `sdk_mods`, then replace it. Move any old separate `bl4_persistence_probe` folder outside too. Preserve `sdk_mods/settings/bl4_persistent_effects.json`. If a mod manager owns these files, undeploy through that manager before manual replacement.
5. Copy the ZIP's `bl4_persistent_effects` folder directly into the game's `sdk_mods` folder.

```text
Borderlands 4/sdk_mods/bl4_persistent_effects/__init__.py
Borderlands 4/sdk_mods/bl4_persistent_effects/_native/BL4RemovalTrace-abi12.dll
```

6. Enable **BL4 Persistent Combat Effects (Experimental)** in the SDK menu. Retention starts automatically when the player is ready.

Top-level documents do not need installation. Manual installation is the qualified method; Vortex deployment has not been separately qualified.

## Language and options

Language defaults to **Auto / 자동**: Korean for Korean game language, English otherwise. Choose **English** or **한국어** to override it, then reopen mod settings. This changes the mod menu only. Console command identifiers and diagnostic JSON fields remain stable and are not translated.

| Option | Default / behavior |
| --- | --- |
| Maximum retained corpses | 50; range 0–500. One corpse and its linked parts form one group. |
| Keep boss corpses | On. Boss and Boss.* rank tags are evaluated before elemental policy. |
| Elemental death behavior | Fade slowly; alternatives are Keep indefinitely and Game default. |
| Elemental corpse fade time | 30 seconds; range 1–600, used by Fade slowly. |
| Retain combat decals | On. Only confirmed bullet, blood and blast materials. |
| Bullet / blood / blast maximum | 512 / 128 / 64; independent limits, range 0–4096 each. |
| Bullet / blood / blast lifetime | 0 / 0 / 0 seconds: unlimited; range 0–3600 each. |

Saved settings take precedence. At a decal cap, the oldest mark of that same category is reused for the new mark. A decal maximum of 0 clears that category's retained originals and leaves new marks to the game. A lifetime of 0 disables timed removal, not count limits. Finite lifetimes fade during the final second and apply to newly created marks. Decreasing a cap releases excess older entries.

Already-dead NPCs and existing parts are not collected retroactively. Game teardown and forced destruction remain possible. Decals clear on world changes; same-world travel may preserve the same world. There is no battlefield save across game sessions.

## Optional commands

```text
bl4_corpses_status
bl4_decals_status
bl4_corpses_off
bl4_corpses_on --max-corpses 100
bl4_decals_off
bl4_decals_on
```

The corpse off command stops the shared retention session, including decal retention. Decal off stops only decals. Turning the mod off disables its retention and automatic start. No off command is required before game exit. Use the menu for persistent configuration; old `--max-limbs` and `--multiplier` arguments are compatibility-only.

## Reporting a problem

For a short diagnostic recording, run `bl4_decals_start`, reproduce the issue, then `bl4_decals_stop`. **These commands start/stop collection, not decal retention.** Detailed traces can be large and add overhead; they are unnecessary for normal play.

Include the game build, actual option values, visible result and matching `decal-events-*.summary.json` from `sdk_mods/bl4_persistent_effects/reports` in [Issues](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/issues). Keep the matching JSONL if deeper analysis is needed; review local paths before sharing. A native fingerprint mismatch needs a compatible mod update, not a bypass.
