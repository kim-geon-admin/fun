# CDDEX

CDDEX는 실제 키보드 입력을 받지만, 모든 활동을 명확히 `SIMULATED`/`FICTIONAL`로 표시하는 Python 터미널 연출 도구입니다. 파일을 읽거나, 명령을 실행하거나, 네트워크·외부 서비스에 접근하지 않습니다.

## 실행

```powershell
py -m pip install -e .
cddex
```

Windows 소스 폴더에서는 다음으로도 실행할 수 있습니다.

```powershell
.\cddex.bat
```

## 명령

- `/init` — 색상별 가상 스캔·스킬·추론·데이터 읽기 연출을 표시합니다. Ctrl+C로 연출만 중단합니다.
- `/help`, `/status`, `/theme`, `/clear`
- `/exit`, `/quit`

`--no-color` 또는 `NO_COLOR=1`을 사용하면 ANSI 색상을 끌 수 있습니다.

## 개발 확인

```powershell
$env:PYTHONPATH = 'src'
py -m unittest discover -s tests -v
```

## 안전성

CDDEX의 도구, 데이터, 진행 상태, 결과는 모두 가상 연출입니다. 실제 시스템·데이터·서비스에 대한 작업을 수행하지 않습니다.

