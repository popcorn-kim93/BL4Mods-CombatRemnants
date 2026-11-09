"""Verify GitHub release assets and check Nexus targets. This script never uploads.

The pinned official Nexus action performs the upload only after both checks pass.
Uses Python's standard library and GitHub CLI; does not build or execute the mod.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile

REPOSITORY = "popcorn-kim93/BL4Mods-CombatRemnants"
ROOT_URL = "https://github.com/" + REPOSITORY
WORK = Path("nexus-release-work")
MAX_PACKAGE = 100 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def version_from_tag(tag):
    require(re.fullmatch(r"v\d+\.\d+\.\d+", tag) is not None,
            "Use an exact vMAJOR.MINOR.PATCH release tag.")
    return tag[1:]


def release_policy(release, tag, allow_prerelease):
    version = version_from_tag(tag)
    require(release.get("tag_name") == tag, "Release tag mismatch.")
    require(release.get("draft") is False and release.get("published_at"),
            "Only published releases may be mirrored; drafts are excluded.")
    require(isinstance(release.get("prerelease"), bool), "Missing prerelease status.")
    if release["prerelease"] and not allow_prerelease:
        return version, False, "Prerelease excluded; set NEXUS_ALLOW_PRERELEASE=true to opt in."
    return version, True, "Release eligible."


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_assets(directory, tag):
    version = version_from_tag(tag)
    package = directory / f"CombatRemnants-{version}.zip"
    manifest_path = directory / "release-manifest.json"
    sums = {}
    for line in (directory / "SHA256SUMS.txt").read_text("utf-8").splitlines():
        match = re.fullmatch(r"([a-f0-9]{64})  ([^/\\]+)", line)
        require(match is not None, "Invalid checksum line.")
        sha, name = match.groups()
        require(name not in sums, "Duplicate checksum entry.")
        sums[name] = sha
    require(set(sums) == {package.name, manifest_path.name}, "Unexpected checksum entries.")
    for file in (package, manifest_path):
        require(file.stat().st_size <= MAX_PACKAGE, "Release asset exceeds size limit.")
        require(digest(file.read_bytes()) == sums[file.name], f"Checksum mismatch: {file.name}")
    manifest = json.loads(manifest_path.read_text("utf-8"))
    require(manifest.get("name") == "Combat Remnants", "Wrong product.")
    require(manifest.get("repository") == ROOT_URL, "Wrong repository.")
    require(manifest.get("tag") == tag and manifest.get("version") == version, "Version mismatch.")
    require(manifest.get("channel") in {"alpha", "beta", "stable"}, "Diagnostic/unknown channel rejected.")
    require(manifest.get("runtime_matches_tested_build") is True, "Unverified runtime package.")
    require(manifest.get("runtime_folder") == "bl4_persistent_effects", "Wrong runtime folder.")
    require(manifest.get("package") == {
        "name": package.name, "bytes": package.stat().st_size, "sha256": sums[package.name]
    }, "Package manifest mismatch.")
    hashes = manifest["sha256"]
    require(isinstance(hashes, dict) and hashes, "Missing content hashes.")
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "Duplicate ZIP members.")
        require(set(names) == set(hashes) | {"CONTENTS.json"}, "Unexpected ZIP members.")
        require(sum(i.file_size for i in archive.infolist()) <= MAX_PACKAGE * 4,
                "Expanded ZIP exceeds size limit.")
        for name in names:
            path = PurePosixPath(name)
            require(not path.is_absolute() and ".." not in path.parts and "\\" not in name
                    and ":" not in name, "Unsafe ZIP member path.")
        for name, sha in hashes.items():
            require(digest(archive.read(name)) == sha, f"Content hash mismatch: {name}")
        contents = json.loads(archive.read("CONTENTS.json"))
        for key in ("name", "version", "channel", "repository", "runtime_folder",
                    "runtime_file_count", "runtime_matches_tested_build", "sha256"):
            require(contents.get(key) == manifest.get(key), f"CONTENTS mismatch: {key}")
        require(sum(n.startswith("bl4_persistent_effects/") for n in hashes)
                == manifest["runtime_file_count"], "Runtime file count mismatch.")
        require("bl4_persistent_effects/__init__.py" in hashes, "Missing runtime module.")
        require(any(n.startswith("bl4_persistent_effects/_native/") and n.endswith(".dll")
                    for n in hashes), "Missing native DLL.")
    return {"version": version, "package": str(package.resolve()), "sha256": sums[package.name],
            "tag": tag, "release_url": ROOT_URL + "/releases/tag/" + tag}


def gh(*args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    require(result.returncode == 0, "GitHub CLI request failed; check repository access and asset availability.")
    return result.stdout


def output(**values):
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as f:
            for key, value in values.items():
                delim = "VALUE_" + uuid.uuid4().hex
                f.write(f"{key}<<{delim}\n{value}\n{delim}\n")


def note(message):
    print(message)
    if path := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(path, "a", encoding="utf-8") as f:
            f.write(message + "\n\n")


def prepare():
    require(os.environ.get("GITHUB_REPOSITORY", REPOSITORY) == REPOSITORY, "Wrong GitHub repository.")
    tag = os.environ["RELEASE_TAG"]
    version_from_tag(tag)  # Validate before constructing any endpoint or argument.
    release = json.loads(gh("api", f"repos/{REPOSITORY}/releases/tags/{tag}"))
    version, eligible, reason = release_policy(release, tag, os.environ.get("ALLOW_PRERELEASE") == "true")
    if not eligible:
        output(upload="false")
        note(reason)
        return
    names = {f"CombatRemnants-{version}.zip", "release-manifest.json", "SHA256SUMS.txt"}
    assets = release.get("assets", [])
    for name in names:
        matches = [a for a in assets if a.get("name") == name]
        require(len(matches) == 1 and matches[0].get("state") == "uploaded",
                f"Missing or incomplete release asset: {name}. Attach all assets before publishing.")
        limit = MAX_PACKAGE if name.endswith(".zip") else 2 * 1024 * 1024
        require(0 < matches[0]["size"] <= limit, f"Invalid asset size: {name}")
    WORK.mkdir(exist_ok=False)
    gh("release", "download", tag, "--repo", REPOSITORY, "--dir", str(WORK),
       *[arg for name in sorted(names) for arg in ("--pattern", name)])
    plan = verify_assets(WORK, tag)
    plan["release_id"] = release["id"]
    # Plain text is valid Nexus description content. Preserve Markdown release notes as text.
    description = f"Combat Remnants {version}\n{plan['release_url']}\n\n{release.get('body') or ''}"
    plan["description"] = description
    (WORK / "plan.json").write_text(json.dumps(plan, indent=2), "utf-8")
    enabled = os.environ.get("SYNC_ENABLED") == "true"
    dry = os.environ.get("DRY_RUN") == "true"
    output(upload=str(enabled and not dry).lower(), package=plan["package"],
           version=version, description=description)
    note(f"Verified {Path(plan['package']).name}\nSHA256: {plan['sha256']}\n"
         f"Upload requested: {enabled and not dry}. No Nexus contact during verification-only runs.")


def api(path):
    key = os.environ.get("NEXUSMODS_API_KEY", "")
    require(bool(key), "Set the NEXUSMODS_API_KEY repository secret.")
    request = urllib.request.Request("https://api.nexusmods.com/v3" + path,
        headers={"apikey": key, "Accept": "application/json", "User-Agent": "CombatRemnants-ReleaseSync"})
    # Never forward a credential through a redirect, or print server bodies/headers.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=45) as response:
            return json.load(response)["data"]
    except urllib.error.HTTPError as error:
        raise ValueError(f"Nexus read request failed (HTTP {error.code}).") from None
    except urllib.error.URLError:
        raise ValueError("Nexus read request failed; check connectivity.") from None


def identifier(name):
    value = os.environ.get(name, "")
    require(bool(re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value)), f"Configure {name} using the Nexus v3 ID.")
    return urllib.parse.quote(value, safe="")


def check_target(mod_files, versions, file_id, version):
    require(any(f.get("id") == file_id for f in mod_files["mod_files"]),
            "Nexus file does not belong to the configured mod.")
    existing = versions["versions"]
    if any(v.get("version", "").removeprefix("v") == version for v in existing):
        return False, "This version already exists on Nexus; not uploaded again. Existing bytes were not compared."
    target = tuple(map(int, version.split(".")))
    for v in existing:
        old = v.get("version", "").removeprefix("v")
        if re.fullmatch(r"\d+\.\d+\.\d+", old):
            require(tuple(map(int, old.split("."))) < target,
                    "A newer version already exists on Nexus; refusing a version rollback.")
    return True, "Nexus target verified; this version is not present."


def preflight():
    plan = json.loads((WORK / "plan.json").read_text("utf-8"))
    verify_assets(WORK, plan["tag"])
    file_id, mod_id = identifier("NEXUS_FILE_ID"), identifier("NEXUS_MOD_ID")
    allowed, reason = check_target(api(f"/mods/{mod_id}/files"),
        api(f"/mod-files/{file_id}/versions"), file_id, plan["version"])
    output(upload=str(allowed).lower())
    note(reason)


def check_connection():
    """Read only: no release download, no upload and no state change."""
    file_id, mod_id = identifier("NEXUS_FILE_ID"), identifier("NEXUS_MOD_ID")
    files = api(f"/mods/{mod_id}/files")["mod_files"]
    require(any(f.get("id") == file_id for f in files),
            "Nexus file does not belong to the configured mod.")
    versions = api(f"/mod-files/{file_id}/versions")["versions"]
    require(isinstance(versions, list), "Unexpected Nexus version list.")
    # Only print release version labels, never response bodies or account/key details.
    labels = [str(v.get("version", ""))[:80] for v in versions]
    note(f"Nexus read connection succeeded. Mod ID: {mod_id}; file ID: {file_id}. "
         f"File membership confirmed; {len(versions)} version(s). "
         f"Version labels: {json.dumps(labels, ensure_ascii=True)}. "
         "No upload or update was requested. Upload permission was not exercised.")


def verify_upload():
    plan = json.loads((WORK / "plan.json").read_text("utf-8"))
    versions = api(f"/mod-files/{identifier('NEXUS_FILE_ID')}/versions")["versions"]
    expected_id = os.environ["NEXUS_VERSION_ID"]
    require(any(v.get("id") == expected_id and v.get("version") == plan["version"] for v in versions),
            "Nexus upload returned an ID but the expected version was not found. Check Nexus before retrying.")
    note(f"Nexus confirmed version {plan['version']}; version ID {expected_id}. "
         "Page publication, full description and independent download hash were not checked or changed.")


if __name__ == "__main__":
    try:
        require(len(sys.argv) == 2, "Usage: nexus_release.py prepare|preflight|verify|connection")
        {"prepare": prepare, "preflight": preflight, "verify": verify_upload,
         "connection": check_connection}[sys.argv[1]]()
    except (ValueError, KeyError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as error:
        print(f"Release sync stopped: {error}", file=sys.stderr)
        sys.exit(1)
