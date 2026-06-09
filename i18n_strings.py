# i18n_strings.py（追加內容）

from enum import Enum
from enum_setting import url
DEFAULT_LANG = "en"


# 語言循環順序：英文 → 繁中 → 簡中 → 英文 ...
_LANG_CYCLE = ["en", "zh", "cn"]


def switch_lang():
    """循環切換語言：en → zh → cn → en。"""
    global DEFAULT_LANG
    try:
        idx = _LANG_CYCLE.index(DEFAULT_LANG)
    except ValueError:
        idx = 0
    DEFAULT_LANG = _LANG_CYCLE[(idx + 1) % len(_LANG_CYCLE)]


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
    LOGIN_NOTICE_TITLE = "提醒"
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
    SESSION_DUPLICATE_TITLE = "重複登入"
    SESSION_DUPLICATE_BODY = "session_duplicate_body"


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
    FOOTER = f'''<span style="font-size:13px; color:#666;">🚀 點我升級 MasQuant，立即創造更多專業策略：<a href="{url.upgrade.value}" style="color:#0078D7;">前往升級</a></span>'''
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
    CAPITAL_LOTS_LABEL = "資金規模："
    CAPITAL_LOTS_OPTION = "本金 {capital} USD / 手數 {lots}"
    STRATEGY_ID = "策略 ID："
    SYMBOL = "商品："
    STOP_CONFIRM_TITLE = "確認停止策略"
    STOP_CONFIRM_BODY = "stop_confirm_body"
    STOP_CONFIRM_OK = "確認"


LEVEL_LABEL = {
    "zh": {
        "FREE": "一般會員",
        "STARTER": "入門會員",
        "GROWTH": "進階會員",
        "PRO": "專業會員"
    },
    "en": {
        "FREE": "Free Member",
        "STARTER": "Starter",
        "GROWTH": "Growth",
        "PRO": "Pro"
    },
    "cn": {
        "FREE": "一般会员",
        "STARTER": "入门会员",
        "GROWTH": "进阶会员",
        "PRO": "专业会员"
    }
}

LEVEL_COLOR = {
    "FREE": "#6c757d",
    "STARTER": "#cd7f32",
    "GROWTH": "#c0c0c0",
    "PRO": "goldenrod"
}

