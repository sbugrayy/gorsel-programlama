MAIN_STYLE = """
QMainWindow {
    background-color: #f0f0f0;
}

QMenuBar {
    background-color: #f0f0f0;
    color: black;
}

QMenuBar::item:selected {
    background-color: #3498db;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QLineEdit, QTextEdit {
    padding: 8px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: white;
}

QListWidget {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: white;
}

QLabel {
    color: #2c3e50;
    font-size: 14px;
}

QRadioButton {
    color: #2c3e50;
    font-size: 14px;
}

QGroupBox {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    margin-top: 1em;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}
""" 