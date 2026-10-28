import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location("package_pdfs", Path(__file__).resolve().parents[1] / "scripts/package-pdfs.py")
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cosi-pdf-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pdfs = self.root / "drafts"
        self.pdfs.mkdir()
        # Minimal marker fixtures test packaging, not PDF rendering or validity.
        for i in range(6):
            (self.pdfs / f"document-{i}.pdf").write_bytes(f"%PDF-1.7\nfixture {i}\n%%EOF\n".encode())

    def package(self):
        return packager.package_pdfs(self.root, "1.0", self.root / "output", self.pdfs)

    def test_draft_archive_is_marked_and_preserves_files_and_checksums(self):
        output = self.package()
        self.assertTrue(output.name.endswith("-TEST.zip"))
        with zipfile.ZipFile(output) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(len(archive.namelist()), 8)
            self.assertIn(b"NOT A RELEASE", archive.read("TEST-ONLY.txt"))
            for line in archive.read("SHA256SUMS").decode().splitlines():
                digest, name = line.split("  ", 1)
                data = archive.read(name)
                self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
                self.assertEqual(data, (self.pdfs / Path(name).name).read_bytes())
        self.assertFalse((self.root / "docs/pdf/1.0").exists())

    def test_normal_mode_uses_only_versioned_repository_folder(self):
        with self.assertRaises(FileNotFoundError):
            packager.package_pdfs(self.root, "1.0", self.root / "output")
        source = self.root / "docs/pdf/1.0"
        source.parent.mkdir(parents=True)
        self.pdfs.rename(source)
        output = packager.package_pdfs(self.root, "1.0", self.root / "output")
        with zipfile.ZipFile(output) as archive:
            self.assertNotIn("TEST-ONLY.txt", archive.namelist())
            self.assertEqual(len(archive.namelist()), 7)

    def test_missing_or_extra_files_fail(self):
        extra = self.pdfs / "build.log"
        extra.write_text("intermediate")
        with self.assertRaises(ValueError):
            self.package()
        extra.unlink()
        extra_pdf = self.pdfs / "extra.pdf"
        extra_pdf.write_bytes(b"%PDF-1.7\n%%EOF\n")
        with self.assertRaisesRegex(ValueError, "exactly six"):
            self.package()
        extra_pdf.unlink()
        (self.pdfs / "document-0.pdf").unlink()
        with self.assertRaises(ValueError):
            self.package()

    def test_directories_symlinks_and_non_PDF_content_fail(self):
        path = self.pdfs / "document-0.pdf"
        path.unlink()
        path.mkdir()
        with self.assertRaises(ValueError):
            self.package()
        path.rmdir()
        path.symlink_to(self.pdfs / "document-1.pdf")
        with self.assertRaises(ValueError):
            self.package()
        path.unlink()
        path.write_bytes(b"not a PDF")
        with self.assertRaises(ValueError):
            self.package()

    def test_does_not_overwrite_an_existing_archive_or_pollute_source_folder(self):
        output = self.package()
        before = output.read_bytes()
        with self.assertRaises(FileExistsError):
            self.package()
        self.assertEqual(output.read_bytes(), before)
        with self.assertRaises(ValueError):
            packager.package_pdfs(self.root, "1.0", self.pdfs, self.pdfs)

    def test_version_cannot_escape_archive_directory(self):
        with self.assertRaises(ValueError):
            packager.package_pdfs(self.root, "../other", self.root / "output", self.pdfs)


if __name__ == "__main__":
    unittest.main()
