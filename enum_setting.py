import enum


class url(enum.Enum):
    offical = "https://mindaismart.com/"
    register = "https://mas.mindaismart.com/authentication/sign-up"
    forget = "https://mas.mindaismart.com/authentication/forget-password"
    upgrade = "https://mas.mindaismart.com/plans"
    login = "https://mas.mindaismart.com/api/intermediary/login"
    terms_api = "https://mindaismart.com/terms_api"
    terms_disclaimer = "https://mindaismart.com/terms_disclaimer"
    terms_ea_setting = "https://doc.mindaismart.com/Getting_Started"

class info(enum.Enum):
    version = "1.0.0"


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
    level_icon_map = {
        "free": "src/free.png",
        "free_trail": "src/free_trail.png",
        "bronze": "src/bronze.png",
        "silver": "src/silver.png",
        "gold": "src/gold.png"
    }
    level_access_map = {
        "free": "一般會員",
        "free_trail": "體驗會員",
        "bronze": "銅級會員",
        "silver": "銀級會員",
        "gold": "黃金會員"
    }
    level_color_map = {
        "free_trail": "#0078D7",
        "free": "#6c757d",
        "bronze": "#cd7f32",
        "silver": "#c0c0c0",
        "gold": "goldenrod"
    }
