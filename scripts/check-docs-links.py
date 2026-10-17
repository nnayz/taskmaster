#!/usr/bin/env python3
"""Validate internal links and assets in the Zeus documentation books.

Usage:
    python3 scripts/check-docs-links.py [--root REPO]
    python3 scripts/check-docs-links.py --site-build site/build

Modes:
    source (default)  Validate the mdBook sources in ``docs/`` and
                      ``developer-docs/``: every page in SUMMARY.md exists,
                      every markdown file is listed, and every internal link
                      and image resolves (cross-guide links included).
    built             Validate the assembled site build produced by the Pages
                      workflow: every relative href/src in generated HTML
                      resolves to a file in the build tree and every fragment
                      exists in its target page. Attributes and fragments are
                      checked exactly as the browser sees them.

The script only uses the Python standard library. External links (scheme,
protocol-relative, mailto) are ignored by design.
"""

from __future__ import annotations

import argparse
import html.parser
import posixpath
import re
import sys
from pathlib import Path

USER_BOOK = "docs"
DEV_BOOK = "developer-docs"

LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
HTML_ATTR_RE = re.compile(r"""(?:href|src)\s*=\s*(?:"([^"]*)"|'([^']*)')""")
FENCE_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)

EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:", "//")


class PageParser(html.parser.HTMLParser):
    """Collect links, asset references, ids, and meta-refresh targets."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []  # (tag, url)
        self.ids: set[str] = set()
        self.refresh_targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in ("a", "link", "script", "img") and values.get("href"):
            self.links.append((tag, values["href"] or ""))
        if tag in ("img", "script") and values.get("src"):
            self.links.append((tag, values["src"] or ""))
        if values.get("id"):
            self.ids.add(values["id"])
        if values.get("name"):
            self.ids.add(values["name"])
        if tag == "meta" and (values.get("http-equiv") or "").lower() == "refresh":
            content = values.get("content") or ""
            match = re.search(r"url=([^\s;]+)", content, re.IGNORECASE)
            if match:
                self.refresh_targets.append(match.group(1).strip("\"'"))


def is_external(target: str) -> bool:
    return target.startswith(EXTERNAL_PREFIXES)


def split_fragment(target: str) -> tuple[str, str]:
    path, _, fragment = target.partition("#")
    return path, fragment


def summary_pages(summary: Path) -> set[str]:
    """Return the book-relative markdown paths listed in SUMMARY.md."""
    pages: set[str] = set()
    text = summary.read_text(encoding="utf-8")
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip("<>")
        if target.endswith(".md"):
            pages.add(target)
    return pages


def book_pages(src: Path) -> list[Path]:
    return sorted(p for p in src.rglob("*.md") if p.name != "SUMMARY.md")


def source_link_errors(book_root: Path, other_root: Path, label: str) -> list[str]:
    """Validate one book's markdown sources. Returns error strings."""
    errors: list[str] = []
    src = book_root / "src"
    summary = src / "SUMMARY.md"
    if not summary.is_file():
        return [f"{label}: missing {summary}"]

    listed = summary_pages(summary)
    for rel in sorted(listed):
        if not (src / rel).is_file():
            errors.append(f"{label}: SUMMARY.md lists missing page {rel}")

    for page in book_pages(src):
        rel = page.relative_to(src).as_posix()
        if rel not in listed:
            errors.append(
                f"{label}: {src / rel} is not listed in SUMMARY.md "
                "(mdBook will not build it)"
            )

    for page in book_pages(src):
        rel_dir = page.relative_to(src).parent.as_posix()
        text = page.read_text(encoding="utf-8")
        text = FENCE_RE.sub("", text)
        text = INLINE_CODE_RE.sub("", text)
        targets = [m.group(1).strip("<>") for m in LINK_RE.finditer(text)]
        for match in HTML_ATTR_RE.finditer(text):
            targets.append(match.group(1) or match.group(2))
        for raw in targets:
            if not raw or is_external(raw):
                continue
            target, _fragment = split_fragment(raw)
            if not target:
                continue
            if target.startswith("/"):
                errors.append(
                    f"{label}: {page}: site-absolute link not allowed in source: {raw}"
                )
                continue
            resolved = posixpath.normpath(posixpath.join(rel_dir, target))
            if resolved.endswith(".md"):
                if resolved.startswith(".."):
                    errors.append(f"{label}: {page}: link escapes the book: {raw}")
                elif not (src / resolved).is_file():
                    errors.append(f"{label}: {page}: broken link {raw}")
                elif resolved not in listed:
                    errors.append(f"{label}: {page}: link to unlisted page {raw}")
            elif resolved.endswith(".html"):
                mapped = cross_book_source(book_root, resolved)
                if mapped is None:
                    errors.append(
                        f"{label}: {page}: unexpected cross-book link {raw} "
                        "(expected dev/<page>.html from docs/ or "
                        "../<page>.html from developer-docs/)"
                    )
                elif not mapped.is_file():
                    errors.append(f"{label}: {page}: broken cross-guide link {raw}")
            else:
                if not (src / resolved).is_file():
                    errors.append(f"{label}: {page}: missing asset {raw}")

    errors.extend(compat_source_errors(book_root, other_root, label))
    return errors


