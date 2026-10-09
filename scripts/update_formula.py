#!/usr/bin/env python3
"""Update only release coordinates in the maintained binary formulae."""
import argparse
import json
import os
from pathlib import Path
import re
import urllib.request

OWNER = "zaubermaerchen"
TOOLS = {"khsier": "_", "pipewisp": "_", "dam": "_", "outage": "-", "sluice": "-", "trysudo": "-"}
PLATFORMS = (("darwin", "arm64"), ("darwin", "amd64"), ("linux", "arm64"), ("linux", "amd64"))


def asset_names(tool, tag):
    if tool not in TOOLS or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
        raise ValueError("unsupported formula or stable release tag")
    separator = TOOLS[tool]
    return [separator.join((tool, tag, system, arch)) + ".tar.gz" for system, arch in PLATFORMS]


def validate_release(tool, tag, release):
    expected = asset_names(tool, tag) + ["SHA256SUMS"]
    if release.get("tag_name") != tag or release.get("draft") is not False or release.get("prerelease") is not False:
        raise ValueError("release must be published and stable with the requested tag")
    assets = {}
    for asset in release.get("assets", []):
        name = asset.get("name")
        if name in expected:
            url = f"https://github.com/{OWNER}/{tool}/releases/download/{tag}/{name}"
            if name in assets or asset.get("browser_download_url") != url:
                raise ValueError("duplicate asset or unexpected asset URL")
            assets[name] = url
    if set(assets) != set(expected):
        raise ValueError("release is missing required assets")
    return assets


def parse_checksums(manifest, names):
    checksums = {}
    for line in manifest.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-fA-F]{64}) [ *]([A-Za-z0-9_.-]+)", line)
        if not match or match[2] in checksums:
            raise ValueError("invalid or duplicate checksum entry")
        checksums[match[2]] = match[1].lower()
    if not set(names).issubset(checksums):
        raise ValueError("required checksum is missing")
    return checksums


def update_formula(original, tool, tag, release, manifest):
    assets = validate_release(tool, tag, release)
    names = asset_names(tool, tag)
    checksums = parse_checksums(manifest, names)
    version_pattern = r'(?m)^  version "[0-9]+\.[0-9]+\.[0-9]+"$'
    if len(re.findall(version_pattern, original)) != 1:
        raise ValueError("unexpected formula version shape")
    current = re.search(r'(?m)^  version "([0-9]+\.[0-9]+\.[0-9]+)"$', original)[1]
    if tuple(map(int, tag[1:].split("."))) < tuple(map(int, current.split("."))):
        raise ValueError("release is older than the current formula")
    pattern = r'(?m)^(      url ")([^"\n]+)("\n      sha256 ")([0-9a-f]{64})(")$'
    matches = list(re.finditer(pattern, original))
    if len(matches) != 4:
        raise ValueError("expected exactly four formula release entries")
    for match, (system, arch) in zip(matches, PLATFORMS):
        sep = re.escape(TOOLS[tool])
        old_url = (rf"https://github\.com/{OWNER}/{tool}/releases/download/v[0-9]+\.[0-9]+\.[0-9]+/"
                   rf"{tool}{sep}v[0-9]+\.[0-9]+\.[0-9]+{sep}{system}{sep}{arch}\.tar\.gz")
        if not re.fullmatch(old_url, match[2]):
            raise ValueError("unexpected formula platform or release URL")
    index = iter(names)
    def replace(match):
        name = next(index)
        return match[1] + assets[name] + match[3] + checksums[name] + match[5]
    updated = re.sub(pattern, replace, original)
    return re.sub(version_pattern, f'  version "{tag[1:]}"', updated)


def fetch(url, token=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "homebrew-tap-updater"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formula", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--source-repository", required=True)
    args = parser.parse_args()
    asset_names(args.formula, args.tag)
    if args.source_repository != f"{OWNER}/{args.formula}":
        parser.error("caller must be the formula's source repository")
    release = json.loads(fetch(f"https://api.github.com/repos/{args.source_repository}/releases/tags/{args.tag}", os.getenv("GH_TOKEN")))
    assets = validate_release(args.formula, args.tag, release)
    manifest = fetch(assets["SHA256SUMS"]).decode("utf-8")
    path = Path("Formula") / f"{args.formula}.rb"
    updated = update_formula(path.read_text(), args.formula, args.tag, release, manifest)
    path.write_text(updated)


if __name__ == "__main__":
    main()
