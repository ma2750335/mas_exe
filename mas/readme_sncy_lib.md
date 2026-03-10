# 專案同步與調整步驟說明

## 📦 exe 端

### 1️⃣ 同步 mas_lib
- **刪除**：
  - 刪除目錄：`mas_platform/server/mas_lib/exe/mas`
- **複製**：
  - 將 `mas_lib` 中 `mas` 資料夾的所有檔案 **複製到** `mas_platform/server/mas_lib/exe`

---

### 2️⃣ 調整 exe_history
- **路徑**：`mas_platform/server/mas_lib/exe/mas/history`
- **操作**：
  - 刪除 `history_data_db.py`
  - 修改 `history_data_manager.py` 的 import：
    ```python
    from mas.history.history_data_mt5 import HistoryData
    ```

---

### 3️⃣ 調整 exe_clinet_post
- **路徑**：`mas_platform/server/mas_lib/exe/mas/clinet/`
- **操作**：
  - 刪除：
    - `client_post_bk.py`
    - `client_post_real.py`
  - 修改 `client_post.py` 的 import：
    ```python
    from mas.clinet.client_post_real_exe import ClientPostReal
    ```

---

## 🌐 server 端

### 1️⃣ 同步 mas_lib
- **刪除**：
  - 刪除目錄：`mas_platform/server/mas_lib/mas`
- **複製**：
  - 將 `mas_lib` 中 `mas` 資料夾的所有檔案 **複製到** `mas_platform/server/mas_lib`

---

### 2️⃣ 調整 server_history
- **路徑**：`mas_platform/server/mas_lib/mas/enum/env_setting.py`
- **操作**：
  - 將 `platform` 變數設為：
    ```python
    platform = True
    ```
- **路徑**：`mas_platform/server/mas_lib/mas/history`
- **操作**：
  - 刪除 `history_data_mt5.py`
  - 修改 `history_data_manager.py` 的 import：
    ```python
    from mas.history.history_data_db import HistoryData
    ```

---

### 3️⃣ 調整 server_clinet_post
- **路徑**：`mas_platform/server/mas_lib/mas/clinet/`
- **操作**：
  - 刪除：
    - `client_post_real.py`
    - `client_post_real_exe.py`
  - 修改 `client_post.py` 的 import：
    ```python
    from mas.clinet.client_post_real_bk import ClientPostReal
    ```

---

## ⚠️ 注意事項
- **請務必確認備份**：在執行刪除與複製前，請將原始檔案備份以防意外損壞。
- **跨端同步一致性**：exe 端與 server 端的 `mas_lib` 更新後，務必確認版本一致性。
- **測試驗證**：完成調整後，請執行基礎測試，確保修改後模組能正常運作。

pyinstaller --onefile --noconfirm --noupx --log-level=WARN --name MAS --exclude-module tkinter server.py