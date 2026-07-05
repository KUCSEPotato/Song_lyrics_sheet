from __future__ import annotations

import sys
import traceback
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from worksheet_generator import create_worksheet_pdf

DEFAULT_TITLE = "가사 따라쓰기 학습지"
DEFAULT_OUTPUT_FILENAME = "lyrics_worksheet.pdf"
READY_MESSAGE = "가사를 입력한 뒤 PDF 저장하기를 눌러주세요."


class LyricsWorksheetWindow(QMainWindow):
    """Main window for creating lyrics handwriting worksheet PDFs."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("가사 따라쓰기 학습지 만들기")
        self.setMinimumSize(720, 620)

        self.title_input = QLineEdit(DEFAULT_TITLE)
        self.lyrics_input = QPlainTextEdit()
        self.lyrics_input.setPlaceholderText(
            "가사를 여기에 붙여넣으세요.\n입력한 줄바꿈은 학습지에도 반영됩니다."
        )

        self.columns_input = QSpinBox()
        self.columns_input.setRange(6, 20)
        self.columns_input.setValue(12)

        self.practice_rows_input = QSpinBox()
        self.practice_rows_input.setRange(1, 3)
        self.practice_rows_input.setValue(1)

        self.save_button = QPushButton("PDF 저장하기")
        self.save_button.clicked.connect(self.save_pdf)

        self.status_label = QLabel(READY_MESSAGE)
        self.status_label.setWordWrap(True)

        self._build_layout()

    def save_pdf(self) -> None:
        """Validate user input, ask for a save path, and create the PDF."""
        lyrics = self.lyrics_input.toPlainText()
        if not lyrics.strip():
            QMessageBox.warning(self, "입력 확인", "가사를 입력해 주세요.")
            self.status_label.setText("가사를 입력해 주세요.")
            return

        selected_path, _ = QFileDialog.getSaveFileName(
            self,
            "PDF 저장",
            str(Path.cwd() / DEFAULT_OUTPUT_FILENAME),
            "PDF 파일 (*.pdf)",
        )
        if not selected_path:
            self.status_label.setText("저장이 취소되었습니다.")
            return

        output_path = _ensure_pdf_suffix(Path(selected_path))
        self.status_label.setText("PDF를 생성하고 있습니다...")
        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:
            created_path = create_worksheet_pdf(
                title=self.title_input.text(),
                lyrics=lyrics,
                output_path=output_path,
                columns=self.columns_input.value(),
                practice_rows=self.practice_rows_input.value(),
            )
        except ValueError as exc:
            traceback.print_exc()
            QMessageBox.warning(self, "입력 확인", str(exc))
            self.status_label.setText("입력 내용을 확인해 주세요.")
        except Exception as exc:
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "PDF 생성 오류",
                f"PDF를 생성하는 중 문제가 발생했습니다.\n\n{exc}",
            )
            self.status_label.setText("PDF 생성에 실패했습니다.")
        else:
            QMessageBox.information(
                self,
                "저장 완료",
                f"PDF가 저장되었습니다.\n\n{created_path}",
            )
            self.status_label.setText("PDF가 저장되었습니다.")
        finally:
            QApplication.restoreOverrideCursor()

    def _build_layout(self) -> None:
        form_layout = QFormLayout()
        form_layout.addRow("학습지 제목", self.title_input)

        options_layout = QHBoxLayout()
        options_layout.addWidget(QLabel("한 줄 칸 수"))
        options_layout.addWidget(self.columns_input)
        options_layout.addSpacing(16)
        options_layout.addWidget(QLabel("연습 행 수"))
        options_layout.addWidget(self.practice_rows_input)
        options_layout.addStretch(1)

        self.lyrics_input.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(QLabel("가사 입력"))
        layout.addWidget(self.lyrics_input, 1)
        layout.addLayout(options_layout)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def _ensure_pdf_suffix(path: Path) -> Path:
    if path.suffix.lower() == ".pdf":
        return path
    if not path.suffix:
        return path.with_suffix(".pdf")
    return path.with_suffix(path.suffix + ".pdf")


def main() -> None:
    """Start the PySide6 application."""
    app = QApplication(sys.argv)
    window = LyricsWorksheetWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
