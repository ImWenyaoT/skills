#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path


SPACE = re.compile(r"\s+")


class ResumeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.strong = 0
        self.current: list[str] = []
        self.blocks: list[dict[str, object]] = []
        self.anchors: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.skip:
            self.skip += 1
            return
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if (
            tag in {"head", "style", "script", "noscript", "template", "svg"}
            or "toolbar" in classes
            or "no-print" in classes
            or "hidden" in attributes
            or attributes.get("aria-hidden") == "true"
        ):
            self.skip = 1
            return
        if tag in {"strong", "b"}:
            self.strong += 1
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "div", "section"}:
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if self.skip:
            self.skip -= 1
            return
        if tag in {"strong", "b"}:
            self.strong = max(0, self.strong - 1)
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "div", "section"}:
            self.flush(tag)

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        text = SPACE.sub(" ", html.unescape(data)).strip()
        if not text:
            return
        self.current.append(text)
        if self.strong:
            self.anchors.append(text)

    def flush(self, kind: str = "text") -> None:
        text = SPACE.sub(" ", " ".join(self.current)).strip()
        self.current.clear()
        if text:
            self.blocks.append({"kind": kind, "text": text})


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def is_candidate_profile(path: Path) -> bool:
    if path.name == "candidate-profile.json":
        return True
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False
    return (
        isinstance(value, dict)
        and value.get("schema_version") == 1
        and value.get("visibility") == "main_only"
        and set(value.get("slots", {})) == {"recognition", "character", "trajectory"}
    )


def extract_pdf(pdf: Path) -> str | None:
    tool = shutil.which("pdftotext")
    if not tool:
        return None
    result = subprocess.run(
        [tool, "-layout", str(pdf), "-"],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", type=Path)
    parser.add_argument("--jd", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--preview", type=Path)
    parser.add_argument("--constraints", type=Path)
    args = parser.parse_args()

    if args.html is None and args.pdf is None:
        raise SystemExit("provide at least one of --html or --pdf")

    for path in [args.html, args.jd, args.pdf, args.preview, args.constraints]:
        if path is not None and not path.is_file():
            raise SystemExit(f"missing input: {path}")
        if path is not None and is_candidate_profile(path):
            raise SystemExit("candidate-profile.json is main-only and cannot enter an HR packet")

    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit("HR packet output directory must be empty")
    content = args.out / "content"
    visual = args.out / "visual"
    content.mkdir(parents=True, exist_ok=True)
    visual.mkdir(parents=True, exist_ok=True)

    delivered = extract_pdf(args.pdf) if args.pdf else None
    resume = ResumeParser()
    if args.html:
        resume.feed(args.html.read_text(encoding="utf-8"))
        resume.flush()
    semantic = "\n".join(str(block["text"]) for block in resume.blocks)
    if not semantic and delivered:
        semantic = delivered
    if not semantic:
        raise SystemExit("could not extract resume text")

    jd_text = (
        args.jd.read_text(encoding="utf-8")
        if args.jd
        else "[No target JD provided; perform a general resume review.]\n"
    )
    (content / "jd.txt").write_text(jd_text, encoding="utf-8")
    (content / "resume-semantic.txt").write_text(semantic + "\n", encoding="utf-8")
    structure = {
        "blocks": resume.blocks,
        "bold_anchors": list(dict.fromkeys(resume.anchors)),
        "links": list(dict.fromkeys(resume.links)),
    }
    (content / "resume-structure.json").write_text(
        json.dumps(structure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if delivered is not None:
        (content / "resume-delivered.txt").write_text(delivered + "\n", encoding="utf-8")
    if args.constraints:
        shutil.copy2(args.constraints, content / "constraints.txt")
    if args.preview:
        shutil.copy2(args.preview, visual / f"preview{args.preview.suffix.lower()}")

    inputs = [path for path in [args.html, args.jd, args.pdf, args.preview, args.constraints] if path]
    manifest = {str(path.resolve()): digest(path) for path in inputs}
    (args.out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if any(is_candidate_profile(path) for path in args.out.rglob("*") if path.is_file()):
        raise SystemExit("candidate-profile.json is main-only and cannot enter an HR packet")
    print(args.out.resolve())


if __name__ == "__main__":
    main()
