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
    TITLE = "MasQuant 交易系統"
    VERSION_PREFIX = "版本：v"
    PROCESS_LOG_LABEL = "流程 Log"
    BACKTEST_LOG_LABEL = "交易訊號 Log"
    BACKTEST_LOG_PLACEHOLDER = "這裡顯示進出場與市價訊號..."


class LoginText(Enum):
    TITLE = "MasQuant 交易系統"
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
    HEALTH_ALERT_TITLE = "策略健康度提醒"
    HEALTH_ALERT_BODY = "health_alert_body"
    HEALTH_LEVEL_LOW = "低"
    HEALTH_LEVEL_MEDIUM = "中"
    HEALTH_LEVEL_HIGH = "高"
    STRATEGY_HEALTH_LABEL = "策略健康度："
    HEALTH_INFO_TITLE = "策略健康度說明"
    HEALTH_INFO_BODY = "health_info_body"
    UPGRADE_REQUIRED_TITLE = "需要升級會員"
    UPGRADE_REQUIRED_BODY = "upgrade_required_body"
    SUBSCRIPTION_EXPIRED_TITLE = "訂閱已過期"
    SUBSCRIPTION_EXPIRED_BODY = "subscription_expired_body"


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
    FOOTER = '''<span style="font-size:13px; color:#666;">🚀 點我升級 MasQuant，立即創造更多專業策略：<a href="https://mas.mindaismart.com/plans" style="color:#0078D7;">前往升級</a></span>'''
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
    DIALOG_RISK_HTML = "risk_notice"
    LOG_OPENED = "🛠 開啟策略設定畫面"
    LOG_DIALOG = "📌 顯示交易確認視窗"
    LOG_STARTED = "🚀 策略開始執行"
    LOG_STOPPED = "⏹️ 策略已停止"
    STATUS_RUNNING = "策略執行中..."
    STATUS_DONE = "❗ 策略執行完成，策略執行中，請勿關閉視窗，關閉視窗則程式交易也會停止！"
    STATUS_FAILED = "❌ 策略執行失敗！"
    LOG_SUCCESS = "✅ 策略執行中！"
    LOG_FAILED = "❌ 策略失敗：{error}"
    ERROR_SYMBOL_NOT_FOUND = "商品代碼錯誤，請輸入正確的商品代碼"
    ERROR_TRADE_EXPERT_DISABLED = "MT5 尚未開啟「允許算法交易」，請先至 MT5 開啟設定後再執行策略。"
    ERROR_TRADE_EXPERT_DISABLED_HTML = "trade_expert_disabled_html"
    CAPITAL = "本金："
    VOLUME = "手數："


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
        MainWindowText.TITLE: "MasQuant 交易系統",
        MainWindowText.VERSION_PREFIX: "版本：v",
        MainWindowText.PROCESS_LOG_LABEL: "📝 流程 Log",
        MainWindowText.BACKTEST_LOG_LABEL: "📊 交易訊號 Log",
        MainWindowText.BACKTEST_LOG_PLACEHOLDER: "這裡顯示進出場與市價訊號...",
        LoginText.TITLE: "MasQuant 交易系統",
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
        CheckText.HEALTH_ALERT_TITLE: "策略健康度提醒",
        CheckText.HEALTH_ALERT_BODY: f'系統偵測到您目前的策略健康度為「{{level}}」。<br>為維護您的投資績效與資產穩健成長，建議盡快前往 <a href="{url.strategy_wizard.value}" style="color:#0078D7; text-decoration:none;">官網</a> 的策略精靈，更新至最新版本的策略。',
        CheckText.HEALTH_LEVEL_LOW: "低",
        CheckText.HEALTH_LEVEL_MEDIUM: "中",
        CheckText.HEALTH_LEVEL_HIGH: "高",
        CheckText.STRATEGY_HEALTH_LABEL: "策略健康度：",
        CheckText.HEALTH_INFO_TITLE: "策略健康度說明",
        CheckText.HEALTH_INFO_BODY: f'<span style="color:#28a745; font-size:16px;">●</span> <b>高</b>：策略狀態良好，可放心繼續使用。<br><br><span style="color:#ff9800; font-size:16px;">●</span> <b>中</b>：部分策略已開始過時，建議盡快更新以維持績效。<br><br><span style="color:#dc3545; font-size:16px;">●</span> <b>低</b>：策略已過時，績效可能受影響，請立即更新。<br><br>請前往 <a href="{url.strategy_wizard.value}" style="color:#0078D7; text-decoration:none;">官網</a> 的策略精靈更新最新策略，以保護您的投資。',
        CheckText.UPGRADE_REQUIRED_TITLE: "需要升級會員",
        CheckText.UPGRADE_REQUIRED_BODY: f'您目前的會員等級無法使用此功能。<br>請前往 <a href="{url.upgrade.value}" style="color:#0078D7; text-decoration:none;">官網</a> 升級會員，解鎖完整功能與專業策略。',
        CheckText.SUBSCRIPTION_EXPIRED_TITLE: "訂閱已過期",
        CheckText.SUBSCRIPTION_EXPIRED_BODY: f'您的訂閱已過期，目前無法使用付費功能。<br>請前往 <a href="{url.upgrade.value}" style="color:#0078D7; text-decoration:none;">官網</a> 續訂方案，繼續享有完整服務。',
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
        StrategyText.DIALOG_RISK_HTML: '<span style="font-size:13px; color:#333;">我已了解：當程式關閉、網路斷線、電腦關機或斷電時，程式交易將自動停止，未平倉部位需自行處理。</span>',
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
        StrategyText.ERROR_TRADE_EXPERT_DISABLED: "MT5 尚未開啟「允許算法交易」，請先至 MT5 開啟設定後再執行策略。",
        StrategyText.ERROR_TRADE_EXPERT_DISABLED_HTML: f'MT5 尚未開啟「允許算法交易」，請先至 MT5 開啟設定後再執行策略。<br>操作設定請參考：<a href="{url.terms_ea_setting.value}">操作設定</a>',
        StrategyText.CAPITAL: "本金：",
        StrategyText.VOLUME: "手數：",
        StrategyText.TERMS_HTML: StrategyText.TERMS_HTML.value,
        StrategyText.FOOTER: StrategyText.FOOTER.value,
        StrategyText.DIALOG_HTML_PREFIX: StrategyText.DIALOG_HTML_PREFIX.value
    },
    "en": {
        MainWindowText.TITLE: "MasQuant Trading System",
        MainWindowText.VERSION_PREFIX: "Version: v",
        MainWindowText.PROCESS_LOG_LABEL: "📝 Process Log",
        MainWindowText.BACKTEST_LOG_LABEL: "📊 Trading Signals",
        MainWindowText.BACKTEST_LOG_PLACEHOLDER: "Entry/exit and market signals shown here...",
        LoginText.TITLE: "MasQuant Trading System",
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
        CheckText.HEALTH_ALERT_TITLE: "Strategy Health Notice",
        CheckText.HEALTH_ALERT_BODY: f'Your current strategy health is "{{level}}".<br>To safeguard your investment performance and the steady growth of your assets, we recommend visiting the Strategy Wizard on our <a href="{url.strategy_wizard.value}" style="color:#0078D7; text-decoration:none;">official website</a> and updating to the latest strategy.',
        CheckText.HEALTH_LEVEL_LOW: "Low",
        CheckText.HEALTH_LEVEL_MEDIUM: "Medium",
        CheckText.HEALTH_LEVEL_HIGH: "High",
        CheckText.STRATEGY_HEALTH_LABEL: "Strategy Health: ",
        CheckText.HEALTH_INFO_TITLE: "About Strategy Health",
        CheckText.HEALTH_INFO_BODY: f'<span style="color:#28a745; font-size:16px;">●</span> <b>High</b>: Your strategy is in good condition. You may continue trading as usual.<br><br><span style="color:#ff9800; font-size:16px;">●</span> <b>Medium</b>: Some strategies are becoming outdated. We recommend updating them soon to maintain performance.<br><br><span style="color:#dc3545; font-size:16px;">●</span> <b>Low</b>: Your strategies are outdated and performance may be affected. Please update immediately.<br><br>Please visit the Strategy Wizard on our <a href="{url.strategy_wizard.value}" style="color:#0078D7; text-decoration:none;">official website</a> to update to the latest strategies and protect your investment.',
        CheckText.UPGRADE_REQUIRED_TITLE: "Upgrade Required",
        CheckText.UPGRADE_REQUIRED_BODY: f'Your current membership does not include this feature.<br>Please visit the <a href="{url.upgrade.value}" style="color:#0078D7; text-decoration:none;">official website</a> to upgrade and unlock the full features and professional strategies.',
        CheckText.SUBSCRIPTION_EXPIRED_TITLE: "Subscription Expired",
        CheckText.SUBSCRIPTION_EXPIRED_BODY: f'Your subscription has expired and paid features are currently unavailable.<br>Please visit the <a href="{url.upgrade.value}" style="color:#0078D7; text-decoration:none;">official website</a> to renew your plan and continue enjoying the full service.',
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
        StrategyText.DIALOG_RISK_HTML: '<span style="font-size:13px; color:#333;">I understand that automated trading will stop if the application is closed, the network is disconnected, or the computer shuts down. Any open positions must be managed manually.</span>',
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
        StrategyText.ERROR_TRADE_EXPERT_DISABLED: "MT5 'Algo Trading' is not enabled. Please enable it in MT5 settings before running the strategy.",
        StrategyText.ERROR_TRADE_EXPERT_DISABLED_HTML: f'MT5 "Algo Trading" is not enabled. Please enable it in MT5 settings before running the strategy.<br>Setup guide: <a href="{url.terms_ea_setting.value}">Setup Guide</a>',
        StrategyText.CAPITAL: "Capital:",
        StrategyText.VOLUME: "Volume (Lots):",
        StrategyText.TERMS_HTML: f'''
        <span style="font-size:13px; color:#333;">
        I have read and agree to the <a href="{url.terms_api.value}" style="color:#d2691e; text-decoration:none;">Terms of Use</a> and 
        <a href="{url.terms_disclaimer.value}" style="color:#d2691e; text-decoration:none;">Disclaimer</a>
        </span>
        ''',
        StrategyText.FOOTER: '''<span style="font-size:13px; color:#666;">🚀 Upgrade to MasQuant for more professional strategies: <a href="https://mas.mindaismart.com/plans" style="color:#0078D7;">Upgrade Now</a></span>''',
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