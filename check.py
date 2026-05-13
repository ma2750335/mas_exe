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


def health_alert_if_needed(parent, healthy):
    if healthy not in (0, 1):
        return
    level_key = CheckText.HEALTH_LEVEL_LOW if healthy == 0 else CheckText.HEALTH_LEVEL_MEDIUM
    body = get_text(CheckText.HEALTH_ALERT_BODY).format(level=get_text(level_key))
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Warning)
    box.setWindowTitle(get_text(CheckText.HEALTH_ALERT_TITLE))
    box.setTextFormat(Qt.RichText)
    box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    box.setText(body)
    box.setStandardButtons(QMessageBox.Ok)
    box.exec_()
