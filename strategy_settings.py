from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDialog, QCheckBox, QSizePolicy, QHBoxLayout, QInputDialog
)
from PySide6.QtGui import QPixmap, QIcon, QFont
from PySide6.QtCore import QThread, Signal, Qt, QSettings, QTimer
from i18n_strings import get_text
from i18n_strings import StrategyText, CheckText
import MetaTrader5 as mt5
import strategy
import check_symbol
import auth
import enum_setting as es
from check import get_resource_path, get_health_display, show_health_info_dialog, health_alert_if_needed, is_genai_enabled

class StrategyWorker(QThread):
    progress_signal = Signal(str)
    result_signal = Signal(object)
    backtest_log_signal = Signal(str)

    def __init__(self, account, password, server, symbol, capital=10000, volume=1, on_stop_callback=None):
        super().__init__()
        self.account = account
        self.password = password
        self.server = server
        self.symbol = symbol
        self.capital = capital
        self.volume = volume
        self.on_stop_callback = on_stop_callback

    def run(self):
        if self.isInterruptionRequested():
            return
        
        thread_safe_log = lambda m: self.progress_signal.emit(str(m))
        thread_safe_backtest_log = lambda m: self.backtest_log_signal.emit(str(m))
        res = strategy.main(
            account=self.account,
            password=self.password,
            server=self.server,
            symbol=self.symbol,
            capital=self.capital,
            volume=self.volume,
            toggle=False,
            log = thread_safe_log,
            backtest_log = thread_safe_backtest_log
        )

        if not self.isInterruptionRequested():
            self.result_signal.emit(res)


class ConfirmDialog(QDialog):
    def __init__(self, strategies, input_login_id, input_password, input_server):
        super().__init__()
        self.setWindowTitle(get_text(StrategyText.DIALOG_TITLE))
        self.resize(400, 300)
        html = get_text(StrategyText.DIALOG_HTML_PREFIX).format(account=input_login_id, server=input_server)
        self.lbl_info = QLabel(html)
        label_font = QFont("Arial", 12)
        self.lbl_info.setFont(label_font)

        self.chk_risk = QCheckBox()
        self.chk_risk.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.label_risk = QLabel(get_text(StrategyText.DIALOG_RISK_HTML))
        self.label_risk.setTextFormat(Qt.RichText)
        self.label_risk.setWordWrap(True)
        self.label_risk.setStyleSheet("font-size:13px; padding-left: 4px;")

        risk_layout = QHBoxLayout()
        risk_layout.addWidget(self.chk_risk)
        risk_layout.addWidget(self.label_risk)

        self.btn_confirm = QPushButton(get_text(StrategyText.DIALOG_CONFIRM))
        self.btn_confirm.setEnabled(False)
        self.btn_cancel = QPushButton(get_text(StrategyText.DIALOG_CANCEL))

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_info)
        layout.addLayout(risk_layout)
        layout.addWidget(self.btn_confirm)
        layout.addWidget(self.btn_cancel)
        self.setLayout(layout)

        self.chk_risk.toggled.connect(self.btn_confirm.setEnabled)
        self.btn_confirm.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)


