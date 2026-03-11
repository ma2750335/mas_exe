style_sheet = """
    /* ========== 全域基底 ========== */
    QWidget {
        background-color: #f5f6fa;
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 14px;
        color: #2d3436;
    }

    /* ========== 標籤 ========== */
    QLabel {
        color: #2d3436;
        font-weight: 600;
        background-color: transparent;
    }

    /* ========== 按鈕 ========== */
    QPushButton {
        background-color: #e17100;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #c96500;
    }
    QPushButton:pressed {
        background-color: #a85500;
    }
    QPushButton:disabled {
        background-color: #bdc3c7;
        color: #7f8c8d;
    }

    /* ========== 輸入框 ========== */
    QLineEdit {
        background-color: #ffffff;
        border: 1.5px solid #dcdde1;
        padding: 7px 10px;
        border-radius: 5px;
        font-size: 14px;
        color: #2d3436;
        selection-background-color: #e17100;
        selection-color: #ffffff;
    }
    QLineEdit:focus {
        border: 1.5px solid #e17100;
    }

    /* ========== 文字區域 ========== */
    QTextEdit {
        background-color: #ffffff;
        border: 1.5px solid #dcdde1;
        border-radius: 5px;
        padding: 6px;
        font-size: 13px;
        color: #2d3436;
    }

    /* ========== Checkbox ========== */
    QCheckBox {
        spacing: 6px;
        color: #2d3436;
        background-color: transparent;
    }
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid #b2bec3;
        border-radius: 3px;
        background-color: #ffffff;
    }
    QCheckBox::indicator:hover {
        border-color: #e17100;
    }
    QCheckBox::indicator:checked {
        background-color: #e17100;
        border-color: #e17100;
        image: none;
    }
    QCheckBox::indicator:checked:hover {
        background-color: #c96500;
        border-color: #c96500;
    }

    /* ========== 訊息方塊 ========== */
    QMessageBox {
        background-color: #f5f6fa;
    }
    QMessageBox QLabel {
        color: #2d3436;
        font-size: 14px;
    }
    QMessageBox QPushButton {
        min-width: 70px;
    }

    /* ========== 輸入對話框 ========== */
    QInputDialog {
        background-color: #f5f6fa;
    }
    QInputDialog QLineEdit {
        min-width: 220px;
    }
"""
