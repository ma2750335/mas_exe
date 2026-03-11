from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QStackedWidget, QLabel
from PySide6.QtGui import QFont
import datetime
from strategy_settings import StrategySettingsForm
from i18n_strings import get_text
from i18n_strings import MainWindowText


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #333;
                font-weight: bold;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QLineEdit {
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
            }
        """)
        self.setWindowTitle(get_text(MainWindowText.TITLE))
        self.resize(800, 500)

        # 主內容切換區
        self.main_content = QStackedWidget()

        # ====== 右側 Log 區域（上下排列）======
        right_panel = QVBoxLayout()

        # --- 上方：流程 Log ---
        self.lbl_process_log = QLabel(get_text(MainWindowText.PROCESS_LOG_LABEL))
        self.lbl_process_log.setFont(QFont("Arial", 11, QFont.Bold))
        self.lbl_process_log.setStyleSheet("color: #0078D7; padding: 2px 0;")

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setPlaceholderText("這裡顯示流程或 Log 訊息...")
        self.text_display.setFixedWidth(300)
        self.text_display.setFont(QFont("Courier New", 14))

        right_panel.addWidget(self.lbl_process_log)
        right_panel.addWidget(self.text_display, stretch=1)

        # --- 下方：回測 Log ---
        self.lbl_backtest_log = QLabel(get_text(MainWindowText.BACKTEST_LOG_LABEL))
        self.lbl_backtest_log.setFont(QFont("Arial", 11, QFont.Bold))
        self.lbl_backtest_log.setStyleSheet("color: #E65100; padding: 2px 0;")

        self.backtest_log_display = QTextEdit()
        self.backtest_log_display.setReadOnly(True)
        self.backtest_log_display.setPlaceholderText(get_text(MainWindowText.BACKTEST_LOG_PLACEHOLDER))
        self.backtest_log_display.setFixedWidth(300)
        self.backtest_log_display.setFont(QFont("Courier New", 12))

        right_panel.addWidget(self.lbl_backtest_log)
        right_panel.addWidget(self.backtest_log_display, stretch=1)

        # 佈局
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.main_content, stretch=2)
        main_layout.addLayout(right_panel, stretch=1)

        bottom_layout = QVBoxLayout()
        bottom_layout.addLayout(main_layout)

        self.setLayout(bottom_layout)

        # 狀態變數
        self.current_view = "process"
        self.process_log = []
        self.log_messages = []
        self.backtest_log_messages = []

    def start_with_user(self, user_level, access_token, expire_date):
        """登入後呼叫此方法初始化策略畫面"""
        print(f"✅ 使用者登入成功（等級: {user_level}, 到期: {expire_date}）")
        self.refresh_labels()
        self.load_setting_form()

    def load_setting_form(self):
        """ 載入策略設定畫面 """
        self.strategy_settings_form = StrategySettingsForm(self, ["Test策略1"])
        self.main_content.addWidget(self.strategy_settings_form)
        self.main_content.setCurrentWidget(self.strategy_settings_form)

    def switch_view(self, new_widget):
        """ 切換主畫面 """
        self.main_content.addWidget(new_widget)
        self.main_content.setCurrentWidget(new_widget)

    def refresh_labels(self):
        """ 切換語言時更新 Log 視窗標題 """
        self.setWindowTitle(get_text(MainWindowText.TITLE))
        self.lbl_process_log.setText(get_text(MainWindowText.PROCESS_LOG_LABEL))
        self.lbl_backtest_log.setText(get_text(MainWindowText.BACKTEST_LOG_LABEL))
        self.backtest_log_display.setPlaceholderText(get_text(MainWindowText.BACKTEST_LOG_PLACEHOLDER))

    def update_process_log(self, message):
        """ 更新流程紀錄 """
        self.process_log.append(message)
        if self.current_view == "process":
            self.update_display()

    def log_message(self, message):
        """ 記錄 Log 訊息（帶時間戳） """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_messages.append(log_entry)
        if self.current_view == "log":
            self.update_display()

    def update_display(self):
        """ 更新顯示區域內容 """
        if self.current_view == "process":
            self.text_display.setPlainText("\n".join(self.process_log))
        else:
            self.text_display.setPlainText("\n".join(self.log_messages))
        
        # 自動捲到最後
        sb = self.text_display.verticalScrollBar()
        sb.setValue(sb.maximum())
        
    def closeEvent(self, event):
        """ 視窗關閉時安全終止副線程 """
        try:
            if hasattr(self, 'strategy_settings_form'):
                form = self.strategy_settings_form
                if form.worker:
                    print("🔴 偵測到策略線程正在運行，準備中斷...")
                    form.stop_strategy()
                    print("✅ 策略線程已安全終止")
        except Exception as e:
            print(f"⚠️ 關閉時出錯：{e}")

        event.accept()

    def toggle_view(self):
        """ 切換流程紀錄 / Log """
        if self.current_view == "process":
            self.current_view = "log"
            self.btn_toggle_view.setText("切換至 流程紀錄")
        else:
            self.current_view = "process"
            self.btn_toggle_view.setText("切換至 Log")

        self.update_display()

    def update_backtest_log(self, message):
        """ 更新回測 Log 視窗 """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.backtest_log_messages.append(log_entry)
        self.backtest_log_display.setPlainText("\n".join(self.backtest_log_messages))

        # 自動捲到最後
        sb = self.backtest_log_display.verticalScrollBar()
        sb.setValue(sb.maximum())
