from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, QUrl,QSettings
from PySide6.QtGui import QPixmap, QDesktopServices
import auth
import enum_setting as es
from i18n_strings import LoginText, get_text
from check import login_and_notify, get_resource_path, check_and_notify
settings = QSettings("mas_tech", "mas_login")

class LoginForm(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle(get_text(LoginText.TITLE))
        self.resize(700, 500)

        # ===== Logo =====
        self.label_logo = QLabel(self)
        self.label_logo.setPixmap(QPixmap(get_resource_path(
            "logo.png")).scaled(300, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_logo.setAlignment(Qt.AlignCenter)

        # ===== 帳號 & 密碼輸入 =====
        self.label_username = QLabel()
        self.textbox_username = QLineEdit("")

        self.label_password = QLabel()
        self.textbox_password = QLineEdit("")
        self.textbox_password.setEchoMode(QLineEdit.Password)

        self.chk_remember = QCheckBox(get_text(LoginText.REMEBER))
        self.chk_remember.setStyleSheet("QCheckBox::indicator{width: 13px;height: 13px;}")
        
        

        # ===== 登入與註冊按鈕 =====
        self.btn_login = QPushButton()
        self.btn_login.setFixedSize(80, 32)

        self.btn_register = QPushButton()
        self.btn_register.setFixedSize(80, 32)
        self.btn_register.clicked.connect(self.open_register_page)

        # ===== 忘記密碼連結 =====
        self.label_forgot = QLabel()
        self.label_forgot.setOpenExternalLinks(True)
        self.label_forgot.setTextFormat(Qt.RichText)
        self.label_forgot.setTextInteractionFlags(Qt.TextBrowserInteraction)

        # ===== 排版 Layout =====
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.label_logo, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)

        # 表單區
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(10)
        form_layout.addWidget(self.label_username, 0, 0)
        form_layout.addWidget(self.textbox_username, 0, 1)
        form_layout.addWidget(self.label_password, 1, 0)
        form_layout.addWidget(self.textbox_password, 1, 1)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.chk_remember, alignment=Qt.AlignRight)

        # checkbox
        self.chk_terms = QCheckBox()
        self.chk_terms.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.chk_terms.setStyleSheet("""
                                     QCheckBox::indicator{width: 15px;height: 15px;}
                                     """)

        self.label_terms = QLabel(get_text(LoginText.TERMS_HTML))
        self.label_terms.setTextFormat(Qt.RichText)
        self.label_terms.setOpenExternalLinks(True)
        self.label_terms.setWordWrap(True)
        self.label_terms.setStyleSheet("font-size:13px;")

        terms_layout = QHBoxLayout()
        terms_layout.addWidget(self.chk_terms)
        terms_layout.addWidget(self.label_terms)
        main_layout.addLayout(terms_layout)

        # 按鈕 + 忘記密碼
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_login)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.btn_register)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.label_forgot)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.update_text()
        self.load_saved_credentials()
        self.btn_login.clicked.connect(self.login_click)

    def load_saved_credentials(self):
        settings = QSettings("mas_tech", "mas_login")
        username = settings.value("username", "")
        password = settings.value("password", "")

        self.textbox_username.setText(username)
        self.textbox_password.setText(password)

        if username and password:
            self.chk_remember.setChecked(True)

    def update_text(self):
        """依目前語言更新所有文字"""
        self.setWindowTitle(get_text(LoginText.TITLE))
        self.label_username.setText(get_text(LoginText.USERNAME))
        self.label_password.setText(get_text(LoginText.PASSWORD))
        self.btn_login.setText(get_text(LoginText.LOGIN_BUTTON))
        self.btn_register.setText(get_text(LoginText.REGISTER_BUTTON))
        self.label_forgot.setText(
            f'<a href={es.url.forget.value} style="color:#0078D7;">{get_text(LoginText.FORGOT_PASSWORD)}</a>'
        )
        self.label_terms.setText(get_text(LoginText.TERMS_HTML))
        self.chk_remember.setText(get_text(LoginText.REMEBER))

    def open_register_page(self):
        QDesktopServices.openUrl(QUrl(es.url.register.value))

    def login_click(self):
        self.btn_login.setEnabled(False)
        username = self.textbox_username.text()
        password = self.textbox_password.text()
        
        settings = QSettings("mas_tech", "mas_login")
        if self.chk_remember.isChecked():
            settings.setValue("username", username)
            settings.setValue("password", password)
        else:
            settings.remove("username")
            settings.remove("password")
        
        if not self.chk_terms.isChecked():
            QMessageBox.warning(self, get_text(LoginText.ERROR_TITLE), get_text(
                LoginText.ERROR_TERMS_REQUIRED))
            self.btn_login.setEnabled(True)
            return

        result = auth.login_request(username, password)

        if check_and_notify(self):
            if result.get("result"):
                if result.get("level") == 'FREE':
                    login_and_notify(
                        self, "Please Upgrade Now To Unlock This Feature. \nUPGRADE: https://mas.mindaismart.com")
                else:
                    if self.on_login_success:
                        self.on_login_success(
                            result.get("level"),
                            result.get("access"),
                            result.get("expire_date")
                        )
            else:
                login_and_notify(self, result.get("msg"))
        self.btn_login.setEnabled(True)
