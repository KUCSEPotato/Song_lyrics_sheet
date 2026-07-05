from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Sequence

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont

LOGGER = logging.getLogger(__name__)

DEFAULT_FONT_NAME = "WorksheetKorean"
FALLBACK_FONT_NAME = "HYSMyeongJo-Medium"

WINDOWS_FONT_CANDIDATES = (
    Path("C:/Windows/Fonts/malgun.ttf"),
    Path("C:/Windows/Fonts/malgunbd.ttf"),
)

MACOS_FONT_CANDIDATES = (
    Path("/System/Library/Fonts/AppleSDGothicNeo.ttc"),
    Path("/System/Library/Fonts/AppleGothic.ttf"),
    Path("/Library/Fonts/NanumGothic.ttf"),
)

LINUX_FONT_CANDIDATES = (
    Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/opentype/noto/NotoSansCJKkr-Regular.otf"),
)


def candidate_font_paths() -> tuple[Path, ...]:
    """Return Korean-capable system font candidates for the current OS."""
    if sys.platform.startswith("win"):
        return WINDOWS_FONT_CANDIDATES
    if sys.platform == "darwin":
        return MACOS_FONT_CANDIDATES
    if sys.platform.startswith("linux"):
        return LINUX_FONT_CANDIDATES
    return WINDOWS_FONT_CANDIDATES + MACOS_FONT_CANDIDATES + LINUX_FONT_CANDIDATES


def register_korean_font(
    *,
    font_name: str = DEFAULT_FONT_NAME,
    candidates: Sequence[Path] | None = None,
) -> str:
    """Register and return a ReportLab font name that can render Korean text."""
    paths = tuple(candidates) if candidates is not None else candidate_font_paths()

    if _is_registered(font_name):
        return font_name

    for font_path in paths:
        if not font_path.exists():
            continue

        try:
            pdfmetrics.registerFont(
                TTFont(font_name, str(font_path), subfontIndex=0)
            )
            return font_name
        except Exception:
            LOGGER.debug(
                "Failed to register Korean font: %s",
                font_path,
                exc_info=True,
            )

    return _register_fallback_font()


def _register_fallback_font() -> str:
    if _is_registered(FALLBACK_FONT_NAME):
        return FALLBACK_FONT_NAME

    try:
        pdfmetrics.registerFont(UnicodeCIDFont(FALLBACK_FONT_NAME))
    except Exception:
        LOGGER.debug("Failed to register fallback Korean CID font.", exc_info=True)

    return FALLBACK_FONT_NAME


def _is_registered(font_name: str) -> bool:
    try:
        pdfmetrics.getFont(font_name)
    except KeyError:
        return False
    return True
