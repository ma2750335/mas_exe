# i18n_strings.py（追加內容）

from enum import Enum
from enum_setting import url
DEFAULT_LANG = "en"


def switch_lang():
    global DEFAULT_LANG
    DEFAULT_LANG = "en" if DEFAULT_LANG == "zh" else "zh"


def get_current_lang():
    return DEFAULT_LANG


class MainWindowText(Enum):
    TITLE = "MAS 交易系統"
    VERSION_PREFIX = "版本：v"


class LoginText(Enum):
    TITLE = "MAS 交易系統"
    USERNAME = "帳號："
    PASSWORD = "密碼："
    LOGIN_BUTTON = "登入"
    REGISTER_BUTTON = "註冊"
    FORGOT_PASSWORD = "忘記密碼？"
    TERMS_HTML = f'''
        <span style="font-size:13px; color:#333;">
        自動化交易前，請先確認MT5 EA設定 <a href="{url.terms_ea_setting.value}" style="color:#d2691e; text-decoration:none;">操作設定</a>
        </span>
    '''
    ERROR_TITLE = "錯誤"
    ERROR_TERMS_REQUIRED = "請先確認MT5設定才能執行策略。"
    REMEBER = "記住我"


class CheckText(Enum):
    VERSION_ALERT_TITLE = "版本更新提醒"
    VERSION_ALERT_BODY = "發現新版本 {latest}，您目前使用的是 {current}\n請至官網下載最新版！"
    LOGIN_FAILED_TITLE = "登錄失敗"
    LOGIN_FAILED_BODY = "請重新確認帳號密碼！"


class StrategyText(Enum):
    TITLE = "策略設定"
    LOGIN_ID = "登入帳號："
    PASSWORD = "登入密碼："
    SERVER = "券商伺服器："
    TERMS_HTML = f'''
        <span style="font-size:13px; color:#333;">
        我已閱讀及同意以上使用條款 <a href="{url.terms_api.value}" style="color:#d2691e; text-decoration:none;">使用條款</a> 和 
        <a href="{url.terms_disclaimer.value}" style="color:#d2691e; text-decoration:none;">免責聲明</a>
        </span>
    '''
    START = "開始執行"
    STOP = "停止"
    STATUS_IDLE = "狀態：未執行"
    FOOTER = '''<span style="font-size:13px; color:#666;">🚀 點我升級 MAS，立即創造更多專業策略：<a href="https://mas.mindaismart.com/plans" style="color:#0078D7;">前往升級</a></span>'''
    ERROR_TITLE = "錯誤"
    ERROR_INPUT_REQUIRED = "請填寫所有設定值！"
    ERROR_TERMS_REQUIRED = "請先勾選同意條款與政策才能執行策略。"
    DIALOG_TITLE = "確認交易設定"
    DIALOG_HTML_PREFIX = """
        <b>請確認交易設定：</b><br>
        <b>券商帳號：</b> {account}<br>
        <b>券商伺服器：</b> {server}<br>
    """
    DIALOG_CONFIRM = "確認執行"
    DIALOG_CANCEL = "取消"
    LOG_OPENED = "🛠 開啟策略設定畫面"
    LOG_DIALOG = "📌 顯示交易確認視窗"
    LOG_STARTED = "🚀 策略開始執行"
    LOG_STOPPED = "⏹️ 策略已停止"
    STATUS_RUNNING = "策略執行中..."
    STATUS_DONE = "❗ 策略執行完成，策略執行中，請勿關閉視窗，關閉視窗則程式交易也會停止！"
    STATUS_FAILED = "❌ 策略執行失敗！"
    LOG_SUCCESS = "✅ 策略執行中！"
    LOG_FAILED = "❌ 策略失敗：{error}"


LEVEL_LABEL = {
    "zh": {
        "free": "一般會員",
        "free_trail": "體驗會員",
        "bronze": "銅級會員",
        "silver": "銀級會員",
        "gold": "黃金會員"
    },
    "en": {
        "free": "Free Member",
        "free_trail": "Trial Member",
        "bronze": "Bronze",
        "silver": "Silver",
        "gold": "Gold"
    }
}

