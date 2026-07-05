from __future__ import annotations

from pathlib import Path

import pytest

from worksheet_generator import create_worksheet_pdf


def test_create_worksheet_pdf_creates_pdf(tmp_path: Path) -> None:
    output_path = tmp_path / "worksheet.pdf"

    result = create_worksheet_pdf(
        title="테스트 학습지",
        lyrics="보고 싶다\n이렇게 말하니까",
        output_path=output_path,
        columns=8,
        practice_rows=1,
    )

    assert result == output_path
    assert result.exists()
    assert result.is_file()
    assert result.stat().st_size > 0
    assert result.read_bytes().startswith(b"%PDF")


def test_create_worksheet_pdf_splits_long_lines(tmp_path: Path) -> None:
    result = create_worksheet_pdf(
        title="긴 줄 테스트",
        lyrics="가나다라마바사아자차카타파하",
        output_path=tmp_path / "long-line.pdf",
        columns=6,
        practice_rows=2,
    )

    assert result.exists()
    assert result.stat().st_size > 0


def test_create_worksheet_pdf_handles_blank_lines(tmp_path: Path) -> None:
    result = create_worksheet_pdf(
        title="빈 줄 테스트",
        lyrics="첫 줄\n\n셋째 줄",
        output_path=tmp_path / "blank-lines.pdf",
        columns=8,
        practice_rows=1,
    )

    assert result.exists()
    assert result.stat().st_size > 0


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"columns": 5}, "한 줄 칸 수"),
        ({"columns": 21}, "한 줄 칸 수"),
        ({"practice_rows": 0}, "연습 행 수"),
        ({"practice_rows": 4}, "연습 행 수"),
        ({"lyrics": " \n\t "}, "가사를 입력"),
    ],
)
def test_create_worksheet_pdf_rejects_invalid_input(
    tmp_path: Path,
    kwargs: dict[str, object],
    message: str,
) -> None:
    options = {
        "title": "입력 범위 테스트",
        "lyrics": "정상 가사",
        "output_path": tmp_path / "invalid.pdf",
        "columns": 12,
        "practice_rows": 1,
    }
    options.update(kwargs)

    with pytest.raises(ValueError, match=message):
        create_worksheet_pdf(**options)
