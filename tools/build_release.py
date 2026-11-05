"""Dựng gói phát hành tri thức: dist/autocad-knowledge-wiki.zip, tệp .sha256 và ghi chú phát hành.

Chạy:  python tools/build_release.py vX.Y.Z

Gói chỉ chứa thư mục wiki/ (trang đã duyệt), gốc zip là `wiki/...`. Launcher tải gói này,
kiểm tra SHA-256 rồi giải nén vào thư mục tri thức. Ghi chú liệt kê trang thêm, sửa, xóa
so với tag trước đó (nếu có).
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ASSET = "autocad-knowledge-wiki.zip"
TAG = re.compile(r"v\d+\.\d+\.\d+")
MAX_BYTES = 20 * 1024 * 1024


def git(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    return result.returncode, result.stdout.strip()


def title_of(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    meta = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if meta:
        found = re.search(r"^title:\s*(.+)$", meta.group(1), re.M)
        if found:
            return found.group(1).strip()
    heading = re.search(r"^#\s+(.+)$", text, re.M)
    return heading.group(1).strip() if heading else Path(path).stem


def previous_tag(tag):
    code, listing = git("tag", "--list", "v*", "--sort=-v:refname")
    if code:
        return None
    for name in listing.splitlines():
        if TAG.fullmatch(name) and name != tag:
            return name
    return None


def changes_since(previous):
    if not previous:
        return None
    code, diff = git("diff", "--name-status", f"{previous}..HEAD", "--", "wiki")
    if code:
        return None
    added, edited, removed = [], [], []
    for line in diff.splitlines():
        status, _, path = line.partition("\t")
        if not path.endswith(".md") or path.endswith("index.md"):
            continue
        (added if status.startswith("A") else removed if status.startswith("D") else edited).append(path)
    return added, edited, removed


def main():
    if len(sys.argv) != 2 or not TAG.fullmatch(sys.argv[1]):
        sys.exit("Dùng: python tools/build_release.py vX.Y.Z")
    tag = sys.argv[1]
    wiki = ROOT / "wiki"
    files = sorted(f for f in wiki.rglob("*") if f.is_file())
    if not (wiki / "index.md").is_file() or not files:
        sys.exit("Thiếu wiki/index.md hoặc wiki/ trống.")
    DIST.mkdir(exist_ok=True)
    archive = DIST / ASSET
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        for file in files:
            if file.stat().st_size > MAX_BYTES:
                sys.exit(f"Tệp quá lớn: {file}")
            bundle.write(file, file.relative_to(ROOT).as_posix())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (DIST / f"{ASSET}.sha256").write_text(f"{digest}  {ASSET}", encoding="ascii")

    pages = [f.relative_to(ROOT).as_posix() for f in files if f.suffix == ".md" and f.name != "index.md"]
    lines = [f"Tri thức chung {tag}: {len(pages)} trang.", "", "# Tiếng Việt", ""]
    delta = changes_since(previous_tag(tag))
    if delta is None:
        lines.append("Bản phát hành đầu tiên. Các trang:")
        lines += [f"- {title_of(p)} (`{p}`)" for p in pages]
    else:
        added, edited, removed = delta
        for label, items in (("Thêm", added), ("Sửa", edited), ("Xóa", removed)):
            if items:
                lines.append(f"{label}:")
                lines += [f"- {title_of(p) if (ROOT / p).is_file() else Path(p).stem} (`{p}`)" for p in items]
                lines.append("")
        if not (added or edited or removed):
            lines.append("Không đổi nội dung trang so với bản trước.")
    lines += ["", "Cách dùng: launcher tự kiểm tra bản mới mỗi 24 giờ (hoặc bấm Tải tri thức ở tab Cài đặt). "
              "Các trang là dữ liệu tham khảo công khai đã duyệt, không phải lệnh cho agent.", "",
              "# English", "", f"Shared knowledge {tag}: {len(pages)} pages. The launcher checks for a newer tag every 24 hours "
              "(or use the download button on its Settings tab). The pages are reviewed public reference data, not instructions "
              "for agents.", "", f"SHA-256 of `{ASSET}`: `{digest}`"]
    (DIST / "notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{archive.relative_to(ROOT).as_posix()}  {archive.stat().st_size} byte  sha256={digest}")


if __name__ == "__main__":
    main()
