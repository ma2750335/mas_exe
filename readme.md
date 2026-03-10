# MAS EXE

此專案是使用 `PySide6` 開發的 Windows GUI 應用程式。  
功能包含登入、策略設定、策略執行，並可透過 `PyInstaller` 打包為單一 `.exe`。

## 1. 重要檔案

- GUI 入口：`main.py`
- 登入流程：`login.py`、`auth.py`
- 主視窗：`main_window.py`
- 策略設定與執行：`strategy_settings.py`、`strategy.py`、`bk_test.py`
- 打包腳本：`build_pyinstaller.bat`
- EXE 版本資訊：`static/version.txt`

## 2. 環境需求

- 作業系統：Windows
- Python：建議 `3.10+`
- 可使用 `pip`

## 3. 安裝相依套件

目前專案根目錄沒有統一的 `requirements.txt`，可先安裝目前程式碼用到的套件：

```powershell
pip install PySide6 pandas requests cryptography MetaTrader5 numpy plotly quantstats sqlalchemy python-dateutil six pyinstaller
```

## 4. 本機執行

```powershell
python .\main.py
```

或

```powershell
py .\main.py
```

## 5. 打包 EXE（建議）

使用內建腳本：

- `build_pyinstaller.bat`

步驟：

1. 開啟 `build_pyinstaller.bat`
2. 只需視需求修改：
   - `set "PROJECT_ROOT=C:\workplace\mas_exe"`
3. 執行：

```powershell
.\build_pyinstaller.bat
```

輸出檔案：

- `dist\strategy_bf6bbd37-a354-4689-91ad-e4c060ef504b.exe`

## 6. 等價手動 PyInstaller 指令

```powershell
py -m PyInstaller --name "strategy_bf6bbd37-a354-4689-91ad-e4c060ef504b" --noconfirm --clean --onefile --log-level=WARN --version-file="C:\workplace\mas_exe\static\version.txt" "C:\workplace\mas_exe\main.py" --distpath "C:\workplace\mas_exe\dist" -w -i "C:\workplace\mas_exe\logo.ico" --add-binary "C:\workplace\mas_exe\logo.png;." --add-binary "C:\workplace\mas_exe\logo.ico;." --exclude-module scipy.special._cdflib --exclude-module pysqlite2 --exclude-module MySQLdb --exclude-module psycopg2
```

## 7. PyInstaller 參數說明

- `--name "strategy_bf6bbd37-a354-4689-91ad-e4c060ef504b"`：設定輸出 EXE 名稱。
- `--noconfirm`：覆蓋既有輸出時不再詢問。
- `--clean`：打包前清除暫存快取（`build` 相關）。
- `--onefile`：打包為單一 EXE 檔案。
- `--log-level=WARN`：僅顯示警告與錯誤等級日誌，減少訊息量。
- `--version-file="...\\static\\version.txt"`：寫入 Windows 檔案版本資訊（檔案內容、公司名、版本號等）。
- `"C:\\workplace\\mas_exe\\main.py"`：指定程式入口腳本。
- `--distpath "C:\\workplace\\mas_exe\\dist"`：指定最終 EXE 輸出資料夾。
- `-w`：Windows 視窗模式，不開啟主控台視窗（適合 GUI 程式）。
- `-i "C:\\workplace\\mas_exe\\logo.ico"`：設定 EXE 圖示。
- `--add-binary "C:\\workplace\\mas_exe\\logo.png;."`：把 `logo.png` 一併打包到執行目錄。
- `--add-binary "C:\\workplace\\mas_exe\\logo.ico;."`：把 `logo.ico` 一併打包到執行目錄。
- `--exclude-module scipy.special._cdflib`：排除未使用模組以減少體積/避免衝突。
- `--exclude-module pysqlite2`：同上，排除未使用模組。
- `--exclude-module MySQLdb`：同上，排除未使用模組。
- `--exclude-module psycopg2`：同上，排除未使用模組。

## 8. 常見問題

### 8.1 錯誤：`Script file '\main.py' does not exist`

通常是 `PROJECT_ROOT` 在 `.bat` 未正確設定。請確認：

- `PROJECT_ROOT` 路徑正確
- `.bat` 未被錯誤編碼破壞（建議維持英文註解）

### 8.2 錯誤：找不到 `pyinstaller` 指令

先測試：

```powershell
py -m PyInstaller --version
```

若仍失敗：

```powershell
pip install pyinstaller
```

### 8.3 打包後 icon 或圖片遺失

目前已使用：

- `--add-binary "logo.png;."`
- `--add-binary "logo.ico;."`

若仍有問題，請確認檔案在專案根目錄，且程式透過 `get_resource_path(...)` 載入資源。

## 9. 專案結構（簡化）

```text
mas_exe/
|-- main.py
|-- main_window.py
|-- login.py
|-- strategy_settings.py
|-- strategy.py
|-- bk_test.py
|-- auth.py
|-- check.py
|-- i18n_strings.py
|-- enum_setting.py
|-- build_pyinstaller.bat
|-- static/
|   |-- version.txt
|-- logo.ico
|-- logo.png
`-- mas/
```

## 10. 備註

- `login.py` 的記住帳密功能使用 `QSettings` 儲存，請依安全需求評估是否保留。
- 專案另含 `setup.py` 與 `mas/` 套件結構，後續可視需求拆分為套件發布流程。
