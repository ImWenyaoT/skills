#!/usr/bin/env python3
"""Render the revision page into response-letter LaTeX.

The revision page is the single source of truth. This script does the mechanical
half of the hand-off: it reads the cards, escapes the LaTeX specials, and writes
one file per reviewer plus the substituted metadata.

Usage:
    python3 render_letter.py <revision-page.html> --out <letter-dir>

The page must carry the anchors that references/html-report.md defines:
    <article class="comment-card" data-comment-id="R1-3" data-status="todo">
      <div class="verbatim">…</div>          the reviewer's exact words
      <div class="response-draft">…</div>     optional, becomes reviewerresponse
      <div class="manuscript-change">…</div>  optional, becomes changes
Document order equals letter order, because the template numbers comments with
\\stepcounter.

Only the standard library is used, so the script runs wherever python3 does.
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# LaTeX specials and their replacements. The substitution runs in ONE pass over
# the text, because chained replaces corrupt each other: a backslash becomes
# \textbackslash{}, and a later rule for { would then escape the braces that
# replacement just introduced.
LATEX_SPECIALS: dict[str, str] = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

_SPECIAL_RE = re.compile("[" + re.escape("".join(LATEX_SPECIALS)) + "]")

FIELD_CLASSES = frozenset(
    {
        "verbatim",
        "translation",
        "status-now",
        "evidence",
        "response-draft",
        "manuscript-change",
        "location",
    }
)


def escape_latex(text: str) -> str:
    """Escape the ten LaTeX special characters in one run of plain text.

    A reviewer who writes "95% of cases" or "Smith & Jones" would otherwise
    break the build, or worse, silently comment out the rest of the line.
    """
    return _SPECIAL_RE.sub(lambda match: LATEX_SPECIALS[match.group()], text)


def collapse_space(text: str) -> str:
    """Collapse HTML whitespace into single spaces and trim the ends."""
    return re.sub(r"\s+", " ", text).strip()


class CommentCard:
    """Hold the fields of one comment card."""

    def __init__(self, comment_id: str, status: str, choice: str) -> None:
        """Store the card identity and start with empty fields."""
        self.comment_id = comment_id
        self.status = status
        self.choice = choice
        self.fields: dict[str, str] = {}

    @property
    def reviewer(self) -> str:
        """Return the reviewer key that groups this card, such as R1 or E."""
        return self.comment_id.split("-", 1)[0]

    def field(self, name: str) -> str:
        """Return one collapsed field value, or an empty string."""
        return collapse_space(self.fields.get(name, ""))


class RevisionPageParser(HTMLParser):
    """Extract comment cards from the revision page.

    The parser tracks one card at a time and one field within it. Nested markup
    inside a field (bold, links) contributes its text and is otherwise ignored,
    so a bolded forceful word survives into the letter as plain text.
    """

    def __init__(self) -> None:
        """Initialize the parser with no open card and no open field."""
        super().__init__(convert_charrefs=True)
        self.cards: list[CommentCard] = []
        self._card: CommentCard | None = None
        self._card_depth = 0
        self._field: str | None = None
        self._field_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Open a card or a field when the matching class attribute appears."""
        attributes = {key: (value or "") for key, value in attrs}
        classes = set(attributes.get("class", "").split())

        if self._card is not None:
            self._card_depth += 1
            if self._field is not None:
                self._field_depth += 1
            else:
                matched = classes & FIELD_CLASSES
                if matched:
                    self._field = sorted(matched)[0]
                    self._field_depth = 1
            return

        if "comment-card" in classes:
            comment_id = attributes.get("data-comment-id", "").strip()
            if not comment_id:
                raise SystemExit("a comment-card is missing data-comment-id")
            self._card = CommentCard(
                comment_id=comment_id,
                status=attributes.get("data-status", "").strip(),
                choice=attributes.get("data-choice", "").strip(),
            )
            self._card_depth = 1

    def handle_endtag(self, tag: str) -> None:
        """Close the open field or card as their depth counters unwind."""
        if self._card is None:
            return
        if self._field is not None:
            self._field_depth -= 1
            if self._field_depth == 0:
                self._field = None
        self._card_depth -= 1
        if self._card_depth == 0:
            self.cards.append(self._card)
            self._card = None

    def handle_data(self, data: str) -> None:
        """Accumulate text into the open field."""
        if self._card is not None and self._field is not None:
            self._card.fields[self._field] = self._card.fields.get(self._field, "") + data


