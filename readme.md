
# MAS EXE 打包與執行說明

本專案為桌面版 Python GUI 程式，使用 `PySide6` 建構介面，並透過 `PyInstaller` 打包為 Windows 可執行檔。

---

## 1. 專案目錄

建議專案目錄如下：

```
C:\workplace\mas_exe
├─ main.py
├─ main_window.py
├─ strategy_settings.py
├─ strategy.py
├─ bk_test.py
├─ logo.ico
├─ logo.png
├─ static\
│  └─ version.txt
├─ mas\
└─ dist\
```

## 2. 執行環境

### Python 版本

請先確認目前使用的 Python 版本：

```bash
python --version
```

### 必要套件

本專案至少需安裝以下套件：

```bash
pip install PySide6 pandas python-dateutil six pyinstaller
```

若專案還有其他套件依賴，請依實際需求補充安裝。

## 3. 安裝與確認 PyInstaller

若系統無法直接辨識 `pyinstaller` 指令，請改用模組方式執行：

```bash
python -m PyInstaller --version
```

若尚未安裝 PyInstaller，請執行：

```bash
python -m pip install pyinstaller
```

安裝完成後再次確認：

```bash
python -m PyInstaller --version
```

例如：

```
6.19.0
```

## 4. 執行程式

在專案根目錄下執行：

```bash
python .\main.py
```

若可正常開啟視窗，表示基本執行環境已就緒。

## 5. 打包指令

目前可正常使用的打包指令如下：

```bash
py -m PyInstaller --name "strategy_bf6bbd37-a354-4689-91ad-e4c060ef504b" --noconfirm --clean --onefile --log-level=WARN --version-file="C:\workplace\mas_exe\static\version.txt" "C:\workplace\mas_exe\main.py" --distpath "C:\workplace\mas_exe\dist" -w -i "C:\workplace\mas_exe\logo.ico" --add-binary "C:\workplace\mas_exe\logo.png;." --add-binary "C:\workplace\mas_exe\logo.ico;." --exclude-module scipy.special._cdflib --exclude-module pysqlite2 --exclude-module MySQLdb --exclude-module psycopg2
```

## 6. 打包參數說明

### 基本參數

- `--name`：指定輸出的 exe 檔名
- `--noconfirm`：不詢問直接覆蓋舊的 build 結果
- `--clean`：清除暫存 build 檔案
- `--onefile`：打包成單一 exe
- `--log-level=WARN`：僅顯示警告等級以上的訊息
- `--version-file`：指定 Windows 可執行檔版本資訊檔
- `--distpath`：指定輸出資料夾
- `-w`：不開啟 console 視窗，適合 GUI 程式
- `-i`：指定 exe 的 icon

### 資源檔打包

- `--add-binary "C:\workplace\mas_exe\logo.png;."`
- `--add-binary "C:\workplace\mas_exe\logo.ico;."`

將圖片與 icon 一起包入執行檔中。

### 排除模組

- `--exclude-module scipy.special._cdflib`
- `--exclude-module pysqlite2`
- `--exclude-module MySQLdb`
- `--exclude-module psycopg2`

排除不需要的模組，減少打包體積與不必要的分析干擾。

## 7. 輸出位置

打包完成後，exe 預設輸出在：

```
C:\workplace\mas_exe\dist
```

例如：

```
C:\workplace\mas_exe\dist\strategy_bf6bbd37-a354-4689-91ad-e4c060ef504b.exe
```

## 8. version.txt 說明

若使用 `--version-file`，需先建立：

```
C:\workplace\mas_exe\static\version.txt
```

範例如下：

```python
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '040904B0',
          [
            StringStruct('CompanyName', 'MAS'),
            StringStruct('FileDescription', 'MAS Strategy EXE'),
            StringStruct('FileVersion', '1.0.0.0'),
            StringStruct('InternalName', 'strategy'),
            StringStruct('OriginalFilename', 'strategy.exe'),
            StringStruct('ProductName', 'MAS Strategy'),
            StringStruct('ProductVersion', '1.0.0.0')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
```

可依實際產品名稱、版本號與公司名稱進行調整。

## 9. 常見錯誤排查

### 錯誤 1：找不到 pyinstaller

**錯誤訊息範例：**

