"""Create a plain text document from a PDF, with each paragraph on a single line.

Requires PyMuPDF: pip install pymupdf

Usage: python pdf_to_text.py input.pdf [output_path]
"""

import re
import statistics
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import pymupdf

LIST_MARKER = r"(?:\(?\d{1,3}[.)]|\(?[A-Za-z][.)]|\(?[ivxIVX]{1,5}[.)]|[•·▪◦‣*–\-])"
STARTS_WITH_MARKER = re.compile(LIST_MARKER + r"(?:\s|$)")
ONLY_MARKER = re.compile(LIST_MARKER + r"$")
PAGE_NUMBER = re.compile(r"\W*(?:page\s*)?\d+\W*$", re.IGNORECASE)

HEADER_FOOTER_ZONE = 0.08  # Share of the page height at the top and bottom
PARAGRAPH_GAP = 1.3  # Line spacing ratio above which a gap separates paragraphs
FIRST_LINE_INDENT = 8  # Points
MIN_SHORT_LINE = 60  # Points of unused width before a line counts as short
SHORT_LINE_RATIO = 0.15  # The same limit, as a share of the text width
SPAN_GAP = 0.15  # Gap between text pieces that counts as a space, relative to font size


@dataclass
class Line:
    text: str
    page: int
    x0: float
    y0: float
    x1: float
    in_margin: bool
    style: tuple
    left_edge: float = 0.0
    right_edge: float = 0.0


def join_spans(spans):
    """Text after a tab, such as a list item after its marker, has a gap but no space."""
    text = ""
    previous = None
    for span in spans:
        if previous and span["bbox"][0] - previous["bbox"][2] > span["size"] * SPAN_GAP:
            text += " "
        text += span["text"]
        previous = span
    return " ".join(text.split())


def read_line(raw_line, page_number, page_height):
    spans = [span for span in raw_line["spans"] if span["text"].strip()]
    if not spans:
        return None

    styles = Counter()
    for span in spans:
        is_bold = bool(span["flags"] & pymupdf.TEXT_FONT_BOLD)
        styles[(round(span["size"] * 2) / 2, is_bold)] += len(span["text"])

    x0, y0, x1, y1 = raw_line["bbox"]
    center = (y0 + y1) / 2 / page_height
    return Line(
        text=join_spans(spans),
        page=page_number,
        x0=x0,
        y0=y0,
        x1=x1,
        in_margin=center < HEADER_FOOTER_ZONE or center > 1 - HEADER_FOOTER_ZONE,
        style=styles.most_common(1)[0][0],
    )


def merge_markers_with_text(lines):
    """Word and others often place a list marker and its text in separate lines."""
    merged = []
    for line in lines:
        previous = merged[-1] if merged else None
        if (
            previous
            and ONLY_MARKER.match(previous.text)
            and line.page == previous.page
            and line.x0 > previous.x0
            and abs(line.y0 - previous.y0) < 6
        ):
            line.text = f"{previous.text} {line.text}"
            line.x0 = previous.x0
            merged[-1] = line
        else:
            merged.append(line)
    return merged


def read_lines(document):
    flags = pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_LIGATURES
    lines = []
    for page_number, page in enumerate(document):
        for block in page.get_text("dict", flags=flags, sort=False)["blocks"]:
            read = (read_line(raw, page_number, page.rect.height) for raw in block.get("lines", []))
            block_lines = [line for line in read if line]
            for line in block_lines:
                line.left_edge = min(other.x0 for other in block_lines)
                line.right_edge = max(other.x1 for other in block_lines)
            lines.extend(block_lines)
    return merge_markers_with_text(lines)


def remove_headers_and_footers(lines, page_count):
    def pattern(line):
        return re.sub(r"\d+", "#", line.text.lower())

    pages_by_pattern = {}
    for line in lines:
        if line.in_margin:
            pages_by_pattern.setdefault(pattern(line), set()).add(line.page)

    min_pages = max(2, page_count / 2)
    return [
        line
        for line in lines
        if not (
            line.in_margin
            and (PAGE_NUMBER.match(line.text) or len(pages_by_pattern[pattern(line)]) >= min_pages)
        )
    ]


def typical_line_spacing(lines):
    gaps = [
        line.y0 - previous.y0
        for previous, line in zip(lines, lines[1:])
        if line.page == previous.page and line.y0 > previous.y0
    ]
    return statistics.median(gaps) if gaps else 0


def ends_short(line):
    width = line.right_edge - line.left_edge
    return line.right_edge - line.x1 > max(MIN_SHORT_LINE, width * SHORT_LINE_RATIO)


def starts_new_paragraph(previous, line, in_list, line_spacing):
    if STARTS_WITH_MARKER.match(line.text) or line.style != previous.style or ends_short(previous):
        return True

    gap = line.y0 - previous.y0
    if line.page != previous.page or gap <= 0:
        # Page or column break. Spacing says nothing here, so use the text itself.
        return previous.text.endswith((".", "!", "?", ":")) and not line.text[0].islower()

    if gap > line_spacing * PARAGRAPH_GAP:
        return True
    return not in_list and line.x0 - previous.x0 > FIRST_LINE_INDENT


def join_lines(text, next_text):
    if text.endswith("­"):
        return text[:-1] + next_text
    if re.search(r"\w-$", text) and next_text[0].islower():
        return text[:-1] + next_text
    return f"{text} {next_text}"


def build_paragraphs(lines):
    line_spacing = typical_line_spacing(lines)
    paragraphs = []  # Pairs of (text, is_list_item)
    previous = None
    for line in lines:
        in_list = bool(paragraphs) and paragraphs[-1][1]
        if previous is None or starts_new_paragraph(previous, line, in_list, line_spacing):
            paragraphs.append((line.text, bool(STARTS_WITH_MARKER.match(line.text))))
        else:
            paragraphs[-1] = (join_lines(paragraphs[-1][0], line.text), in_list)
        previous = line
    return paragraphs


def render(paragraphs):
    text = ""
    previous_is_list = False
    for paragraph, is_list in paragraphs:
        if text:
            text += "\n" if previous_is_list and is_list else "\n\n"
        text += paragraph
        previous_is_list = is_list
    return text + "\n"


def main():
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {Path(sys.argv[0]).name} input.pdf [output_path]")

    source = Path(sys.argv[1])
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else source.with_suffix(".txt")

    if not source.is_file():
        sys.exit(f"File not found: {source}")

    with pymupdf.open(source) as document:
        lines = remove_headers_and_footers(read_lines(document), document.page_count)

    if not lines:
        sys.exit(f"No text found in {source}. It may be a scanned PDF, which needs OCR first.")

    output.write_text(render(build_paragraphs(lines)), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
