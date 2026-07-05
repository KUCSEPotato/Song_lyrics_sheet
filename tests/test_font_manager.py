from __future__ import annotations

from pathlib import Path

from reportlab.pdfbase import pdfmetrics

from font_manager import FALLBACK_FONT_NAME, register_korean_font


def test_register_korean_font_returns_reportlab_font_name() -> None:
    font_name = register_korean_font(font_name="WorksheetKoreanTest")

    assert isinstance(font_name, str)
    assert font_name
    assert pdfmetrics.getFont(font_name)


def test_register_korean_font_falls_back_when_candidates_are_missing(
    tmp_path: Path,
) -> None:
    font_name = register_korean_font(
        font_name="MissingCandidateFont",
        candidates=[tmp_path / "missing-font.ttf"],
    )

    assert font_name == FALLBACK_FONT_NAME
    assert pdfmetrics.getFont(font_name)