def reviewer_title(key: str) -> str:
    """Return the section title for one reviewer key."""
    if key.upper().startswith("E"):
        return "the Editor"
    number = key[1:] or "?"
    return rf"Reviewer \#{number}"


def render_reviewer_file(key: str, cards: list[CommentCard]) -> str:
    """Render one Reviewers/*.tex file.

    The order of the environments sets the printed numbering, so the cards are
    written in the order the page holds them.
    """
    is_editor = key.upper().startswith("E")
    comment_env = "editorcomment" if is_editor else "reviewercomment"
    response_env = "editorresponse" if is_editor else "reviewerresponse"

    lines = [
        "% " + "=" * 79,
        f"% {reviewer_title(key)} — generated from the revision page.",
        "% The order of these environments sets the printed numbering. Do not sort them.",
        "% " + "=" * 79,
    ]
    if not is_editor:
        lines.append(rf"\startReviewerSection{{{reviewer_title(key)}}}")
    lines.append("")

    for card in cards:
        verbatim = card.field("verbatim")
        if not verbatim:
            raise SystemExit(
                f"{card.comment_id}: the verbatim field is empty. "
                "A comment block must quote the reviewer, so the letter cannot be generated."
            )
        lines.append(f"% --- {card.comment_id} ({card.status or 'no status'}) ---")
        lines.append(rf"\begin{{{comment_env}}}")
        lines.append(escape_latex(verbatim))
        lines.append(rf"\end{{{comment_env}}}")
        lines.append(rf"\begin{{{response_env}}}")

        draft = card.field("response-draft")
        lines.append(
            escape_latex(draft)
            if draft
            else f"{{{{RESPONSE-TO-{card.comment_id}}}}}  % no draft on the page yet"
        )

        change = card.field("manuscript-change")
        if change:
            lines.append(r"\begin{changes}")
            lines.append(escape_latex(change))
            lines.append(r"\end{changes}")

        location = card.field("location")
        if location:
            lines.append(f"% lands in: {escape_latex(location)}")
        lines.append(rf"\end{{{response_env}}}")
        lines.append("")

    return "\n".join(lines) + "\n"


def group_by_reviewer(cards: list[CommentCard]) -> dict[str, list[CommentCard]]:
    """Group cards by reviewer key while preserving document order."""
    grouped: dict[str, list[CommentCard]] = {}
    for card in cards:
        grouped.setdefault(card.reviewer, []).append(card)
    return grouped


def main(argv: list[str] | None = None) -> int:
    """Parse the page and write the reviewer files."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("page", type=Path, help="the revision page HTML")
    parser.add_argument("--out", type=Path, required=True, help="letter directory")
    args = parser.parse_args(argv)

    try:
        html = args.page.read_text(encoding="utf-8")
    except OSError as error:
        print(f"cannot read the revision page: {error}", file=sys.stderr)
        return 1

    page_parser = RevisionPageParser()
    page_parser.feed(html)
    if not page_parser.cards:
        print(
            "no comment cards found. The page must use "
            '<article class="comment-card" data-comment-id="...">.',
            file=sys.stderr,
        )
        return 1

    reviewers_dir = args.out / "Reviewers"
    reviewers_dir.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    for key, cards in group_by_reviewer(page_parser.cards).items():
        name = "Editor" if key.upper().startswith("E") else key
        target = reviewers_dir / f"{name}.tex"
        target.write_text(render_reviewer_file(key, cards), encoding="utf-8")
        written.append(f"{target} ({len(cards)} comments)")

    for line in written:
        print(f"wrote {line}")
    drafted = sum(1 for card in page_parser.cards if card.field("response-draft"))
    print(f"{drafted}/{len(page_parser.cards)} comments carry a response draft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
