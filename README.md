# 가사 따라쓰기 학습지 생성기

붙여넣은 가사를 한 글자당 한 칸으로 나누어 A4 PDF 따라쓰기 학습지로 만드는 데스크톱 프로그램입니다. Windows 사용자는 GitHub Actions에서 빌드된 `LyricsWorksheet.exe`를 내려받아 Python 설치 없이 실행할 수 있습니다.

## 주요 기능

- PySide6 기반 GUI
- 학습지 제목, 가사, 한 줄 칸 수, 연습 행 수 설정
- A4 세로 PDF 생성
- 사진 예시처럼 페이지 중앙에 이어진 큰 격자 형태로 출력
- 가사 줄바꿈 유지
- 긴 가사는 지정한 칸 수 기준으로 자동 분할
- 띄어쓰기 칸은 회색 배경으로 표시
- 운영체제에 설치된 한글 폰트 자동 탐색

## 프로젝트 구조

```text
lyrics-worksheet/
├── app.py
├── worksheet_generator.py
├── font_manager.py
├── LyricsWorksheet.spec
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── AGENTS.md
├── tests/
│   ├── test_worksheet_generator.py
│   └── test_font_manager.py
└── .github/
    └── workflows/
        └── build-windows.yml
```

## macOS 개발 환경 설정

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python app.py
```

macOS 앱 번들 생성은 필수 범위가 아닙니다. macOS에서는 Python으로 GUI를 실행하고 PDF 생성 기능을 테스트합니다.

## 프로그램 실행 방법

개발 환경에서 실행할 때:

```bash
source .venv/bin/activate
python app.py
```

## 테스트 방법

```bash
python -m pytest
python -m compileall .
```

## Windows에서 직접 EXE 빌드

Windows PowerShell에서 다음 명령을 실행합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest
pyinstaller --noconfirm --clean LyricsWorksheet.spec
```

빌드 결과는 다음 위치에 생성됩니다.

```text
dist/LyricsWorksheet.exe
```

기본 PyInstaller 명령은 다음과 같습니다.

```powershell
pyinstaller `
  --noconfirm `
  --clean `
  --onefile `
  --windowed `
  --name LyricsWorksheet `
  app.py
```

이 프로젝트는 재현 가능한 빌드를 위해 `LyricsWorksheet.spec`를 함께 제공합니다.

## GitHub Actions로 EXE 받기

1. GitHub 저장소의 `Actions` 탭을 연다.
2. `Build Windows EXE` 워크플로를 선택한다.
3. `Run workflow`로 수동 실행하거나 `main` 브랜치에 push한다.
4. 실행이 끝난 워크플로 페이지의 `Artifacts` 영역에서 `LyricsWorksheet-Windows`를 내려받는다.
5. 압축을 풀어 `LyricsWorksheet.exe`를 실행한다.

## Windows 사용법

```text
1. LyricsWorksheet.exe를 실행한다.
2. 제목과 가사를 입력한다.
3. 칸 수와 연습 행 수를 선택한다.
4. PDF 저장하기를 누른다.
5. 저장 위치를 선택한다.
```

## 알려진 제한 사항

- 폰트 파일은 저장소에 포함하지 않습니다. 실행 환경에 설치된 한글 폰트를 우선 사용하고, 실패하면 ReportLab CID 폰트를 사용합니다.
- GUI 동작은 수동 확인을 기본으로 하며, 자동 테스트는 PDF 생성과 폰트 등록 로직 중심입니다.
- PDF의 글자 단위 처리는 Python 문자열의 문자 단위를 따릅니다. 완성형 한글 음절은 한 칸으로 처리하지만, 복잡한 결합 문자나 이모지는 사용자 환경에 따라 표시가 다를 수 있습니다.
