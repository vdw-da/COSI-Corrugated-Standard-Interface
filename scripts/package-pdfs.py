#!/usr/bin/env python3
"""Package six externally compiled PDFs; never compile or publish documents."""
import argparse
import hashlib
import io
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def package_pdfs(root, version, output_dir, test_pdf_dir=None):
    if not re.fullmatch(r"[0-9]+\.[0-9]+(?:\.[0-9]+)?", version):
        raise ValueError("Version must be numeric, such as 1.0")
    source = (Path(test_pdf_dir) if test_pdf_dir is not None else
              Path(root) / "docs" / "pdf" / version).resolve()
    output_dir = Path(output_dir).resolve()
    if source == output_dir or source in output_dir.parents:
        raise ValueError("Output must be outside the PDF source folder")
    entries = sorted(source.iterdir())
    if len(entries) != 6 or any(p.is_symlink() or not p.is_file() or
                               p.suffix.lower() != ".pdf" for p in entries):
        raise ValueError("The source folder must contain exactly six PDF files and nothing else")
    payloads = {}
    for path in entries:
        if any(c in path.name for c in "\r\n\\"):
            raise ValueError(f"Unsupported PDF filename: {path.name!r}")
        data = path.read_bytes()
        # Basic file-format sanity only; content, visual review and correspondence
        # with Markdown sources remain the reviewer's responsibility.
        if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-1024:]:
            raise ValueError(f"Missing PDF header/end marker: {path.name}")
        payloads[f"docs/pdf/{version}/{path.name}"] = data
    checksums = "".join(f"{hashlib.sha256(data).hexdigest()}  {name}\n"
                        for name, data in payloads.items())
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in payloads.items():
            archive.writestr(name, data)
        archive.writestr("SHA256SUMS", checksums)
        if test_pdf_dir is not None:
            archive.writestr("TEST-ONLY.txt", "TEST ONLY — NOT A RELEASE\n"
                             "These PDFs were supplied for a packaging test. They are not approved\n"
                             "release documents and may predate the current specification.\n")
    suffix = "-TEST" if test_pdf_dir is not None else ""
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"cosi-{version}-pdfs{suffix}.zip"
    with output.open("xb") as stream:
        stream.write(buffer.getvalue())
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="document version, e.g. 1.0")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--test-pdf-dir", type=Path,
                        help="use temporary draft PDFs; output is always marked TEST")
    args = parser.parse_args()
    try:
        output = package_pdfs(ROOT, args.version, args.output_dir, args.test_pdf_dir)
    except (OSError, ValueError) as error:
        parser.exit(1, f"PDF packaging failed: {error}\n")
    print(f"Created {output} (six PDFs plus checksums)")
    print("Packaging does not establish document approval or source/PDF correspondence.")


if __name__ == "__main__":
    main()
