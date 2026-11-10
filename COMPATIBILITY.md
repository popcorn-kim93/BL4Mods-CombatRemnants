# Compatibility and validation — v0.18.3 Alpha

## Tested environment

Borderlands 4 Steam, Windows x64; native module `BL4RemovalTrace-abi12.dll`, original-pool API 2. Requires a separately installed Borderlands 4 Python SDK. Validation used the locally installed SDK; alternate SDK versions are not qualified.

Tested game executable SHA256:

```text
ba75f7c2874b16efb5536a5c0cc28918a03efd3e55d790d2e4db57de0c3a353a
```

PE timestamp: 4086165580; image size: 652288000 bytes. Startup checks PE layout and selected function fingerprints. It does not hash the entire executable at runtime. Patches can require a mod update.

## Startup and upgrades

Fresh installations with no settings file enable automatically. Existing saved disabled choices are respected. The mod also starts when enabled after entering the world, without requiring a console command. The native DLL is unchanged from 0.18.2.

## Remaining coverage and limits

Finite decal durations, competition from unmanaged effects, long sessions, multiplayer and all enemy/area combinations have not been comprehensively tested. More or larger visible marks can increase resource use.

Supported decal materials are explicitly allowlisted (103). Damage areas, puddles, warning markers and unknown materials are left to the game. Niagara renderer decals and general dust, ash, ice and particle residue are not generally retained. World teardown and forced destruction remain allowed. No remnants are saved across sessions.

More or larger visible marks can cost memory and rendering time. The default combined decal cap of 704 is not a measured performance guarantee. Detailed diagnostic capture adds work and large logs; leave it off during normal play. Public packages omit developer source, captures and personal settings. Updating requires a new game process.
