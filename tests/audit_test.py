"""Regression tests for public validation and publication boundaries."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit import Audit, markdown_files, public_files


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cosi-audit-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for path in markdown_files(ROOT):
            dest = self.root / path.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
        self.output = []
        self.audit = Audit(self.root, self.output.append)

    def write(self, path, text):
        path = self.root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def change_register(self, transform):
        path = "adr/decision-register.md"
        self.write(path, transform(self.audit.read(path)))

    def records(self):
        self.audit.records(self.audit.documents())

    def test_public_enumeration_excludes_private_backups_and_local_rules(self):
        self.write("tmp/backup/README.md", "[broken](missing.md) O-" + "99")
        self.write(".local/config.md", "[broken](missing.md)")
        docs = self.audit.documents()
        self.assertNotIn("tmp/backup/README.md", docs)
        self.assertNotIn(".local/config.md", docs)
        self.audit.publication()
        self.assertFalse(self.audit.failures, self.output)

    def test_validator_exit_status_cannot_be_overridden_by_success_text(self):
        result = subprocess.CompletedProcess([], 1, "OK example\n" * 9, "fatal error")
        with patch("audit.subprocess.run", return_value=result):
            self.audit.validate()
        self.assertTrue(self.audit.failures)
        self.assertIn("fatal error", "\n".join(self.output))

    def test_validator_has_no_fixed_example_count(self):
        result = subprocess.CompletedProcess([], 0, "PASS 10/10 examples valid", "")
        with patch("audit.subprocess.run", return_value=result):
            self.audit.validate()
        self.assertFalse(self.audit.failures)

    def test_missing_validator_fails(self):
        with patch("audit.subprocess.run", side_effect=FileNotFoundError("node")):
            self.audit.validate()
        self.assertTrue(self.audit.failures)

    def test_register_is_valid_in_source_archive(self):
        self.records()
        self.audit.publication()
        self.assertFalse((self.root / "tmp").exists())
        self.assertFalse(self.audit.failures, self.output)

    def test_internal_identifiers_rejected_in_prose_json_and_workflow(self):
        for name in ["README.md", "examples/leak.json", ".github/workflows/leak.yml"]:
            with self.subTest(name=name):
                original = (self.root / name).read_text() if (self.root / name).exists() else None
                self.write(name, '"O-' + '99"')
                self.audit.failures.clear()
                self.audit.publication()
                self.assertIn("internal review identifiers are absent from public files", self.audit.failures)
                if original is None:
                    (self.root / name).unlink()
                else:
                    self.write(name, original)

    def test_duplicate_and_missing_adr_rows_fail(self):
        original = self.audit.read("adr/decision-register.md")
        row = next(line for line in original.splitlines() if line.startswith("| [ADR-000001]"))
        for modified in [original + "\n" + row, original.replace(row, "")]:
            with self.subTest(modified=modified[-80:]):
                self.write("adr/decision-register.md", modified)
                self.audit.failures.clear()
                self.records()
                self.assertIn("ADR files and register rows match without duplicates", self.audit.failures)

    def test_unknown_citations_and_missing_adr_fail(self):
        self.write("README.md", "ADR-999999")
        (self.root / "adr/ADR-000001-quality-message-end-of-job-mandatory.md").unlink()
        self.records()
        self.assertIn("every public ADR citation exists", self.audit.failures)
        self.assertIn("ADR files and register rows match without duplicates", self.audit.failures)

    def test_link_targets_checked_including_private_paths_and_fragments(self):
        self.write("tmp/exists.md", "private")
        self.write("other.md", '<a id="kept"></a>')
        self.write("README.md", "[missing](missing.md) [private](tmp/exists.md) "
                   "[wrong anchor](other.md#absent) [quoted](`missing2.md`)")
        self.audit.links(self.audit.documents())
        output = "\n".join(self.output)
        self.assertIn("missing target: missing.md", output)
        self.assertIn("private target: tmp/exists.md", output)
        self.assertIn("missing fragment: other.md#absent", output)

    def test_headings_and_explicit_anchors_without_agenda(self):
        self.write("other.md", '# Common `value`\n## Common `value`\n<a id="kept"></a>')
        self.write("README.md", "[first](other.md#common-value) [second](other.md#common-value-1) "
                   "[explicit](other.md#kept) `[not a link](missing.md)`")
        docs = {p: self.audit.read(p) for p in ["README.md", "other.md"]}
        self.audit.links(docs)
        self.assertFalse(self.audit.failures, self.output)

    def test_missing_document_and_incorrect_version_fail(self):
        docs = self.audit.documents()
        self.audit.versions(docs)
        self.assertFalse(self.audit.failures, self.output)
        del docs["docs/glossary.md"]
        docs["README.md"] = "**Version:** 1.0.1"
        self.audit.versions(docs)
        self.assertIn("all six publication surfaces declare Version 1.0", self.audit.failures)

    def test_git_inventory_respects_local_exclusions_and_checks_tracked_files(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.write(".git/info/exclude", "personal-notes.md\nlocal-work/\n")
        self.write("personal-notes.md", "not published")
        self.write("local-work/draft.md", "not published")
        self.write("public-new.md", "published")
        self.write("tracked.md", "published")
        subprocess.run(["git", "-C", str(self.root), "add", "tracked.md"], check=True)
        self.write(".gitignore", "tracked.md\n")
        files = {p.relative_to(self.root).as_posix() for p in public_files(self.root)}
        self.assertNotIn("personal-notes.md", files)
        self.assertNotIn("local-work/draft.md", files)
        self.assertIn("public-new.md", files)
        self.assertIn("tracked.md", files)
        self.write("README.md", "[private](personal-notes.md) [directory](local-work/)")
        self.audit.links(self.audit.documents())
        self.assertIn("private target: personal-notes.md", "\n".join(self.output))
        self.assertIn("private target: local-work/", "\n".join(self.output))
        self.write("tracked.md", "O-" + "99")
        self.audit.publication()
        self.assertIn("internal review identifiers are absent from public files", self.audit.failures)

    def test_adr_without_deciding_authority_fails(self):
        path = "adr/ADR-000001-quality-message-end-of-job-mandatory.md"
        self.write(path, self.audit.read(path).replace("Decided by", "Unattributed"))
        self.records()
        self.assertIn('every ADR carries a "Decided by" line', self.audit.failures)


if __name__ == "__main__":
    unittest.main()
