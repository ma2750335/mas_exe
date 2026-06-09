from PySide6.QtWidgets import QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon
from login import LoginForm
from main_window import MainWindow
import winform_style
from i18n_strings import switch_lang, get_current_lang, get_text, MainWindowText
from check import get_resource_path, show_session_duplicate_dialog

def main():
    app = QApplication([])
    app.setWindowIcon(QIcon(get_resource_path("logo.ico")))
    app.setStyleSheet(winform_style.style_sheet)

    # 初始化主視窗（先不 show）
    main_window = MainWindow()

    # 語言切換按鈕 UI（整合到登入畫面右上角）
    language_button = QPushButton()
    language_button.setFixedWidth(100)

    # 按鈕顯示「下一個」要切換到的語言（與 switch_lang 的 en→zh→cn 循環順序一致）
    _NEXT_LANG_LABEL = {"en": "繁體中文", "zh": "简体中文", "cn": "English"}

    def update_language_button_text():
        language_button.setText(_NEXT_LANG_LABEL.get(get_current_lang(), "繁體中文"))

    def toggle_language():
        switch_lang()
        update_language_button_text()
        login_form.update_text()
        container.setWindowTitle(get_text(MainWindowText.TITLE))

    language_button.clicked.connect(toggle_language)
    update_language_button_text()

    # 登入成功的 callback：進入主畫面
    def on_login_success(user_level, access_permissions, expire_date, healthy, is_subsription, user_id, strategy_id, symbol, capital, lots):
        if not main_window.start_with_user(user_level, access_permissions, expire_date, healthy, is_subsription, user_id, strategy_id, symbol, capital, lots):
            show_session_duplicate_dialog(container)
            app.quit()
            return
        container.close()
        main_window.show()

    # 顯示登入視窗
    login_form = LoginForm(on_login_success=on_login_success)

    # 加上語言切換按鈕到上方
    top_layout = QHBoxLayout()
    top_layout.addStretch()
    top_layout.addWidget(language_button)

    layout = QVBoxLayout()
    layout.addLayout(top_layout)
    layout.addWidget(login_form)

    container = QWidget()
    container.setLayout(layout)
    container.setWindowTitle(get_text(MainWindowText.TITLE))
    container.setWindowIcon(QIcon(get_resource_path("logo.ico")))
    container.setStyleSheet(winform_style.style_sheet)
    container.resize(800, 500)
    container.show()

    app.exec()


if __name__ == "__main__":
    main()
