# Changelog

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
