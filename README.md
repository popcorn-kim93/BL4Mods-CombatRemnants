# Combat Remnants — Borderlands 4

**The fight ends. The traces remain.**  
**전투가 끝나도, 흔적은 남는다.**

Combat Remnants is a Borderlands 4 mod about preserving the aftermath of combat. Its first public alpha keeps eligible enemy corpses and their associated severed parts together, with a configurable corpse limit instead of normal timed cleanup.

**Current release: v0.11.0 — Alpha**

[Download v0.11.0](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/releases/tag/v0.11.0) · [Installation & usage](INSTALL.md) · [한국어 설치·사용 안내](INSTALL.ko.md) · [Changelog](CHANGELOG.md)

Download **`CombatRemnants-0.11.0.zip`** from the release assets. GitHub's automatically generated **Source code** archives contain this documentation, not the installable mod.

## What this alpha does

- Treats one corpse and its verified owner-linked severed parts as one group.
- Protects eligible groups from the supported timed cleanup, dissolve and body-hiding paths while retention is active.
- Releases the oldest corpse group when the configured corpse limit is exceeded. Parts follow their source corpse; there is no separate limb count setting.
- Leaves world teardown, forced destruction and out-of-world cleanup available to the game.
- Offers explicit start, status and stop commands. There is no automatic timed stop.

The count is a **retention ceiling**, not a target number of spawned bodies. Unassociated parts retain their normal game behavior. Map changes, reloads and exiting the game do not preserve a saved battlefield.

## Quick start

Install the [Borderlands 4 Python SDK](https://bl-sdk.github.io/oak2-mod-db/) and follow the [installation guide](INSTALL.md). Enable **BL4 Persistent Combat Effects (Experimental)** in the SDK mod menu; this is the existing in-game name of Combat Remnants in v0.11.0.

Load a character into the world, then run this **before combat**:

```text
bl4_corpses_on --max-corpses 50
```

Check status or stop:

```text
bl4_corpses_status
bl4_corpses_off
```

Stopping releases retained bodies to the game's cleanup and removes their linked parts. Enabling the menu entry alone does not start retention. See the installation guide for changing the count during play and troubleshooting.

## Current scope and direction

| Category | v0.11.0 |
| --- | --- |
| Eligible enemy corpses | Supported by the current retention policy |
| Severed parts with a verified protected NPC owner | Kept with that corpse group |
| Blood, bullet and blast decals | Planned; not implemented |
| Explosion fragments, ash, dust, ice and elemental particle residue | Planned; not implemented |

The broader goal is a battlefield that retains visible evidence of the fight. Each additional category needs its own lifetime, ownership and performance investigation.

## Alpha qualification

The current package was tested on a Windows x64 Steam build. Native protection checks the executable layout and selected code fingerprints before starting. Other builds, multiplayer and long sessions have not been qualified. See [COMPATIBILITY.md](COMPATIBILITY.md) for the tested build and limits.

In the latest short in-game test, a limit of five left the latest five tracked corpses and eight linked parts at stop. The tester reported that bodies and parts generally remained together on screen. This supports the group policy; it does not establish long-idle persistence, all enemy types or performance at a 500-corpse limit.

## Downloads and source management

This public repository hosts documentation and release metadata. Installable packages are published under [Releases](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/releases). Development source is maintained separately in Perforce. The package contains the Python modules needed at runtime, the native library and its required third-party notices; it does not include the C++ development project, research captures or game assets.

For bug reports, use [Issues](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/issues) and include the command, game build, enemy/death type, visible result and relevant session reports. See [INSTALL.md](INSTALL.md#reporting-a-problem).

[Third-party notices](THIRD_PARTY_NOTICES.md)
