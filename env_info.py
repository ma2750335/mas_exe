# 部署設定（取代 .env，避免 PyInstaller 打包後相對路徑問題）
#
# 為什麼是 .py 不是 .env：
#   - .env 是資料檔，bundler 預設不會打包；改用 .py 是 Python 原生 import
#     系統處理，零路徑問題。
#   - 直接用 Python type（bool / int），call site 不用做字串 parse。
#
# 換環境作法：
#   - 改 ENV_VERSION（0=dev / 1=test / 2=pd）即可切換所有 mas API base URL
#   - 改 IS_GENAI 開關健康度功能
#   - 改完重新 build EXE

# 裝置 UUID（後端用來識別此 EXE 安裝實例 / 策略歸屬）
UUID = "test123"

# 是否啟用 GENAI 健康度功能（badge / alert / 監控 timer）
IS_GENAI = False

# 環境版本：0 = dev (localhost) / 1 = test / 2 = pd
ENV_VERSION = 2
