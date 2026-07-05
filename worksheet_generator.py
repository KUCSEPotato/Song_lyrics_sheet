from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, SimpleDocTemplate, Table, TableStyle

from font_manager import register_korean_font

DEFAULT_TITLE = "가사 따라쓰기 학습지"
PDF_AUTHOR = "Lyrics Worksheet Generator"

MIN_COLUMNS = 6
MAX_COLUMNS = 20
MIN_PRACTICE_ROWS = 1
MAX_PRACTICE_ROWS = 3


@dataclass(frozen=True)
class LayoutConfig:
    left_margin: float = 20 * mm
    right_margin: float = 20 * mm
    top_margin: float = 26 * mm
    bottom_margin: float = 22 * mm
    max_lyric_font_size: float = 22
    min_lyric_font_size: float = 10
    font_size_ratio: float = 0.52


LAYOUT = LayoutConfig()
GRID_COLOR = colors.HexColor("#222222")


def create_worksheet_pdf(
    *,
    title: str,
    lyrics: str,
    output_path: str | Path,
    columns: int = 12,
    practice_rows: int = 1,
) -> Path:
    """Create a Korean lyrics handwriting worksheet PDF and return its path."""
    normalized_title = title.strip() or DEFAULT_TITLE
    _validate_inputs(lyrics=lyrics, columns=columns, practice_rows=practice_rows)

    output = _normalize_output_path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    font_name = register_korean_font()
    usable_width = A4[0] - LAYOUT.left_margin - LAYOUT.right_margin
    cell_width = usable_width / columns
    rows_per_page = _rows_per_page(
        cell_size=cell_width,
        practice_rows=practice_rows,
    )

    document = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=LAYOUT.left_margin,
        rightMargin=LAYOUT.right_margin,
        topMargin=LAYOUT.top_margin,
        bottomMargin=LAYOUT.bottom_margin,
        title=normalized_title,
        author=PDF_AUTHOR,
    )

    story = _build_story(
        lyrics=lyrics,
        columns=columns,
        practice_rows=practice_rows,
        cell_width=cell_width,
        rows_per_page=rows_per_page,
        font_name=font_name,
    )

    def set_metadata(canvas, doc) -> None:
        canvas.saveState()
        canvas.setTitle(normalized_title)
        canvas.setAuthor(PDF_AUTHOR)
        canvas.restoreState()

    document.build(story, onFirstPage=set_metadata, onLaterPages=set_metadata)
    return output


def _validate_inputs(*, lyrics: str, columns: int, practice_rows: int) -> None:
    if not lyrics.strip():
        raise ValueError("가사를 입력해 주세요.")
    if not MIN_COLUMNS <= columns <= MAX_COLUMNS:
        raise ValueError("한 줄 칸 수는 6에서 20 사이여야 합니다.")
    if not MIN_PRACTICE_ROWS <= practice_rows <= MAX_PRACTICE_ROWS:
        raise ValueError("연습 행 수는 1에서 3 사이여야 합니다.")


def _normalize_output_path(output_path: str | Path) -> Path:
    path = Path(output_path).expanduser()
    if not path.suffix:
        return path.with_suffix(".pdf")
    return path


def _build_story(
    *,
    lyrics: str,
    columns: int,
    practice_rows: int,
    cell_width: float,
    rows_per_page: int,
    font_name: str,
) -> list:
    row_groups = _build_row_groups(
        lyrics=lyrics,
        columns=columns,
        practice_rows=practice_rows,
    )
    pages = _paginate_row_groups(row_groups, rows_per_page)

    story: list = []
    for page_index, page_rows in enumerate(pages):
        if page_index > 0:
            story.append(PageBreak())
        story.append(
            _create_grid_table(
                rows=_pad_rows(page_rows, columns, rows_per_page),
                cell_width=cell_width,
                font_name=font_name,
            )
        )

    return story


def _rows_per_page(*, cell_size: float, practice_rows: int) -> int:
    available_height = A4[1] - LAYOUT.top_margin - LAYOUT.bottom_margin
    group_height = practice_rows + 1
    max_rows = int(available_height // cell_size)
    groups_per_page = max(1, max_rows // group_height)
    return groups_per_page * group_height


def _build_row_groups(
    *,
    lyrics: str,
    columns: int,
    practice_rows: int,
) -> list[list[list[str]]]:
    groups: list[list[list[str]]] = []

    for original_line in lyrics.splitlines():
        if original_line == "":
            groups.append(_blank_group(columns, practice_rows))
            continue

        for chunk in _split_line(original_line, columns):
            display_row = ["" if _is_spacing_character(char) else char for char in chunk]
            display_row.extend([""] * (columns - len(display_row)))
            groups.append(
                [display_row]
                + [[""] * columns for _ in range(practice_rows)]
            )

    return groups


def _blank_group(columns: int, practice_rows: int) -> list[list[str]]:
    return [[""] * columns for _ in range(practice_rows + 1)]


def _paginate_row_groups(
    row_groups: list[list[list[str]]],
    rows_per_page: int,
) -> list[list[list[str]]]:
    pages: list[list[list[str]]] = []
    current_page: list[list[str]] = []

    for group in row_groups:
        if current_page and len(current_page) + len(group) > rows_per_page:
            pages.append(current_page)
            current_page = []
        current_page.extend(group)

    if current_page:
        pages.append(current_page)

    return pages


def _pad_rows(
    rows: list[list[str]],
    columns: int,
    rows_per_page: int,
) -> list[list[str]]:
    padded_rows = list(rows)
    while len(padded_rows) < rows_per_page:
        padded_rows.append([""] * columns)
    return padded_rows


def _split_line(line: str, columns: int) -> list[list[str]]:
    characters = list(line)
    return [characters[start : start + columns] for start in range(0, len(characters), columns)]


def _create_grid_table(
    *,
    rows: list[list[str]],
    cell_width: float,
    font_name: str,
) -> Table:
    font_size = max(
        LAYOUT.min_lyric_font_size,
        min(LAYOUT.max_lyric_font_size, cell_width * LAYOUT.font_size_ratio),
    )

    table = Table(
        rows,
        colWidths=[cell_width] * len(rows[0]),
        rowHeights=[cell_width] * len(rows),
        hAlign="CENTER",
    )

    style_commands = [
        ("GRID", (0, 0), (-1, -1), 0.6, GRID_COLOR),
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]

    table.setStyle(TableStyle(style_commands))
    return table


def _is_spacing_character(char: str) -> bool:
    return char.isspace()
