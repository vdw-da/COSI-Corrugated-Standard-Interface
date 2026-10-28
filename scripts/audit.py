#!/usr/bin/env python3
"""Repository consistency checks; a clean audit is not release approval.

Runs without private files or Git metadata. Publication checks exclude local working
material and reject internal review identifiers in public files.
"""
from pathlib import Path
import re
import html
import unicodedata
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {"tmp", "node_modules", "__pycache__"}
# Provenance records must be able to quote the identifiers they replaced.
ALLOW = {
    ("ED-", "adr/ADR-000016-schema-corrections-to-documented-intent.md"),
    ("vdw:transparent-data", "adr/ADR-000020-standard-named-cosi.md"),
    ("vdw:transparent-data", "adr/ADR-000016-schema-corrections-to-documented-intent.md"),
    ("VDW Transparent Data", "adr/ADR-000020-standard-named-cosi.md"),
}


def public_path(path):
    return not any((part.startswith(".") and part not in {".github", ".gitignore"})
                   or part in EXCLUDED_DIRS for part in path.parts)


def public_files(root):
    """Use Git's publication inventory, or traverse a standalone source archive.

    Local exclude rules stay local. Tracked files remain audit inputs even if an
    ignore rule would otherwise exclude them. No personal filenames are embedded.
    """
    root = Path(root).resolve()
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        top = None
    if top and Path(top).resolve() == root:
        names = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached", "--others",
             "--exclude-standard", "-z"], capture_output=True, check=True).stdout
        paths = {root / name.decode("utf-8") for name in names.split(b"\0") if name}
        return sorted(path for path in paths if path.is_file()
                      and not any(part.is_symlink() for part in (path, *path.parents)))

    # Archives do not contain Git metadata or local working files.
    result = []
    def visit(directory):
        for path in sorted(directory.iterdir()):
            if not public_path(path.relative_to(root)) or path.is_symlink():
                continue
            if path.is_dir():
                visit(path)
            else:
                result.append(path)
    visit(root)
    return result


def markdown_files(root):
    return [p for p in public_files(root) if p.suffix == ".md"]


def anchors(text):
    """GitHub-style heading slugs plus explicit HTML anchors."""
    text = re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.S)
    found = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', text))
    used = set()
    for title in re.findall(r"^#{1,6} +(.+?) *#*\s*$", text, re.M):
        title = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", title)
        title = html.unescape(re.sub(r"<[^>]+>", "", title)).lower()
        slug = "".join(c for c in title if c in " -_" or unicodedata.category(c)[0] in "LN").replace(" ", "-")
        unique, count = slug, 0
        while unique in used:
            count += 1
            unique = f"{slug}-{count}"
        used.add(unique)
        found.add(unique)
    return found


def strip_code(text):
    text = re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "CODE", text)


