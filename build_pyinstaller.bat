@echo off
setlocal

REM Change only this path if needed.
set "PROJECT_ROOT=C:\workplace\mas_exe"

REM Optional: output exe name.
set "APP_NAME=strategy_bf6bbd37-a354-4689-91ad-e4c060ef504b"

set "MAIN_PY=%PROJECT_ROOT%\main.py"
set "VERSION_FILE=%PROJECT_ROOT%\static\version.txt"
set "DIST_PATH=%PROJECT_ROOT%\dist"
set "ICON_FILE=%PROJECT_ROOT%\logo.ico"
set "LOGO_PNG=%PROJECT_ROOT%\logo.png"
set "LOGO_ICO=%PROJECT_ROOT%\logo.ico"

echo [INFO] Building "%APP_NAME%" from "%MAIN_PY%"

py -m PyInstaller ^
  --name "%APP_NAME%" ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --log-level=WARN ^
  --version-file="%VERSION_FILE%" ^
  "%MAIN_PY%" ^
  --distpath "%DIST_PATH%" ^
  -w ^
  -i "%ICON_FILE%" ^
  --add-binary "%LOGO_PNG%;." ^
  --add-binary "%LOGO_ICO%;." ^
  --exclude-module scipy.special._cdflib ^
  --exclude-module pysqlite2 ^
  --exclude-module MySQLdb ^
  --exclude-module psycopg2

if errorlevel 1 (
  echo [ERROR] PyInstaller build failed.
  exit /b 1
)

echo [INFO] Build completed successfully.
exit /b 0
