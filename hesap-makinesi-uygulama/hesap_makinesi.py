import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLineEdit, QGridLayout,
                            QMenuBar, QMenu, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import ctypes

class HesapMakinesi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tema = "acik"  # Varsayılan tema
        self.setWindowTitle("Hesap Makinesi")
        self.setFixedSize(300, 450)  # Sabit pencere boyutu
        
        # İkon ayarla
        self.setWindowIcon(QIcon('calculator.ico'))
        
        # Windows koyu tema ayarı
        if self.tema == "koyu":
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                int(self.winId()), 
                20, 
                ctypes.byref(ctypes.c_int(2)), 
                ctypes.sizeof(ctypes.c_int)
            )
        
        # Menü bar oluşturma
        menubar = self.menuBar()
        tema_menu = menubar.addMenu('Tema')
        
        # Tema seçenekleri
        acik_tema = QAction('Açık Tema', self)
        acik_tema.triggered.connect(lambda: self.tema_degistir("acik"))
        tema_menu.addAction(acik_tema)
        
        koyu_tema = QAction('Koyu Tema', self)
        koyu_tema.triggered.connect(lambda: self.tema_degistir("koyu"))
        tema_menu.addAction(koyu_tema)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Ekran
        self.ekran = QLineEdit()
        self.ekran.setAlignment(Qt.AlignRight)
        self.ekran.setReadOnly(True)
        self.ekran.setMaxLength(15)
        self.ekran.setMinimumHeight(50)
        layout.addWidget(self.ekran)
        
        # Tuş takımı grid'i
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        
        # Sayı ve operatör tuşları
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('÷', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('×', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
        ]
        
        for (text, row, col) in buttons:
            button = QPushButton(text)
            button.setMinimumSize(60, 60)
            if text in '÷×+-':
                button.setObjectName("operator")
            elif text == '=':
                button.setObjectName("equals")
            elif text.isdigit() or text == '.':
                button.setObjectName("number")
            button.clicked.connect(lambda checked, text=text: self.on_button_click(text))
            grid_layout.addWidget(button, row, col)
        
        # Temizle butonu
        clear_button = QPushButton('C')
        clear_button.setMinimumSize(60, 60)
        clear_button.setObjectName("clear")
        clear_button.clicked.connect(self.clear)
        layout.addWidget(clear_button)
        
        layout.addLayout(grid_layout)
        
        # Değişkenler
        self.current_number = ''
        self.previous_number = ''
        self.operator = ''
        self.result = None
        self.yeni_sayi = True
        
        # Varsayılan temayı uygula
        self.tema_degistir("acik")
    
    def tema_degistir(self, tema):
        self.tema = tema
        if tema == "acik":
            # Açık tema için pencere başlığını sıfırla
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                int(self.winId()), 
                20, 
                ctypes.byref(ctypes.c_int(0)), 
                ctypes.sizeof(ctypes.c_int)
            )
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f6fa;
                }
                QMenuBar {
                    background-color: #f5f6fa;
                    color: #2f3542;
                }
                QMenuBar::item:selected {
                    background-color: #70a1ff;
                    color: white;
                }
                QMenu {
                    background-color: #f5f6fa;
                    color: #2f3542;
                }
                QMenu::item:selected {
                    background-color: #70a1ff;
                    color: white;
                }
                QLineEdit {
                    background-color: white;
                    border: 2px solid #dfe4ea;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 24px;
                    color: #2f3542;
                    margin: 5px;
                }
                QPushButton {
                    border: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton#number {
                    background-color: white;
                    color: #2f3542;
                }
                QPushButton#number:hover {
                    background-color: #f1f2f6;
                }
                QPushButton#operator {
                    background-color: #dfe4ea;
                    color: #2f3542;
                }
                QPushButton#operator:hover {
                    background-color: #c8d6e5;
                }
                QPushButton#equals {
                    background-color: #70a1ff;
                    color: white;
                }
                QPushButton#equals:hover {
                    background-color: #5352ed;
                }
                QPushButton#clear {
                    background-color: #ff6b81;
                    color: white;
                }
                QPushButton#clear:hover {
                    background-color: #ff4757;
                }
            """)
        else:  # koyu tema
            # Koyu tema için pencere başlığını ayarla
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                int(self.winId()), 
                20, 
                ctypes.byref(ctypes.c_int(2)), 
                ctypes.sizeof(ctypes.c_int)
            )
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2f3542;
                }
                QMenuBar {
                    background-color: #2f3542;
                    color: #dfe4ea;
                }
                QMenuBar::item:selected {
                    background-color: #70a1ff;
                    color: white;
                }
                QMenu {
                    background-color: #2f3542;
                    color: #dfe4ea;
                }
                QMenu::item:selected {
                    background-color: #70a1ff;
                    color: white;
                }
                QLineEdit {
                    background-color: #353b48;
                    border: 2px solid #444853;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 24px;
                    color: white;
                    margin: 5px;
                }
                QPushButton {
                    border: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton#number {
                    background-color: #353b48;
                    color: white;
                }
                QPushButton#number:hover {
                    background-color: #444853;
                }
                QPushButton#operator {
                    background-color: #444853;
                    color: white;
                }
                QPushButton#operator:hover {
                    background-color: #535763;
                }
                QPushButton#equals {
                    background-color: #70a1ff;
                    color: white;
                }
                QPushButton#equals:hover {
                    background-color: #5352ed;
                }
                QPushButton#clear {
                    background-color: #ff6b81;
                    color: white;
                }
                QPushButton#clear:hover {
                    background-color: #ff4757;
                }
            """)
    
    def on_button_click(self, text):
        if text.isdigit() or text == '.':
            if self.yeni_sayi:
                self.ekran.clear()
                self.yeni_sayi = False
            current = self.ekran.text()
            self.ekran.setText(current + text)
        
        elif text in '÷×+-':
            self.previous_number = self.ekran.text()
            self.operator = text
            self.yeni_sayi = True
        
        elif text == '=':
            current_number = self.ekran.text()
            
            try:
                if self.operator == '+':
                    result = float(self.previous_number) + float(current_number)
                elif self.operator == '-':
                    result = float(self.previous_number) - float(current_number)
                elif self.operator == '×':
                    result = float(self.previous_number) * float(current_number)
                elif self.operator == '÷':
                    result = float(self.previous_number) / float(current_number)
                
                # Sonucu ekrana yazdır
                if result.is_integer():
                    self.ekran.setText(str(int(result)))
                else:
                    self.ekran.setText(f"{result:.2f}".rstrip('0').rstrip('.'))
                
                self.yeni_sayi = True
                
            except Exception as e:
                self.ekran.setText('Hata')
                self.yeni_sayi = True
    
    def clear(self):
        self.ekran.clear()
        self.current_number = ''
        self.previous_number = ''
        self.operator = ''
        self.result = None
        self.yeni_sayi = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hesap_makinesi = HesapMakinesi()
    hesap_makinesi.show()
    sys.exit(app.exec_()) 