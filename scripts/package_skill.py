"""package_skill.py - validate the repo's manifests and build the upload zip.

Claude.ai, ChatGPT and other hosts that accept a *skill upload* expect a zip
whose ROOT contains SKILL.md. GitHub's "Code -> Download ZIP" produces a zip
with everything nested under `<repo>-<branch>/`, which those uploaders reject.
This script builds the correct shape and checks that every manifest agrees
before it does.

    python scripts/package_skill.py                # validate, then write dist/
    python scripts/package_skill.py --validate-only
    python scripts/package_skill.py --version 1.1.0   # bump every manifest first

Exits 1 if validation fails, so CI can gate a release on it.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
DIST = ROOT / "dist"

# Every file that carries a version, and the JSON path to it.
MANIFESTS = {
    ".claude-plugin/plugin.json": ("version",),
    ".claude-plugin/marketplace.json": ("plugins", 0, "version"),
    ".cursor-plugin/plugin.json": ("version",),
    ".cursor-plugin/marketplace.json": ("plugins", 0, "version"),
}

EXCLUDE_DIRS = {"__pycache__", ".git", ".pytest_cache", ".ipynb_checkpoints"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db"}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def dig(obj, path):
    """Walk a JSON structure by a tuple of keys/indices. Returns None if absent."""
    for step in path:
        try:
            obj = obj[step]
        except (KeyError, IndexError, TypeError):
            return None
    return obj


def assign(obj, path, value):
    for step in path[:-1]:
        obj = obj[step]
    obj[path[-1]] = value


def load_json(rel: str):
    p = ROOT / rel
    if not p.exists():
        return None, f"missing manifest: {rel}"
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"{rel} is not valid JSON: {e}"


def parse_frontmatter(text: str):
    """Return (dict, error). Only the flat top-level keys we care about."""
    if not text.startswith("---"):
        return None, "SKILL.md does not start with YAML frontmatter"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "SKILL.md frontmatter is not closed with ---"
    fm, out, key = text[3:end], {}, None
    for line in fm.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^\s", line) and key:            # continuation line
            out[key] += " " + line.strip()
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, out[key.strip()] = key.strip(), val.strip().strip("'\"")
    return out, None


def iter_files(base: Path):
    for p in sorted(base.rglob("*")):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.suffix in EXCLUDE_SUFFIXES or p.name in EXCLUDE_NAMES:
            continue
        yield p


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------

def find_skills():
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(d for d in SKILLS_DIR.iterdir()
                  if d.is_dir() and (d / "SKILL.md").exists())


def validate():
    """Returns (errors, info). Checks manifests, versions and every SKILL.md."""
    errors, info = [], {}

    skills = find_skills()
    if not skills:
        errors.append(f"no skills found: expected {SKILLS_DIR.name}/<name>/SKILL.md")
        return errors, info
    info["skills"] = [s.name for s in skills]

    # --- manifests parse, and all versions agree -------------------------
    versions, names = {}, {}
    for rel, vpath in MANIFESTS.items():
        data, err = load_json(rel)
        if err:
            errors.append(err)
            continue
        v = dig(data, vpath)
        if v is None:
            errors.append(f"{rel}: no version at {'.'.join(map(str, vpath))}")
        else:
            versions[rel] = v
        if rel.endswith("plugin.json"):
            names[rel] = data.get("name")
        else:
            names[rel] = dig(data, ("plugins", 0, "name"))

    if len(set(versions.values())) > 1:
        errors.append("manifest versions disagree: " +
                      ", ".join(f"{k}={v}" for k, v in versions.items()))
    elif versions:
        info["version"] = next(iter(versions.values()))

    declared = set(n for n in names.values() if n)
    if len(declared) > 1:
        errors.append("manifest plugin names disagree: " +
                      ", ".join(f"{k}={v}" for k, v in names.items()))
    elif declared:
        info["plugin_name"] = next(iter(declared))
        for s in skills:
            if s.name == info["plugin_name"]:
                break
        else:
            errors.append(
                f"plugin name {info['plugin_name']!r} matches no skill directory "
                f"({', '.join(s.name for s in skills)}). Not fatal for hosts, but "
                f"the repo reads as inconsistent.")

    # --- cursor marketplace source must be relative ----------------------
    cur, _ = load_json(".cursor-plugin/marketplace.json")
    src = dig(cur, ("plugins", 0, "source")) if cur else None
    if isinstance(src, str) and (src.startswith("/") or ".." in src):
        errors.append(f".cursor-plugin/marketplace.json: source {src!r} must be "
                      f"relative with no parent traversal")

    # --- every SKILL.md ---------------------------------------------------
    for s in skills:
        fm, err = parse_frontmatter((s / "SKILL.md").read_text(encoding="utf-8"))
        label = f"{s.name}/SKILL.md"
        if err:
            errors.append(f"{label}: {err}")
            continue
        name, desc = fm.get("name"), fm.get("description")
        if not name:
            errors.append(f"{label}: frontmatter has no name")
        else:
            if name != s.name:
                errors.append(f"{label}: name {name!r} does not match its "
                              f"directory {s.name!r}")
            if len(name) > 64 or not NAME_RE.match(name):
                errors.append(f"{label}: name must be <=64 chars of lowercase "
                              f"letters, numbers and hyphens")
            if any(w in name for w in ("anthropic", "claude")):
                errors.append(f"{label}: name may not contain reserved words")
        if not desc:
            errors.append(f"{label}: frontmatter has no description")
        elif len(desc) > 1024:
            errors.append(f"{label}: description is {len(desc)} chars, max 1024")
        if "<" in (desc or "") and ">" in (desc or ""):
            errors.append(f"{label}: description may not contain XML tags")

        body = (s / "SKILL.md").read_text(encoding="utf-8").splitlines()
        info.setdefault("body_lines", {})[s.name] = len(body)
        if len(body) > 500:
            errors.append(f"{label}: body is {len(body)} lines, over the "
                          f"recommended 500 - split into reference files")

        # linked reference files must exist
        for target in re.findall(r"\]\((?!https?://)([^)#]+)\)",
                                 (s / "SKILL.md").read_text(encoding="utf-8")):
            if not (s / target).exists():
                errors.append(f"{label}: links to missing file {target}")

    return errors, info


# --------------------------------------------------------------------------
# packaging
# --------------------------------------------------------------------------

def set_version(new: str):
    """Write `new` into every manifest so they cannot drift."""
    if not re.match(r"^\d+\.\d+\.\d+$", new):
        raise SystemExit(f"version must be semver like 1.0.0, got {new!r}")
    for rel, vpath in MANIFESTS.items():
        p = ROOT / rel
        data = json.loads(p.read_text(encoding="utf-8"))
        assign(data, vpath, new)
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                     encoding="utf-8")
        print(f"  set {rel} -> {new}")


def build_zip(skill_dir: Path, version: str) -> Path:
    """Zip with SKILL.md at the ROOT, which is what skill uploaders require."""
    DIST.mkdir(exist_ok=True)
    out = DIST / f"{skill_dir.name}.zip"
    if out.exists():
        out.unlink()
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in iter_files(skill_dir):
            z.write(f, f.relative_to(skill_dir).as_posix())
            n += 1
    print(f"  {out.relative_to(ROOT).as_posix()}  ({n} files, "
          f"{out.stat().st_size / 1024:.0f} KB)")
    return out


def verify_zip(path: Path):
    """A zip that fails this is the exact failure mode uploaders reject."""
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        bad = z.testzip()
    if bad:
        raise SystemExit(f"corrupt entry in {path.name}: {bad}")
    if "SKILL.md" not in names:
        raise SystemExit(f"{path.name} has no SKILL.md at its root - uploaders "
                         f"will reject it. Root entries: {sorted(names)[:5]}")
    nested = [n for n in names if n.count("/") and n.split("/")[0] == path.stem]
    if nested:
        raise SystemExit(f"{path.name} nests everything under {path.stem}/ - "
                         f"the skill files must sit at the zip root")
    print(f"  verified: SKILL.md at zip root, {len(names)} entries")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--validate-only", action="store_true")
    ap.add_argument("--version", help="set this version in every manifest first")
    ap.add_argument("--clean", action="store_true", help="remove dist/ first")
    a = ap.parse_args(argv)

    if a.version:
        print("bumping manifests")
        set_version(a.version)

    print("validating")
    errors, info = validate()
    for k in ("skills", "plugin_name", "version"):
        if k in info:
            print(f"  {k}: {info[k]}")
    for name, n in info.get("body_lines", {}).items():
        print(f"  {name}/SKILL.md: {n} lines")
    if errors:
        for e in errors:
            print(f"  FAIL  {e}")
        print(f"{len(errors)} problem(s) found")
        return 1
    print("  all manifests agree")

    if a.validate_only:
        return 0

    if a.clean and DIST.exists():
        shutil.rmtree(DIST)
    print("packaging")
    for s in find_skills():
        verify_zip(build_zip(s, info.get("version", "0.0.0")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
