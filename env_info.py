# ?函蔡閮剖?嚗?隞?.env嚗??PyInstaller ??敺撠楝敺?憿?
#
# ?箔?暻潭 .py 銝 .env嚗?
#   - .env ?航???嚗undler ?身銝???嚗??.py ??Python ?? import
#     蝟餌絞??嚗頝臬?????
#   - ?湔??Python type嚗ool / int嚗?call site 銝??銝?parse??
#
# ?憓?瘜?
#   - ??ENV_VERSION嚗?=dev / 1=test / 2=pd嚗?臬?????mas API base URL
#   - ??IS_GENAI ???亙熒摨血???
#   - ?孵?? build EXE

# 鋆蔭 UUID嚗?蝡舐靘??交迨 EXE 摰?撖虫? / 蝑甇詨惇嚗?
UUID = "5609ea94-4fc0-4e7f-9fe3-0bdedebcec27"
PRODUCT = "book25k" 

# 蝑?亙熒摨?API 隤? token嚗?4 摮? hex嚗uild ?敺垢 /my-strategies/:id/build-status 撋嚗?
HEALTH_TOKEN = "50338d2dcab9de6b1d62c5bd66d3e2793522ee04602f738d08442c342386ff9b"

# ?臬? GENAI ?亙熒摨血??踝?badge / alert / ?? timer嚗?
IS_GENIE = False

# ?啣??嚗? = dev (localhost) / 1 = test / 2 = pd
ENV_VERSION = 2

# GENAI EXE ??嚗?蝡舐靘??交迨 EXE ???穿??餃? payload 銝?
GENAI_EXE_VERSION = "0.0.1"

# ?身隤?嚗n / zh / cn嚗??桀??撣豢嚗??芣蝺 i18n嚗????芯?雿輻嚗?
DEFAULT_LANG = "en"

# 每子策略風險上限（mas_book Gold4Leg 讀取）。黃金最小手數 0.01 的風險在 $10k 上已達 1.75%+，
# 設太低會導致每個訊號都被小帳戶保護跳過、永遠不下單。
SUB_RISK = 0.03

# 黃金子策略的正常下單風險（策略驗證值）。SUB_RISK 只在最小手裝不下時當放寬上限，
# 兩者分開才不會讓大帳戶被一路放大到 SUB_RISK（2026-08-14 修）。
BASE_SUB_RISK = 0.01

# 風險檔位：conservative / balanced / aggressive（mas_book RISK_MAP 名目總風險 2%/5%/10%）。
RISK_PROFILE = "balanced"
