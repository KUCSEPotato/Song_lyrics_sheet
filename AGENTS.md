# AGENTS.md

## 프로젝트 목적

이 프로젝트는 사용자가 붙여넣은 가사를 한 글자당 한 칸으로 나누어 A4 PDF 따라쓰기 학습지로 만드는 Python 데스크톱 앱입니다. Windows 최종 사용자는 `LyricsWorksheet.exe`를 더블클릭해 사용할 수 있어야 합니다.

## 개발 규칙

- Python 3.12를 기준으로 개발합니다.
- GUI는 `app.py`의 PySide6 코드에 둡니다.
- PDF 생성 로직은 `worksheet_generator.py`에 둡니다.
- 폰트 탐색 및 등록 로직은 `font_manager.py`에 둡니다.
- GUI와 PDF 생성 로직은 분리합니다.
- 모든 공개 함수에는 type hint를 작성합니다.
- 핵심 공개 함수에는 docstring을 작성합니다.
- 사용자에게 표시되는 문구는 한국어로 작성합니다.
- 코드 주석은 필요한 경우에만 영어로 작성합니다.
- 폰트 파일은 저장소에 커밋하지 않습니다.

## 테스트와 검증

변경 후 반드시 다음 명령을 실행합니다.

```bash
python -m pytest
python -m compileall .
```

macOS에서는 Python으로 GUI 실행과 PDF 생성 기능을 확인합니다.

```bash
python app.py
```

Windows에서는 PyInstaller로 EXE 빌드를 확인합니다.

```powershell
pyinstaller --noconfirm --clean LyricsWorksheet.spec
```

생성 파일은 `dist/LyricsWorksheet.exe`여야 합니다.