def table_rows(text, identifier):
    return [[cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
            for line in text.splitlines()
            if re.match(r"^\|\s*(?:" + identifier + r")\s*\|", line)]


class Audit:
    def __init__(self, root=ROOT, log=print):
        self.root, self.log, self.failures = Path(root).resolve(), log, []

    def check(self, label, ok, detail=""):
        self.log(f"{'OK' if ok else 'FAIL'} {label}")
        if not ok:
            self.failures.append(label)
            if detail:
                self.log(f"  {detail}")

    def read(self, relative):
        try:
            return (self.root / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            self.check(f"read {relative}", False, error)
            return ""

    def validate(self):
        try:
            run = subprocess.run(["node", str(self.root / "scripts/validate-examples.mjs")],
                                 cwd=self.root, capture_output=True, text=True, timeout=180)
            self.log(run.stdout.rstrip())
            self.check("all schemas compile and all examples validate", run.returncode == 0,
                       run.stderr or f"validator exit status {run.returncode}")
        except (OSError, subprocess.TimeoutExpired) as error:
            self.check("schema/example validator runs", False, error)

    def documents(self):
        return {p.relative_to(self.root).as_posix(): self.read(p.relative_to(self.root))
                for p in markdown_files(self.root)}

    def links(self, docs):
        bad = []
        published = set(public_files(self.root))
        published.update(parent for path in list(published) for parent in path.parents
                         if parent == self.root or self.root in parent.parents)
        for source, text in docs.items():
            for match in re.finditer(r"\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\s*\)",
                                     strip_code(text)):
                target = match.group(1) or match.group(2)
                parts = urlsplit(target)
                if parts.scheme or parts.netloc or target == "…":
                    continue
                path = ((self.root / source).parent / unquote(parts.path)).resolve() if parts.path else self.root / source
                try:
                    relative = path.relative_to(self.root)
                except ValueError:
                    bad.append(f"{source}: outside repository: {target}")
                    continue
                if path not in published and (path.exists() or not public_path(relative)):
                    bad.append(f"{source}: private target: {target}")
                elif not path.exists():
                    bad.append(f"{source}: missing target: {target}")
                elif parts.fragment and path.suffix == ".md":
                    if unquote(parts.fragment) not in anchors(self.read(relative)):
                        bad.append(f"{source}: missing fragment: {target}")
        self.check("public Markdown links and fragments resolve", not bad, "\n  ".join(bad))

    def publication(self):
        identifiers = []
        for path in public_files(self.root):
            relative = path.relative_to(self.root).as_posix()
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeError:
                continue
            if re.search(r"\bO-\d+\b", text):
                identifiers.append(relative)
        self.check("internal review identifiers are absent from public files", not identifiers, identifiers)

    def identifiers(self, docs):
        used = set()
        for token, pattern in [
            ("ADR0001-style", r"\bADR\d{3,4}\b"), ("FG-", r"(?<![A-Za-z])FG-\d"),
            ("ED-", r"(?<![A-Za-z])ED-\d"), ("U-", r"(?<![A-Za-z])U-\d"),
            ("agenda letters", r"(?<![A-Za-z0-9-])[ABCEF]-\d[abc]?(?![A-Za-z0-9])"),
            ("vdw:transparent-data", r"vdw:transparent-data"),
            ("VDW Transparent Data", r"VDW Transparent Data"),
        ]:
            hits = {p for p, text in docs.items() if re.search(pattern, text)}
            used.update((token, p) for p in hits if (token, p) in ALLOW)
            self.check(f"no {token} outside provenance records",
                       all((token, p) in ALLOW for p in hits),
                       sorted(p for p in hits if (token, p) not in ALLOW))
        self.check("provenance exceptions still used", used == ALLOW, sorted(ALLOW - used))

    def records(self, docs):
        register = docs.get("adr/decision-register.md", "")
        paths = sorted((self.root / "adr").glob("ADR-*.md"))
        ids = [p.name[:10] for p in paths]
        listed = re.findall(r"^\| \[(ADR-\d{6})\]", register, re.M)
        self.check("ADR files and register rows match without duplicates",
                   bool(ids) and len(ids) == len(set(ids)) and len(listed) == len(set(listed))
                   and set(ids) == set(listed), sorted(set(ids) ^ set(listed)))
        missing = [p.name for p in paths if "Decided by" not in self.read(p.relative_to(self.root))]
        self.check('every ADR carries a "Decided by" line', not missing, missing)
        cited = set(re.findall(r"\bADR-\d{6}\b", "\n".join(docs.values())))
        self.check("every public ADR citation exists", cited <= set(ids), sorted(cited - set(ids)))
    def versions(self, docs):
        surfaces = ["README.md", "docs/technical-guide.md", "docs/glossary.md",
                    "docs/message-properties.md", "docs/naming-conventions.md", "docs/corrugated-faults.md"]
        bad = [p for p in surfaces if not re.search(r"^\*\*Version:\*\* 1\.0(?=\s|$)", docs.get(p, ""), re.M)]
        self.check("all six publication surfaces declare Version 1.0", not bad, bad)
        bad = [p for p, text in docs.items() if re.search(r"0\.9 \(Draft\)|Status:\*\* Working Document", text)]
        self.check("no obsolete draft version labels", not bad, bad)

    def run(self):
        self.validate()
        docs = self.documents()
        self.identifiers(docs)
        self.links(docs)
        self.records(docs)
        self.publication()
        self.versions(docs)
        self.log(f"AUDIT FAILED: {len(self.failures)} checks" if self.failures else
                 "AUDIT CLEAN — consistency checks passed; release approval remains separate.")
        return 1 if self.failures else 0


def main():
    return Audit().run()


if __name__ == "__main__":
    raise SystemExit(main())
