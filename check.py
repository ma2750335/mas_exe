from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
import auth
import enum_setting as es
from i18n_strings import CheckText, StrategyText, get_text
from env_info import IS_GENAI
import sys
import os

CURRENT_VERSION = es.info.version.value


def is_genai_enabled():
    """True if env_info.IS_GENAI is set. Gates all health-related UI and monitoring."""
    return IS_GENAI


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


_LOGIN_ERROR_CODE_MAP = {
    "Error_exe_login_001": CheckText.LOGIN_ERROR_001,
    "Error_exe_login_002": CheckText.LOGIN_ERROR_002,
    "Error_exe_login_003": CheckText.LOGIN_ERROR_003,
    "Error_exe_login_004": CheckText.LOGIN_ERROR_004,
    "Error_exe_login_005": CheckText.LOGIN_ERROR_005,
    "Error_exe_login_006": CheckText.LOGIN_ERROR_006,
    "Error_exe_login_007": CheckText.LOGIN_ERROR_007,
    "Error_exe_login_008": CheckText.LOGIN_ERROR_008,
    "Error_exe_login_999": CheckText.LOGIN_ERROR_999,
}


def login_and_notify(main_window, msg=None, code=None):
    """Show login failure dialog.

    Resolution order:
      1. code 已知 → 用對應 i18n message（支援 HTML 連結）
      2. code 未知或缺 → fall back 到後端 raw msg
      3. 都沒有 → fall back 到本地預設 LOGIN_FAILED_BODY
    """
    if code and code in _LOGIN_ERROR_CODE_MAP:
        body = get_text(_LOGIN_ERROR_CODE_MAP[code])
    elif msg:
        body = msg
    else:
        body = get_text(CheckText.LOGIN_FAILED_BODY)
    _show_html_alert(main_window, get_text(CheckText.LOGIN_FAILED_TITLE), body)


def get_health_display(healthy):
    """Return (label_text, color_hex) for healthy=0/1/2. Return (None, None) when IS_GENAI is off or value unknown."""
    if not is_genai_enabled():
        return None, None
    if healthy == 0:
        return get_text(CheckText.HEALTH_LEVEL_LOW), "#dc3545"
    if healthy == 1:
        return get_text(CheckText.HEALTH_LEVEL_MEDIUM), "#ff9800"
    if healthy == 2:
        return get_text(CheckText.HEALTH_LEVEL_HIGH), "#28a745"
    return None, None


def _show_html_alert(parent, title, body_html):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Warning)
    box.setWindowTitle(title)
    box.setTextFormat(Qt.RichText)
    box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    box.setText(body_html)
    box.setStandardButtons(QMessageBox.Ok)
    box.exec_()


def health_alert_if_needed(parent, healthy):
    if not is_genai_enabled():
        return
    if healthy not in (0, 1):
        return
    level_key = CheckText.HEALTH_LEVEL_LOW if healthy == 0 else CheckText.HEALTH_LEVEL_MEDIUM
    body = get_text(CheckText.HEALTH_ALERT_BODY).format(level=get_text(level_key))
    _show_html_alert(parent, get_text(CheckText.HEALTH_ALERT_TITLE), body)


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


def check_subscription(parent, level, is_subsription):
    """Return True if user may proceed; show modal alert and return False otherwise."""
    if level == 'FREE':
        _show_html_alert(
            parent,
            get_text(CheckText.UPGRADE_REQUIRED_TITLE),
            get_text(CheckText.UPGRADE_REQUIRED_BODY),
        )
        return False
    if not is_subsription:
        _show_html_alert(
            parent,
            get_text(CheckText.SUBSCRIPTION_EXPIRED_TITLE),
            get_text(CheckText.SUBSCRIPTION_EXPIRED_BODY),
        )
        return False
    return True
