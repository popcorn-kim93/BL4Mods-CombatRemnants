# Changelog

## 0.14.4 — Alpha — 2026-11-09

- Default settings: automatic start, boss retention enabled, elemental deaths dissolve slowly over 30 seconds.
- Existing saved preferences remain intact. The native DLL is identical to game-tested 0.14.3.
- Includes the 0.14.3 changes below; 0.14.3 was kept as a Perforce checkpoint and not published on GitHub.

## 0.14.3 — Alpha — 2026-11-09

Changes since the public 0.11.0 release:

- Preserve normal Gib body hiding while retaining linked fragments; improve supported body and limb dissolve protection.
- Use event-driven enrollment and destruction/unload bookkeeping. Make repeated state diagnostics and periodic full reports optional; process bounded queue batches.
- Add boss retention and evaluate it before elemental death policy.
- Add keep / slow dissolve / game-default elemental modes with configurable 1–600 second slow dissolve duration.
- Start automatically on the game thread when the player is ready.
- Hook the actual delayed menu-exit path, disable protection, stop timers and detach SDK callbacks before allowing the original exit state machine to continue.
- Add startup/exit evidence, fingerprint guards and tests.

25 local checks passed. A fresh in-game test confirmed automatic start and menu-exit cleanup with process exit code 0. See [validation limits](COMPATIBILITY.md).

## 0.11.0 — Alpha — 2026-11-02

First public **Combat Remnants** release.

- Keeps eligible enemy corpses and their associated severed parts as one retention group.
- Uses a configurable corpse limit instead of normal timed cleanup for protected groups.
- Removes linked parts before releasing the oldest corpse when the limit is exceeded.
- Connects severed parts through verified ownership; does not infer ownership from proximity or spawn order.
- Keeps the established native protection for common corpse cleanup, deferred expiry, supported dissolve inputs and Gib body hiding.
- Replaces the independent limb cap with the corpse-group policy. The old `--max-limbs` argument is ignored.
- Includes integrated session reporting and explicit start/status/stop commands.

The public name is Combat Remnants. The tested in-game menu name remains **BL4 Persistent Combat Effects (Experimental)**, and the installation folder remains `bl4_persistent_effects`.

Current support is limited to corpses and linked severed parts. Decals, general particles and other combat residue remain future work. See [compatibility and validation](COMPATIBILITY.md) for the alpha test boundaries.
