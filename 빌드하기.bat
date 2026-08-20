@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo ===== 홈페이지 빌드 시작 =====
echo.
where python >/dev/null 2>&1
if %errorlevel%==0 (python build.py) else (py build.py)
echo.
if exist dist (
  echo ===== 완료 =====
  echo dist 폴더가 만들어졌습니다.
  echo 이 폴더를 Netlify ^> 프로젝트 ^> Deploys 탭에 드래그하세요.
  echo.
  echo 창을 닫지 말고 아래 안내를 읽으세요.
) else (
  echo ===== 실패 =====
  echo dist 폴더가 안 생겼습니다. 위 빨간 글씨를 캡처해서 보내주세요.
)
echo.
pause