LEVEL_COLOR = {
    "free_trail": "#0078D7",
    "free": "#6c757d",
    "bronze": "#cd7f32",
    "silver": "#c0c0c0",
    "gold": "goldenrod"
}

LEVEL_ICON = {
    "free": "src/free.png",
    "free_trail": "src/free_trail.png",
    "bronze": "src/bronze.png",
    "silver": "src/silver.png",
    "gold": "src/gold.png"
}

i18n_map = {
    "zh": {
        MainWindowText.TITLE: "MAS 交易系統",
        MainWindowText.VERSION_PREFIX: "版本：v",
        LoginText.TITLE: "MAS 交易系統",
        LoginText.USERNAME: "帳號：",
        LoginText.PASSWORD: "密碼：",
        LoginText.LOGIN_BUTTON: "登入",
        LoginText.REGISTER_BUTTON: "註冊",
        LoginText.FORGOT_PASSWORD: "忘記密碼？",
        LoginText.TERMS_HTML: LoginText.TERMS_HTML.value,
        LoginText.ERROR_TITLE: "錯誤",
        LoginText.REMEBER :"記住我",
        LoginText.ERROR_TERMS_REQUIRED: "請先確認MT5設定才能執行策略。",
        CheckText.VERSION_ALERT_TITLE: "版本更新提醒",
        CheckText.VERSION_ALERT_BODY: "發現新版本 {latest}，您目前使用的是 {current}\n請至官網下載最新版！",
        CheckText.LOGIN_FAILED_TITLE: "登錄失敗",
        CheckText.LOGIN_FAILED_BODY: "請重新確認帳號密碼！",
        StrategyText.TITLE: "策略設定",
        StrategyText.LOGIN_ID: "MT5登入帳號：",
        StrategyText.PASSWORD: "MT5登入密碼：",
        StrategyText.SERVER: "MT5券商伺服器：",
        StrategyText.START: "開始執行",
        StrategyText.STOP: "停止",
        StrategyText.STATUS_IDLE: "狀態：未執行",
        StrategyText.ERROR_TITLE: "錯誤",
        StrategyText.ERROR_INPUT_REQUIRED: "請填寫所有設定值！",
        StrategyText.ERROR_TERMS_REQUIRED: "請先勾選同意條款與政策才能執行策略。",
        StrategyText.DIALOG_TITLE: "確認交易設定",
        StrategyText.DIALOG_CONFIRM: "確認執行",
        StrategyText.DIALOG_CANCEL: "取消",
        StrategyText.LOG_OPENED: "🛠 開啟策略設定畫面",
        StrategyText.LOG_DIALOG: "📌 顯示交易確認視窗",
        StrategyText.LOG_STARTED: "🚀 策略開始執行",
        StrategyText.LOG_STOPPED: "⏹️ 策略已停止",
        StrategyText.STATUS_RUNNING: "策略執行中...",
        StrategyText.STATUS_DONE: "❗ 策略執行完成，策略執行中，請勿關閉視窗，關閉視窗則程式交易也會停止！",
        StrategyText.STATUS_FAILED: "❌ 策略執行失敗！",
        StrategyText.LOG_SUCCESS: "✅ 策略執行中！",
        StrategyText.LOG_FAILED: "❌ 策略失敗：{error}",
        StrategyText.ERROR_SYMBOL_NOT_FOUND: "商品代碼錯誤，請輸入正確的商品代碼",
        StrategyText.TERMS_HTML: StrategyText.TERMS_HTML.value,
        StrategyText.FOOTER: StrategyText.FOOTER.value,
        StrategyText.DIALOG_HTML_PREFIX: StrategyText.DIALOG_HTML_PREFIX.value
    },
    "en": {
        MainWindowText.TITLE: "MAS Trading System",
        MainWindowText.VERSION_PREFIX: "Version: v",
        LoginText.TITLE: "MAS Trading System",
        LoginText.USERNAME: "Account:",
        LoginText.PASSWORD: "Password:",
        LoginText.LOGIN_BUTTON: "Login",
        LoginText.REGISTER_BUTTON: "Register",
        LoginText.FORGOT_PASSWORD: "Forgot Password?",
        LoginText.TERMS_HTML: f'''
        <span style="font-size:13px; color:#333;">
Before starting automated trading, please review your MT5 EA settings in the 
<a href="{url.terms_ea_setting.value}" style="color:#d2691e; text-decoration:none;">Setup Guide</a>.
</span>''',
        LoginText.REMEBER :"Remember me",
        LoginText.ERROR_TITLE: "Error",
        LoginText.ERROR_TERMS_REQUIRED: "Please confirm your MT5 settings before running the strategy.",
        CheckText.VERSION_ALERT_TITLE: "Update Notice",
        CheckText.VERSION_ALERT_BODY: "New version {latest} found. You are using {current}.\nPlease visit the official site to download the latest version!",
        CheckText.LOGIN_FAILED_TITLE: "Login Failed",
        CheckText.LOGIN_FAILED_BODY: "Please check your username or password again!",
        StrategyText.TITLE: "Strategy Settings",
        StrategyText.LOGIN_ID: "MT5 Login Account:",
        StrategyText.PASSWORD: "MT5 Login Password:",
        StrategyText.SERVER: "MT5 Broker Server:",
        StrategyText.START: "Start",
        StrategyText.STOP: "Stop",
        StrategyText.STATUS_IDLE: "Status: Idle",
        StrategyText.ERROR_TITLE: "Error",
        StrategyText.ERROR_INPUT_REQUIRED: "Please fill in all required fields!",
        StrategyText.ERROR_TERMS_REQUIRED: "You must agree to the terms and policies before executing.",
        StrategyText.DIALOG_TITLE: "Confirm Strategy Execution",
        StrategyText.DIALOG_CONFIRM: "Confirm",
        StrategyText.DIALOG_CANCEL: "Cancel",
        StrategyText.LOG_OPENED: "🛠 Opened Strategy Settings",
        StrategyText.LOG_DIALOG: "📌 Showing strategy confirmation dialog",
        StrategyText.LOG_STARTED: "🚀 Strategy execution started",
        StrategyText.LOG_STOPPED: "⏹️ Strategy stopped",
        StrategyText.STATUS_RUNNING: "Strategy running...",
        StrategyText.STATUS_DONE: "❗ Strategy finished. Do not close the window while running!",
        StrategyText.STATUS_FAILED: "❌ Strategy failed!",
        StrategyText.LOG_SUCCESS: "✅ Strategy is running!",
        StrategyText.LOG_FAILED: "❌ Strategy failed: {error}",
        StrategyText.ERROR_SYMBOL_NOT_FOUND: "Symbol not found. Please enter correct symbol",
        StrategyText.TERMS_HTML: f'''
        <span style="font-size:13px; color:#333;">
        I have read and agree to the <a href="{url.terms_api.value}" style="color:#d2691e; text-decoration:none;">Terms of Use</a> and 
        <a href="{url.terms_disclaimer.value}" style="color:#d2691e; text-decoration:none;">Disclaimer</a>
        </span>
        ''',
        StrategyText.FOOTER: '''<span style="font-size:13px; color:#666;">🚀 Upgrade to MAS for more professional strategies: <a href="https://mas.mindaismart.com/plans" style="color:#0078D7;">Upgrade Now</a></span>''',
        StrategyText.DIALOG_HTML_PREFIX: '''
        <b>Please confirm strategy settings:</b><br>
        <b>Account:</b> {account}<br>
        <b>Server:</b> {server}<br>
        '''
    }
}


def get_text(key: Enum, lang: str = None) -> str:
    if lang is None:
        lang = get_current_lang()
    return i18n_map.get(lang, {}).get(key, key.value)


def get_level_label(level: str) -> str:
    lang = get_current_lang()
    return LEVEL_LABEL.get(lang, {}).get(level, level)


def get_level_color(level: str) -> str:
    return LEVEL_COLOR.get(level, "#000")


def get_level_icon(level: str) -> str:
    return LEVEL_ICON.get(level, "")
