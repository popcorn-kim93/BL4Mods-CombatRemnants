# Combat Remnants — Borderlands 4

**The fight ends. The traces remain. / 전투가 끝나도, 흔적은 남는다.**

Combat Remnants preserves eligible enemy corpses and their linked severed parts as one group, with a configurable corpse limit.

**Current release: v0.14.4 — Alpha**

[Download v0.14.4](https://github.com/popcorn-kim93/BL4Mods-CombatRemnants/releases/tag/v0.14.4) · [Installation & usage](INSTALL.md) · [한국어 설치·사용 안내](INSTALL.ko.md) · [Changelog](CHANGELOG.md)

Download **CombatRemnants-0.14.4.zip** from Releases. GitHub's automatic Source code archives contain documentation, not the installable mod.

## Features

- Starts automatically when enabled and a player is ready.
- Keeps eligible corpses and owner-linked parts together; releases the oldest group when the corpse limit is exceeded.
- Allows boss retention to be turned on or off, before evaluating elemental policy.
- Offers keep indefinitely, dissolve slowly, or game-default elemental-death modes. Slow dissolve duration is configurable from 1 to 600 seconds.
- Preserves normal body hiding when a body is replaced by Gib fragments.
- Uses event-driven NPC/death/part discovery, with one initial live-NPC query per map. Periodic state diagnostics and full reports are opt-in.
- Releases protection, timers and SDK callbacks on menu exit while preserving the original exit state machine.

The count is a retention ceiling, not a target spawn count. Parts have no separate limit. World teardown, forced destruction, out-of-world cleanup and unassociated parts retain game behavior. Remnants are not saved across sessions.

## Quick start

Install the [Borderlands 4 Python SDK](https://bl-sdk.github.io/oak2-mod-db/), put the package's `bl4_persistent_effects` folder inside `sdk_mods`, and enable **BL4 Persistent Combat Effects (Experimental)** in the SDK menu. This is Combat Remnants' current in-game name.

Retention starts automatically. Options: corpse limit (default 50), boss retention (default on), elemental behavior (default slow dissolve), and slow dissolve duration (default 30 seconds). Existing saved settings take precedence.

Optional commands:

```text
bl4_corpses_status
bl4_corpses_off
bl4_corpses_on --max-corpses 100
```

`off` stops the current session and returns groups to cleanup. `on` starts it again. You do not need to run off before exiting.

## Scope and validation

Supported: corpses and verified owner-linked severed parts. **Blood/bullet/blast decals and general particles such as dust, ash and ice residue are not implemented.**

25 local checks passed. A v0.14.3 game session with the same native DLL confirmed automatic start and menu-exit cleanup of protection, timers, SDK callbacks and recording workers; the game exited with code 0. This does not qualify all enemies, long sessions, multiplayer or performance at large limits. See [validation](COMPATIBILITY.md).

## Downloads and source management

This public repository contains documentation and release metadata. Development source is maintained in Perforce. Release packages contain runtime Python modules, the native DLL and third-party notices, without the C++ development project, research captures or game assets.

See [reporting a problem](INSTALL.md#reporting-a-problem) and [third-party notices](THIRD_PARTY_NOTICES.md).
