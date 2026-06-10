from PySide6.QtWidgets import QMessageBox, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
import auth
import enum_setting as es
from i18n_strings import CheckText, StrategyText, get_text
from env_info import IS_GENIE
import sys
import os

CURRENT_VERSION = es.info.version.value


def is_genai_enabled():
    """True if env_info.IS_GENAI is set. Gates all health-related UI and monitoring."""
    return IS_GENIE


def get_resource_path(relative_path):
        """取得資源的正確路徑（支援 PyInstaller 打包後）"""
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

def get_latest_version() -> str:
    try:
        return auth.check_version()
    except Exception:
        return CURRENT_VERSION


def check_and_notify(main_window):
    last_version = get_latest_version()
    if last_version != CURRENT_VERSION:
        QMessageBox.warning(
            main_window,
            get_text(CheckText.VERSION_ALERT_TITLE),
            get_text(CheckText.VERSION_ALERT_BODY).format(
                latest=last_version, current=CURRENT_VERSION
            )
        )
        return False
    return True


def login_and_notify(main_window, msg=None, is_success=False):
    """顯示後端回傳的登入訊息（rsp 的 msg_toggle=True 時呼叫）。

    登入成敗與訊息內容皆由 SERVER 端決定；前端不再用 error code 對應本地 i18n。
    is_success 只決定彈窗標題：
      - True  → 中性「提醒」（登入成功但後端仍附帶一則通知）
      - False → 「登入失敗」
    msg 為空時 fall back 到本地預設 LOGIN_FAILED_BODY。
    """
    body = msg or get_text(CheckText.LOGIN_FAILED_BODY)
    title_key = CheckText.LOGIN_NOTICE_TITLE if is_success else CheckText.LOGIN_FAILED_TITLE
    _show_html_alert(main_window, get_text(title_key), body)


def get_health_display(health_rsp):
    """Return (label_text, color_hex) for a health-response dict.

    Returns (None, None) when IS_GENAI is off, rsp is None, or healthLevel is UNKNOWN.
    """
    if not is_genai_enabled():
        return None, None
    if not health_rsp or not isinstance(health_rsp, dict):
        return None, None
    level = health_rsp.get("healthLevel")
    if level == "HIGH":
        return get_text(CheckText.HEALTH_LEVEL_HIGH), "#28a745"
    if level == "MEDIUM":
        return get_text(CheckText.HEALTH_LEVEL_MEDIUM), "#ff9800"
    if level == "LOW":
        return get_text(CheckText.HEALTH_LEVEL_LOW), "#dc3545"
    return None, None


def _force_min_width(box, min_width=480):
    """強制 QMessageBox 最小寬度，避免標題列文字被截斷。

    QMessageBox 預設只依「內文」寬度自適應；當內文很短而標題較長時，
    視窗會太窄、標題列文字被省略成「…」。做法是在 grid layout 最底列
    塞一個橫向 spacer 撐出最小寬度，標題就有空間完整顯示。
    """
    layout = box.layout()
    if layout is None:
        return
    spacer = QSpacerItem(min_width, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout.addItem(spacer, layout.rowCount(), 0, 1, layout.columnCount())


def _show_html_alert(parent, title, body_html):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Warning)
    box.setWindowTitle(title)
    box.setTextFormat(Qt.RichText)
    box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    box.setText(body_html)
    box.setStandardButtons(QMessageBox.Ok)
    _force_min_width(box)
    box.exec_()


def health_alert_if_needed(parent, health_rsp) -> bool:
    """Show alert when action is WARN or STOP.

    Returns:
        True if the strategy should be stopped (shouldStop=True); False otherwise.
    """
    if not is_genai_enabled():
        return False
    if not health_rsp or not isinstance(health_rsp, dict):
        return False
    action = health_rsp.get("action")
    should_stop = bool(health_rsp.get("shouldStop", False))
    if action not in ("WARN", "STOP"):
        return should_stop
    # Prefer backend message (already localised); fall back to local template
    body = health_rsp.get("message") or get_text(CheckText.HEALTH_ALERT_BODY).format(
        level=get_text(
            CheckText.HEALTH_LEVEL_LOW
            if health_rsp.get("healthLevel") == "LOW"
            else CheckText.HEALTH_LEVEL_MEDIUM
        )
    )
    _show_html_alert(parent, get_text(CheckText.HEALTH_ALERT_TITLE), body)
    return should_stop


def show_health_info_dialog(parent):
    if not is_genai_enabled():
        return
    _show_html_alert(
        parent,
        get_text(CheckText.HEALTH_INFO_TITLE),
        get_text(CheckText.HEALTH_INFO_BODY),
    )


def show_session_duplicate_dialog(parent):
    _show_html_alert(
        parent,
        get_text(CheckText.SESSION_DUPLICATE_TITLE),
        get_text(CheckText.SESSION_DUPLICATE_BODY),
    )


def confirm_stop_strategy(parent):
    """彈確認窗：停止策略前警告手動平倉。

    Returns:
        True 若使用者按「確認」；False 若按「取消」或關閉視窗。
    預設按鈕為「取消」——防止 Enter 誤觸造成意外停止。
    """
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Warning)
    box.setWindowTitle(get_text(StrategyText.STOP_CONFIRM_TITLE))
    box.setTextFormat(Qt.RichText)
    box.setText(get_text(StrategyText.STOP_CONFIRM_BODY))
    btn_confirm = box.addButton(get_text(StrategyText.STOP_CONFIRM_OK), QMessageBox.AcceptRole)
    btn_cancel = box.addButton(get_text(StrategyText.DIALOG_CANCEL), QMessageBox.RejectRole)
    box.setDefaultButton(btn_cancel)
    box.exec_()
    return box.clickedButton() == btn_confirm


def check_subscription(parent, level, is_subsription=None):
    """Return True if user may proceed; show modal alert and return False otherwise.

    只有 FREE 會被擋（提示升級會員）。STARTER / GROWTH / PRO 一律放行，
    不再因 is_subsription 卡控登入。
    （保留 is_subsription 參數以維持 login.py 呼叫端相容，目前不使用。）
    """
    if level == 'FREE':
        _show_html_alert(
            parent,
            get_text(CheckText.UPGRADE_REQUIRED_TITLE),
            get_text(CheckText.UPGRADE_REQUIRED_BODY),
        )
        return False
    return True