def cross_book_source(book_root: Path, resolved: str) -> Path | None:
    """Map a book-relative .html link to the other book's markdown source."""
    root = book_root.parent
    if book_root.name == USER_BOOK:
        if not resolved.startswith("dev/") or "/" in resolved[len("dev/"):]:
            return None
        name = resolved[len("dev/"):]
        if not name.endswith(".html"):
            return None
        return root / DEV_BOOK / "src" / (name[: -len(".html")] + ".md")
    if book_root.name == DEV_BOOK:
        if not resolved.startswith("../") or "/" in resolved[3:]:
            return None
        name = resolved[3:]
        if not name.endswith(".html"):
            return None
        return root / USER_BOOK / "src" / (name[: -len(".html")] + ".md")
    return None


def compat_source_errors(book_root: Path, other_root: Path, label: str) -> list[str]:
    """Validate compatibility redirect pages in one book's source."""
    errors: list[str] = []
    src = book_root / "src"
    for page in sorted(src.rglob("*.html")):
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        rel_dir = page.relative_to(src).parent.as_posix()
        targets = parser.refresh_targets + [href for tag, href in parser.links if tag == "a"]
        if not parser.refresh_targets:
            errors.append(f"{label}: {page}: compatibility page has no meta refresh")
        for raw in targets:
            if is_external(raw) or raw.startswith("#"):
                continue
            target, _ = split_fragment(raw)
            if not target:
                continue
            resolved = posixpath.normpath(posixpath.join(rel_dir, target))
            mapped = cross_book_source(book_root, resolved)
            if mapped is None or not mapped.is_file():
                errors.append(
                    f"{label}: {page}: redirect target {raw} does not resolve "
                    "to a page in the other guide"
                )
    return errors


def built_errors(site_build: Path) -> list[str]:
    errors: list[str] = []
    user_index = site_build / "docs" / "index.html"
    dev_index = site_build / "docs" / "dev" / "index.html"
    for index, label in ((user_index, "User Guide"), (dev_index, "Developer Guide")):
        if not index.is_file():
            errors.append(f"built: {label} index missing: {index}")
    if errors:
        return errors

    ids_cache: dict[Path, set[str]] = {}

    def ids_for(path: Path) -> set[str]:
        if path not in ids_cache:
            parser = PageParser()
            parser.feed(path.read_text(encoding="utf-8", errors="replace"))
            ids_cache[path] = parser.ids
        return ids_cache[path]

    checked_links = 0
    for page in sorted((site_build / "docs").rglob("*.html")):
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        page_dir = page.parent
        for tag, raw in parser.links:
            if not raw or is_external(raw) or raw.startswith("#"):
                if raw.startswith("#") and raw[1:] and raw[1:] not in ids_for(page):
                    errors.append(f"built: {page}: missing fragment {raw}")
                continue
            checked_links += 1
            target, fragment = split_fragment(raw)
            if target.endswith(".md"):
                errors.append(f"built: {page}: markdown link leaked into HTML: {raw}")
                continue
            if target.startswith("/"):
                resolved = site_build / target.lstrip("/")
            else:
                resolved = (page_dir / target).resolve()
            if resolved.is_dir():
                resolved = resolved / "index.html"
            try:
                resolved.relative_to(site_build.resolve())
            except ValueError:
                errors.append(f"built: {page}: link escapes the site build: {raw}")
                continue
            if not resolved.is_file():
                errors.append(f"built: {page}: broken {tag} target {raw}")
                continue
            if fragment and resolved.suffix == ".html" and fragment not in ids_for(resolved):
                errors.append(f"built: {page}: missing fragment #{fragment} in {raw}")
        for raw in parser.refresh_targets:
            if is_external(raw):
                continue
            target, _ = split_fragment(raw)
            resolved = (page_dir / target).resolve()
            if not resolved.is_file():
                errors.append(f"built: {page}: redirect target {raw} is missing")

    print(f"checked {checked_links} built links")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root (default: parent of this script)",
    )
    parser.add_argument(
        "--site-build",
        type=Path,
        default=None,
        help="validate an assembled site build directory instead of sources",
    )
    args = parser.parse_args()

    if args.site_build is not None:
        site_build = args.site_build.resolve()
        if not site_build.is_dir():
            print(f"error: {site_build} is not a directory", file=sys.stderr)
            return 2
        errors = built_errors(site_build)
    else:
        root = args.root.resolve()
        user_root = root / USER_BOOK
        dev_root = root / DEV_BOOK
        for book in (user_root, dev_root):
            if not (book / "src").is_dir():
                print(f"error: missing book source {book / 'src'}", file=sys.stderr)
                return 2
        errors = []
        errors += source_link_errors(user_root, dev_root, "user-guide")
        errors += source_link_errors(dev_root, user_root, "developer-guide")

    if errors:
        print(f"{len(errors)} documentation link error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("documentation links OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