```
pyinstaller : 無法辨識 'pyinstaller'
```

**原因**

- PyInstaller 未安裝
- 或目前環境的 PATH 未包含對應 Scripts 路徑

**解法**

請改用：

```bash
python -m PyInstaller --version
```

若尚未安裝：

```bash
python -m pip install pyinstaller
```

### 錯誤 2：No module named PyInstaller

**原因**

目前使用的 Python 環境未安裝 PyInstaller。

**解法**

```bash
python -m pip install pyinstaller
```

### 錯誤 3：找不到 logo.ico、logo.png 或 static\version.txt

**原因**

- 檔案不存在
- 路徑錯誤
- 目錄名稱不一致

**解法**

```bash
dir C:\workplace\mas_exe\logo.*
dir C:\workplace\mas_exe\static\version.txt
```

若檔案不存在，請：

- 建立 `static\version.txt`
- 放入 `logo.ico`
- 放入 `logo.png`

或先移除相關參數後再打包。

### 錯誤 4：打包成功但 exe 執行失敗

**可能原因**

- 缺少模組
- 缺少資源檔
- GUI 模式下沒有 console 視窗，無法直接看到錯誤訊息

**建議作法**

先移除 `-w`，重新打包為可顯示 console 的版本，方便觀察實際錯誤：

```bash
py -m PyInstaller --name "strategy_test" --noconfirm --clean --onefile "C:\workplace\mas_exe\main.py" --distpath "C:\workplace\mas_exe\dist"
```

之後執行 exe，觀察錯誤內容，再決定是否補上：

- `--hidden-import`
- `--add-data`
- `--add-binary`

## 10. 建議打包流程

建議依以下順序操作：

1. **第一步：確認程式能正常執行**

   ```bash
   python .\main.py
   ```

2. **第二步：確認 PyInstaller 已安裝**

   ```bash
   python -m PyInstaller --version
   ```

3. **第三步：確認必要資源檔存在**

   ```bash
   dir C:\workplace\mas_exe\logo.*
   dir C:\workplace\mas_exe\static\version.txt
   ```

4. **第四步：執行打包**

   ```bash
   py -m PyInstaller --name "strategy_bf6bbd37-a354-4689-91ad-e4c060ef504b" --noconfirm --clean --onefile --log-level=WARN --version-file="C:\workplace\mas_exe\static\version.txt" "C:\workplace\mas_exe\main.py" --distpath "C:\workplace\mas_exe\dist" -w -i "C:\workplace\mas_exe\logo.ico" --add-binary "C:\workplace\mas_exe\logo.png;." --add-binary "C:\workplace\mas_exe\logo.ico;." --exclude-module scipy.special._cdflib --exclude-module pysqlite2 --exclude-module MySQLdb --exclude-module psycopg2
   ```

5. **第五步：檢查輸出檔案**

   ```bash
   dir C:\workplace\mas_exe\dist
   ```

## 11. 最小化測試建議

若執行或打包有問題，可先建立 `test_import.py` 進行最小測試：

```python
print("start")

import pandas as pd
print("pandas ok", pd.__version__)

from PySide6.QtWidgets import QApplication
print("PySide6 ok")

print("all ok")
```

執行：

```bash
python .\test_import.py
```

若這支測試檔都無法執行，請先檢查 Python 環境與套件安裝狀況。

## 12. 備註

- 若未來需支援更多資源檔，可額外加入 `--add-data` 或 `--add-binary`
- 若 exe 執行後提示缺模組，可再補 `--hidden-import`
- 若 GUI 打包後沒有反應，建議先移除 `-w`，保留 console 觀察錯誤

範例：

```bash
py -m PyInstaller --name "strategy_test" --noconfirm --clean --onefile "C:\workplace\mas_exe\main.py" --distpath "C:\workplace\mas_exe\dist"
```

## 13. 簡要結論

本專案建議打包流程如下：

- 確認 Python 環境正常
- 確認 `main.py` 可正常執行
- 確認 `python -m PyInstaller --version` 正常
- 準備 `logo.ico`、`logo.png`、`static\version.txt`
- 執行正式打包指令
- 於 `dist` 目錄取得 exe
- 若 exe 執行異常，先移除 `-w` 重新打包以查看錯誤訊息