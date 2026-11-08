# Combat Remnants 0.14.4 installation and usage

## Install or update

1. Install the [Borderlands 4 Python SDK](https://bl-sdk.github.io/oak2-mod-db/) for Windows x64. Check [compatibility](COMPATIBILITY.md).
2. Exit the game. Updating the native DLL requires a new game process.
3. Download **CombatRemnants-0.14.4.zip** from the [release](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/releases/tag/v0.14.4), not the Source code archives.
4. Back up the old `sdk_mods/bl4_persistent_effects` folder outside `sdk_mods`, then replace it. Move any legacy separate `bl4_persistence_probe` folder outside too. Preserve `sdk_mods/settings/bl4_persistent_effects.json`. Undeploy mod-manager-owned files through that manager first.
5. Copy the ZIP's `bl4_persistent_effects` folder into the game's `sdk_mods` folder.

```text
Borderlands 4/sdk_mods/bl4_persistent_effects/__init__.py
Borderlands 4/sdk_mods/bl4_persistent_effects/_native/BL4RemovalTrace-abi11.dll
```

6. Enable **BL4 Persistent Combat Effects (Experimental)** in the SDK menu. Retention starts automatically when the player is ready.

Top-level documents are not installed into the game. This guide covers manual installation; Vortex deployment has not been separately qualified.

## Options

- Maximum retained corpses: default 50, range 0–500. Each corpse and its linked parts form one group. The oldest group is released when the cap is exceeded.
- Boss retention (`보스 시체 유지`): on by default. Turning it off excludes verified Boss. rank tags and linked parts before elemental policy.
- Elemental death (`원소 사망 처리`): keep indefinitely (`안 없어지게`), dissolve slowly (`천천히 사라지게`, default), or game default (`게임 기본 동작`).
- Elemental dissolve duration: default 30 seconds, range 1–600; applies to slow dissolve mode.

Saved settings take precedence. Ordinary deaths and linked parts remain under count retention. The cap does not spawn bodies. Already-dead NPCs and existing parts are not collected retroactively. World teardown, forced destruction and out-of-world cleanup remain available. Battlefield state is not saved across sessions.

## Optional commands

```text
bl4_corpses_status
bl4_corpses_off
bl4_corpses_on --max-corpses 100
```

No on command is required for automatic use. `off` stops retention and releases groups; `on` starts again after pending release completes. Disabling the mod also disables automatic start. You do not need off before game exit.

A zero cap releases groups; use off to stop control and recording. The old `--max-limbs` and `--multiplier` arguments are ignored. `bl4_effects_on` is an alias.

## Reporting a problem

Include your game build, options, enemy/death type, visible result and session logs in [Issues](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/issues).

```text
Borderlands 4/sdk_mods/bl4_persistent_effects/reports/
```

Startup: `startup-*.jsonl`. Exit: `retention-*.native.shutdown.jsonl` and `*.native.shutdown.native.log`. Object events: `retention-*.native.jsonl`. Review local paths before posting publicly. A code-fingerprint mismatch means this package does not support the installed build; report it instead of bypassing the check.
