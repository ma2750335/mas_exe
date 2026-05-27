import enum
from env_info import ENV_VERSION


class info(enum.Enum):
    version = "1.0.0"
    health_monitor_minutes = 60
    # 從 env_info.ENV_VERSION 讀取（0=dev / 1=test / 2=pd）
    env_version = ENV_VERSION
    # 主 app base URL，依 env_version 對應 (dev, test, pd)
    base_url = (
        "http://localhost:3000",
        "https://mastest.mindaismart.com",
        "https://mas.mindaismart.com",
    )


def _base():
    """回傳當前環境的主 app base URL。"""
    return info.base_url.value[info.env_version.value]


class url(enum.Enum):
    # mas app routes（依 env_version 切換 base）
    register = f"{_base()}/authentication/sign-up"
    forget = f"{_base()}/authentication/forget-password"
    upgrade = f"{_base()}/plans"
    login = f"{_base()}/api/intermediary/login"
    strategy_wizard = f"{_base()}/strategy-wizard"
    strategy_health = f"{_base()}/api/mas-genie/strategy-health"

    # 非 mas app 子網域（目前不切 env；若需要切換之後在 info 加對應 base 變數）
    offical = "https://mindaismart.com/"
    terms_api = "https://mindaismart.com/terms_api"
    terms_disclaimer = "https://mindaismart.com/terms_disclaimer"
    terms_ea_setting = "https://doc.mindaismart.com/Getting_Started"


class dashboard(enum.Enum):
    # 報表名稱
    key_to_label_name = {
        "normal_report": "一般數據",
        "data_report": "完整數據",
        "kpi_report": "KPI 報表",
        "trade_report": "買賣點報表"
    }

    # 報表說明
    key_to_description = {
        "normal_report": "📄 資金淨值、交易次數",
        "data_report": "📊 資金淨值、累積報酬率、最大回撤、持倉統計等基本數據分析",
        "kpi_report": "🎯 勝率、獲利因子、Sharpe Ratio 等策略績效指標",
        "trade_report": "📈 策略進出場 K 線圖，顯示每筆買賣點、停損與進出場邏輯"
    }

    # 等級圖示與名稱
    # NOTE: PNG 檔名尚未實體改名，path 暫時保留舊檔名；改名 PNG 後同步更新 path
    level_icon_map = {
        "FREE": "src/free.png",
        "FREETRAIL": "src/bronze.png",
        "STARTER": "src/silver.png",
        "PRO": "src/gold.png"
    }
    level_access_map = {
        "FREE": "一般會員",
        "FREETRAIL": "體驗會員",
        "STARTER": "入門會員",
        "PRO": "專業會員"
    }
    level_color_map = {
        "FREE": "#6c757d",
        "FREETRAIL": "#cd7f32",
        "STARTER": "#c0c0c0",
        "PRO": "goldenrod"
    }