# NOTE: PNG 檔名尚未實體改名，path 暫時保留舊檔名；改名 PNG 後同步更新 path
LEVEL_ICON = {
    "FREE": "src/free.png",
    "STARTER": "src/bronze.png",
    "GROWTH": "src/silver.png",
    "PRO": "src/gold.png"
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
        CheckText.LOGIN_NOTICE_TITLE: "提醒",
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
        CheckText.SESSION_DUPLICATE_TITLE: "重複登入",
        CheckText.SESSION_DUPLICATE_BODY: f'本機已開啟此帳號的 MasQuant 交易系統。<br><br>為避免策略衝突與重複下單風險，目前同一帳號在同一台電腦上僅能開啟一個視窗。<br>請先關閉現有視窗後再試一次。<br><br>若您需要同時部署多個視窗執行策略，請前往 <a href="{url.upgrade.value}" style="color:#0078D7; text-decoration:none;">官網</a> 升級會員等級以解鎖此功能。',
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
        StrategyText.CAPITAL_LOTS_LABEL: "資金規模：",
        StrategyText.CAPITAL_LOTS_OPTION: "本金 {capital} USD / 手數 {lots}",
        StrategyText.STRATEGY_ID: "策略 ID：",
        StrategyText.SYMBOL: "商品：",
        StrategyText.STOP_CONFIRM_TITLE: "確認停止策略",
        StrategyText.STOP_CONFIRM_BODY: '⚠️ 重要：停止策略後，程式 <b>不會自動平倉</b>。<br>您 MT5 中所有未平倉部位將維持原狀，<b>繼續承受市場波動風險</b>。<br><br>請於停止後立即至 MT5 手動處理未平倉部位，以避免損失擴大。<br><br>確定要停止策略嗎？',
        StrategyText.STOP_CONFIRM_OK: "確認",
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
        CheckText.LOGIN_NOTICE_TITLE: "Notice",
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
        CheckText.SESSION_DUPLICATE_TITLE: "Duplicate Login Detected",
        CheckText.SESSION_DUPLICATE_BODY: f'MasQuant Trading System is already open with this account on this machine.<br><br>To prevent strategy conflicts and duplicate orders, only one window per account is currently allowed on the same computer.<br>Please close the existing window and try again.<br><br>If you need to run multiple windows simultaneously, please visit the <a href="{url.upgrade.value}" style="color:#0078D7; text-decoration:none;">official website</a> to upgrade your membership and unlock this feature.',
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
        StrategyText.CAPITAL_LOTS_LABEL: "Account Size: ",
        StrategyText.CAPITAL_LOTS_OPTION: "Capital {capital} USD / Lots {lots}",
        StrategyText.STRATEGY_ID: "Strategy ID: ",
        StrategyText.SYMBOL: "Symbol: ",
        StrategyText.STOP_CONFIRM_TITLE: "Confirm Stop Strategy",
        StrategyText.STOP_CONFIRM_BODY: '⚠️ Important: Stopping the strategy will <b>NOT auto-close your positions</b>.<br>All open positions in MT5 will remain and <b>continue to be exposed to market risk</b>.<br><br>Please close any open positions manually in MT5 immediately after stopping, to prevent further losses.<br><br>Are you sure you want to stop?',
        StrategyText.STOP_CONFIRM_OK: "Confirm",
        StrategyText.TERMS_HTML: f'''
        <span style="font-size:13px; color:#333;">
        I have read and agree to the <a href="{url.terms_api.value}" style="color:#d2691e; text-decoration:none;">Terms of Use</a> and 
        <a href="{url.terms_disclaimer.value}" style="color:#d2691e; text-decoration:none;">Disclaimer</a>
        </span>
        ''',
        StrategyText.FOOTER: f'''<span style="font-size:13px; color:#666;">🚀 Upgrade to MasQuant for more professional strategies: <a href="{url.upgrade.value}" style="color:#0078D7;">Upgrade Now</a></span>''',
        StrategyText.DIALOG_HTML_PREFIX: '''
        <b>Please confirm strategy settings:</b><br>
        <b>Account:</b> {account}<br>
        <b>Server:</b> {server}<br>
        '''
    },
    "cn": {
        MainWindowText.TITLE: "MasQuant 交易系统",
        MainWindowText.VERSION_PREFIX: "版本：v",
        MainWindowText.PROCESS_LOG_LABEL: "📝 流程 Log",
        MainWindowText.BACKTEST_LOG_LABEL: "📊 交易信号 Log",
        MainWindowText.BACKTEST_LOG_PLACEHOLDER: "这里显示进出场与市价信号...",
        LoginText.TITLE: "MasQuant 交易系统",
        LoginText.USERNAME: "账号：",
        LoginText.PASSWORD: "密码：",
        LoginText.LOGIN_BUTTON: "登录",
        LoginText.REGISTER_BUTTON: "注册",
        LoginText.FORGOT_PASSWORD: "忘记密码？",
        LoginText.TERMS_HTML: f'''
        <span style="font-size:13px; color:#333;">
        自动化交易前，请先确认MT5 EA设置 <a href="{url.terms_ea_setting.value}" style="color:#d2691e; text-decoration:none;">操作设置</a>
        </span>
    ''',
        LoginText.ERROR_TITLE: "错误",
        LoginText.REMEBER: "记住我",
        LoginText.ERROR_TERMS_REQUIRED: "请先确认MT5设置才能执行策略。",
        CheckText.VERSION_ALERT_TITLE: "版本更新提醒",
        CheckText.VERSION_ALERT_BODY: "发现新版本 {latest}，您当前使用的是 {current}\n请至官网下载最新版！",
        CheckText.LOGIN_FAILED_TITLE: "登录失败",
        CheckText.LOGIN_FAILED_BODY: "请重新确认账号密码！",
        CheckText.LOGIN_NOTICE_TITLE: "提醒",
        CheckText.HEALTH_ALERT_TITLE: "策略健康度提醒",
        CheckText.HEALTH_ALERT_BODY: f'系统检测到您当前的策略健康度为「{{level}}」。<br>为维护您的投资绩效与资产稳健成长，建议尽快前往 <a href="{url.strategy_wizard.value}" style="color:#0078D7; text-decoration:none;">官网</a> 的策略向导，更新至最新版本的策略。',
        CheckText.HEALTH_LEVEL_LOW: "低",
        CheckText.HEALTH_LEVEL_MEDIUM: "中",
        CheckText.HEALTH_LEVEL_HIGH: "高",
        CheckText.STRATEGY_HEALTH_LABEL: "策略健康度：",
        CheckText.HEALTH_INFO_TITLE: "策略健康度说明",
        CheckText.HEALTH_INFO_BODY: f'<span style="color:#28a745; font-size:16px;">●</span> <b>高</b>：策略状态良好，可放心继续使用。<br><br><span style="color:#ff9800; font-size:16px;">●</span> <b>中</b>：部分策略已开始过时，建议尽快更新以维持绩效。<br><br><span style="color:#dc3545; font-size:16px;">●</span> <b>低</b>：策略已过时，绩效可能受影响，请立即更新。<br><br>请前往 <a href="{url.strategy_wizard.value}" style="color:#0078D7; text-decoration:none;">官网</a> 的策略向导更新最新策略，以保护您的投资。',
        CheckText.UPGRADE_REQUIRED_TITLE: "需要升级会员",
        CheckText.UPGRADE_REQUIRED_BODY: f'您当前的会员等级无法使用此功能。<br>请前往 <a href="{url.upgrade.value}" style="color:#0078D7; text-decoration:none;">官网</a> 升级会员，解锁完整功能与专业策略。',
        CheckText.SUBSCRIPTION_EXPIRED_TITLE: "订阅已过期",
        CheckText.SUBSCRIPTION_EXPIRED_BODY: f'您的订阅已过期，当前无法使用付费功能。<br>请前往 <a href="{url.upgrade.value}" style="color:#0078D7; text-decoration:none;">官网</a> 续订方案，继续享有完整服务。',
        CheckText.SESSION_DUPLICATE_TITLE: "重复登录",
        CheckText.SESSION_DUPLICATE_BODY: f'本机已打开此账号的 MasQuant 交易系统。<br><br>为避免策略冲突与重复下单风险，当前同一账号在同一台电脑上仅能打开一个窗口。<br>请先关闭现有窗口后再试一次。<br><br>若您需要同时部署多个窗口执行策略，请前往 <a href="{url.upgrade.value}" style="color:#0078D7; text-decoration:none;">官网</a> 升级会员等级以解锁此功能。',
        StrategyText.TITLE: "策略设置",
        StrategyText.LOGIN_ID: "MT5登录账号：",
        StrategyText.PASSWORD: "MT5登录密码：",
        StrategyText.SERVER: "MT5券商服务器：",
        StrategyText.START: "开始执行",
        StrategyText.STOP: "停止",
        StrategyText.STATUS_IDLE: "状态：未执行",
        StrategyText.ERROR_TITLE: "错误",
        StrategyText.ERROR_INPUT_REQUIRED: "请填写所有设置值！",
        StrategyText.ERROR_TERMS_REQUIRED: "请先勾选同意条款与政策才能执行策略。",
        StrategyText.DIALOG_TITLE: "确认交易设置",
        StrategyText.DIALOG_CONFIRM: "确认执行",
        StrategyText.DIALOG_CANCEL: "取消",
        StrategyText.DIALOG_RISK_HTML: '<span style="font-size:13px; color:#333;">我已了解：当程序关闭、网络断线、电脑关机或断电时，程序交易将自动停止，未平仓仓位需自行处理。</span>',
        StrategyText.LOG_OPENED: "🛠 打开策略设置界面",
        StrategyText.LOG_DIALOG: "📌 显示交易确认窗口",
        StrategyText.LOG_STARTED: "🚀 策略开始执行",
        StrategyText.LOG_STOPPED: "⏹️ 策略已停止",
        StrategyText.STATUS_RUNNING: "策略执行中...",
        StrategyText.STATUS_DONE: "❗ 策略执行完成，策略执行中，请勿关闭窗口，关闭窗口则程序交易也会停止！",
        StrategyText.STATUS_FAILED: "❌ 策略执行失败！",
        StrategyText.LOG_SUCCESS: "✅ 策略执行中！",
        StrategyText.LOG_FAILED: "❌ 策略失败：{error}",
        StrategyText.ERROR_SYMBOL_NOT_FOUND: "商品代码错误，请输入正确的商品代码",
        StrategyText.ERROR_TRADE_EXPERT_DISABLED: "MT5 尚未开启「允许算法交易」，请先至 MT5 开启设置后再执行策略。",
        StrategyText.ERROR_TRADE_EXPERT_DISABLED_HTML: f'MT5 尚未开启「允许算法交易」，请先至 MT5 开启设置后再执行策略。<br>操作设置请参考：<a href="{url.terms_ea_setting.value}">操作设置</a>',
        StrategyText.CAPITAL: "本金：",
        StrategyText.VOLUME: "手数：",
        StrategyText.CAPITAL_LOTS_LABEL: "资金规模：",
        StrategyText.CAPITAL_LOTS_OPTION: "本金 {capital} USD / 手数 {lots}",
        StrategyText.STRATEGY_ID: "策略 ID：",
        StrategyText.SYMBOL: "商品：",
        StrategyText.STOP_CONFIRM_TITLE: "确认停止策略",
        StrategyText.STOP_CONFIRM_BODY: '⚠️ 重要：停止策略后，程序 <b>不会自动平仓</b>。<br>您 MT5 中所有未平仓仓位将维持原状，<b>继续承受市场波动风险</b>。<br><br>请于停止后立即至 MT5 手动处理未平仓仓位，以避免损失扩大。<br><br>确定要停止策略吗？',
        StrategyText.STOP_CONFIRM_OK: "确认",
        StrategyText.TERMS_HTML: f'''
        <span style="font-size:13px; color:#333;">
        我已阅读及同意以上使用条款 <a href="{url.terms_api.value}" style="color:#d2691e; text-decoration:none;">使用条款</a> 和
        <a href="{url.terms_disclaimer.value}" style="color:#d2691e; text-decoration:none;">免责声明</a>
        </span>
    ''',
        StrategyText.FOOTER: f'''<span style="font-size:13px; color:#666;">🚀 点我升级 MasQuant，立即创造更多专业策略：<a href="{url.upgrade.value}" style="color:#0078D7;">前往升级</a></span>''',
        StrategyText.DIALOG_HTML_PREFIX: '''
        <b>请确认交易设置：</b><br>
        <b>券商账号：</b> {account}<br>
        <b>券商服务器：</b> {server}<br>
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