class StrategySettingsForm(QWidget):
    def __init__(self, main_window, selected_strategies):
        super().__init__()
        self.setWindowTitle(get_text(StrategyText.TITLE))
        self.resize(500, 400)
        self.main_window = main_window
        self.selected_strategies = selected_strategies

        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap(get_resource_path("logo.png")).scaled(180, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)

        label_font = QFont("Arial", 12)

        self.lbl_health = QLabel()
        self.lbl_health.setTextFormat(Qt.RichText)
        self.lbl_health.setFont(label_font)

        self.btn_health_info = QPushButton("ⓘ")
        self.btn_health_info.setFlat(True)
        self.btn_health_info.setCursor(Qt.PointingHandCursor)
        self.btn_health_info.setFixedSize(24, 24)
        self.btn_health_info.setStyleSheet(
            "QPushButton { font-size: 16px; color: #0078D7; border: none; padding: 0; background: transparent; }"
            "QPushButton:hover { color: #005A9E; background: transparent; }"
        )
        self.btn_health_info.clicked.connect(self._show_health_info)

        health_layout = QHBoxLayout()
        health_layout.addStretch()
        health_layout.addWidget(self.lbl_health)
        health_layout.addWidget(self.btn_health_info)
        health_layout.addStretch()

        self._refresh_health_display()
        layout.addLayout(health_layout)

        self.lbl_strategy_id = QLabel()
        self.lbl_strategy_id.setTextFormat(Qt.RichText)
        self.lbl_strategy_id.setFont(label_font)

        self.lbl_symbol = QLabel()
        self.lbl_symbol.setTextFormat(Qt.RichText)
        self.lbl_symbol.setFont(label_font)

        strategy_info_layout = QHBoxLayout()
        strategy_info_layout.addStretch()
        strategy_info_layout.addWidget(self.lbl_strategy_id)
        strategy_info_layout.addSpacing(30)
        strategy_info_layout.addWidget(self.lbl_symbol)
        strategy_info_layout.addStretch()

        self._refresh_strategy_info()
        layout.addLayout(strategy_info_layout)

        self.lbl_login_id = QLabel(get_text(StrategyText.LOGIN_ID))
        self.lbl_login_id.setFont(label_font)
        self.input_login_id = QLineEdit()

        self.lbl_password = QLabel(get_text(StrategyText.PASSWORD))
        self.lbl_password.setFont(label_font)
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.lbl_server = QLabel(get_text(StrategyText.SERVER))
        self.lbl_server.setFont(label_font)
        self.input_server = QLineEdit()

        self.lbl_capital = QLabel(get_text(StrategyText.CAPITAL))
        self.lbl_capital.setFont(label_font)
        self.input_capital = QLineEdit("10000")

        self.lbl_volume = QLabel(get_text(StrategyText.VOLUME))
        self.lbl_volume.setFont(label_font)
        self.input_volume = QLineEdit("1")

        self.chk_terms = QCheckBox()
        self.chk_terms.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.label_terms = QLabel(get_text(StrategyText.TERMS_HTML))
        self.label_terms.setTextFormat(Qt.RichText)
        self.label_terms.setOpenExternalLinks(True)
        self.label_terms.setWordWrap(True)
        self.label_terms.setStyleSheet("font-size:13px; padding-left: 4px;")

        terms_layout = QHBoxLayout()
        terms_layout.addWidget(self.chk_terms)
        terms_layout.addWidget(self.label_terms)

        self.btn_start = QPushButton(get_text(StrategyText.START))
        self.btn_stop = QPushButton(get_text(StrategyText.STOP))
        self.lbl_status = QLabel(get_text(StrategyText.STATUS_IDLE))

        self.label_footer = QLabel()
        self.label_footer.setTextFormat(Qt.RichText)
        self.label_footer.setText(get_text(StrategyText.FOOTER))
        self.label_footer.setOpenExternalLinks(True)
        self.label_footer.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.lbl_login_id)
        layout.addWidget(self.input_login_id)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.lbl_server)
        layout.addWidget(self.input_server)
        capital_volume_layout = QHBoxLayout()
        capital_volume_layout.addWidget(self.lbl_capital)
        capital_volume_layout.addWidget(self.input_capital, stretch=1)
        capital_volume_layout.addSpacing(20)
        capital_volume_layout.addWidget(self.lbl_volume)
        capital_volume_layout.addWidget(self.input_volume, stretch=1)
        layout.addLayout(capital_volume_layout)
        layout.addLayout(terms_layout)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_stop)
        layout.addWidget(self.lbl_status)
        layout.addWidget(self.label_footer)
        self.setLayout(layout)

        self.btn_start.clicked.connect(self.open_confirm_dialog)
        self.btn_stop.clicked.connect(self.stop_strategy)
        self.worker = None

        self.health_monitor_timer = QTimer(self)
        self.health_monitor_timer.timeout.connect(self._check_health)

        self.main_window.update_process_log(get_text(StrategyText.LOG_OPENED))

    def _refresh_health_display(self):
        healthy = getattr(self.main_window, "healthy", None)
        label, color = get_health_display(healthy)
        if label is None:
            self.lbl_health.hide()
            self.btn_health_info.hide()
            return
        self.lbl_health.show()
        self.btn_health_info.show()
        prefix = get_text(CheckText.STRATEGY_HEALTH_LABEL)
        self.lbl_health.setText(
            f'{prefix}<span style="color:{color}; font-size:18px;">●</span> '
            f'<span style="color:{color}; font-weight:bold;">{label}</span>'
        )

    def _refresh_strategy_info(self):
        sid = getattr(self.main_window, "strategy_id", None)
        sym = getattr(self.main_window, "symbol", None)
        if not sid and not sym:
            self.lbl_strategy_id.hide()
            self.lbl_symbol.hide()
            return
        self.lbl_strategy_id.show()
        self.lbl_symbol.show()
        self.lbl_strategy_id.setText(
            f'{get_text(StrategyText.STRATEGY_ID)}<b>{sid or "-"}</b>'
        )
        self.lbl_symbol.setText(
            f'{get_text(StrategyText.SYMBOL)}<b>{sym or "-"}</b>'
        )

    def _show_health_info(self):
        show_health_info_dialog(self)

    def _check_health(self):
        healthy = auth.get_strategy_health()
        if healthy is None:
            return
        self.main_window.healthy = healthy
        self._refresh_health_display()
        health_alert_if_needed(self, healthy)

    def open_confirm_dialog(self):
        input_login_id = self.input_login_id.text()
        input_password = self.input_password.text()
        input_server = self.input_server.text()

        if not input_login_id or not input_password or not input_server:
            QMessageBox.warning(self, get_text(StrategyText.ERROR_TITLE), get_text(StrategyText.ERROR_INPUT_REQUIRED))
            return
        if not self.chk_terms.isChecked():
            QMessageBox.warning(self, get_text(StrategyText.ERROR_TITLE), get_text(StrategyText.ERROR_TERMS_REQUIRED))
            return

        self.main_window.update_process_log(get_text(StrategyText.LOG_DIALOG))
        confirm_dialog = ConfirmDialog(self.selected_strategies, input_login_id, input_password, input_server)
        if confirm_dialog.exec():
            if not self.check_trade_expert_enabled(input_login_id, input_password, input_server):
                return
            self.check_symbol(symbol="")

    def show_trade_expert_warning(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(get_text(StrategyText.ERROR_TITLE))
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(get_text(StrategyText.ERROR_TRADE_EXPERT_DISABLED_HTML))
        msg_box.exec()

    def check_trade_expert_enabled(self, account, password, server):
        try:
            if not mt5.initialize(login=int(account), password=password, server=server, timeout=6000):
                self.show_trade_expert_warning()
                return False

            terminal_info = mt5.terminal_info()
            if terminal_info is None or not terminal_info.trade_allowed:
                mt5.shutdown()
                self.show_trade_expert_warning()
                return False

            account_info = mt5.account_info()
            if account_info is None or not account_info.trade_expert:
                mt5.shutdown()
                self.show_trade_expert_warning()
                return False

            mt5.shutdown()
            return True
        except Exception as e:
            self.show_trade_expert_warning()
            return False


    def check_symbol(self,symbol=""):
        res = check_symbol.main(
            account=self.input_login_id.text(),
            password=self.input_password.text(),
            server=self.input_server.text(),
            symbol=symbol
        )
        
        settings = QSettings("mas_tech", "strategy_settings")
        
        if res:
             settings.setValue("symbol", res)
             self.start_strategy()
        else:
             text, ok = QInputDialog.getText(
                 self, 
                 get_text(StrategyText.TITLE),
                 get_text(StrategyText.ERROR_SYMBOL_NOT_FOUND)
             )
             if ok and text:
                 self.check_symbol(text)



    def start_strategy(self):
        settings = QSettings("mas_tech", "strategy_settings")
        symbol = settings.value("symbol", "")
        
        self.lbl_status.setText(get_text(StrategyText.STATUS_RUNNING))

        self.worker = StrategyWorker(
            account=self.input_login_id.text(),
            password=self.input_password.text(),
            server=self.input_server.text(),
            symbol=symbol,
            capital=float(self.input_capital.text() or 10000),
            volume=float(self.input_volume.text() or 1),
            on_stop_callback=strategy.stop_main
        )
        self.worker.progress_signal.connect(self.handle_worker_progress)
        self.worker.result_signal.connect(self.handle_worker_result)
        self.worker.backtest_log_signal.connect(self.handle_backtest_log)
        self.worker.start()

        self.main_window.update_process_log(get_text(StrategyText.LOG_STARTED))

        if is_genai_enabled():
            self._check_health()
            interval_min = es.info.health_monitor_minutes.value
            if interval_min > 0:
                self.health_monitor_timer.start(interval_min * 60 * 1000)

    def stop_strategy(self):
        self.health_monitor_timer.stop()
        if self.worker:
            if self.worker.on_stop_callback:
                self.worker.on_stop_callback()
            self.worker.wait(3000)
            if self.worker.isRunning():
                self.worker.terminate()
            self.worker = None
        self.lbl_status.setText(get_text(StrategyText.LOG_STOPPED))
        self.main_window.update_process_log(get_text(StrategyText.LOG_STOPPED))

    def handle_worker_progress(self, msg):
        self.main_window.update_process_log(f"📄 {msg}")

    def handle_worker_result(self, res):
        if res.get('status'):
            self.lbl_status.setText(get_text(StrategyText.STATUS_DONE))
            self.main_window.update_process_log(get_text(StrategyText.LOG_SUCCESS))
        else:
            self.lbl_status.setText(get_text(StrategyText.STATUS_FAILED))
            error_msg = res.get('error')
            self.main_window.update_process_log(get_text(StrategyText.LOG_FAILED).format(error=error_msg))

    def handle_backtest_log(self, msg):
        self.main_window.update_backtest_log(msg)
