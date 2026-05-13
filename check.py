from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
import auth
import enum_setting as es
from i18n_strings import CheckText, get_text
import sys
import os

CURRENT_VERSION = es.info.version.value

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


def login_and_notify(main_window, msg):
    if not msg:
        msg = get_text(CheckText.LOGIN_FAILED_BODY)
    QMessageBox.warning(
        main_window,
        get_text(CheckText.LOGIN_FAILED_TITLE),
        msg
    )


def get_health_display(healthy):
    """Return (label_text, color_hex) for healthy=0/1/2. Return (None, None) for unknown/None."""
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
    if healthy not in (0, 1):
        return
    level_key = CheckText.HEALTH_LEVEL_LOW if healthy == 0 else CheckText.HEALTH_LEVEL_MEDIUM
    body = get_text(CheckText.HEALTH_ALERT_BODY).format(level=get_text(level_key))
    _show_html_alert(parent, get_text(CheckText.HEALTH_ALERT_TITLE), body)


def show_health_info_dialog(parent):
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
