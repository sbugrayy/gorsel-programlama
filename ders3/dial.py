import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QDial, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DialUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dial (Döndürme) Kontrolü")
        self.setFixedSize(400, 300)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        ana_layout = QVBoxLayout(central_widget)
        
        # Başlık etiketi
        baslik = QLabel("Ses Seviyesi Kontrolü")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setFont(QFont("Arial", 14, QFont.Bold))
        ana_layout.addWidget(baslik)
        
        # Yatay layout oluştur
        yatay_layout = QHBoxLayout()
        
        # Dial (döndürme) kontrolü
        self.dial = QDial()
        self.dial.setMinimum(0)
        self.dial.setMaximum(100)
        self.dial.setValue(50)  # Başlangıç değeri
        self.dial.setNotchesVisible(True)  # Çentikleri göster
        self.dial.setNotchTarget(5.0)  # Çentik aralığı
        self.dial.setWrapping(False)  # Tam tur dönmeyi engelle
        self.dial.valueChanged.connect(self.deger_degisti)
        yatay_layout.addWidget(self.dial)
        
        # Değer gösterge paneli
        self.deger_label = QLabel("50%")
        self.deger_label.setAlignment(Qt.AlignCenter)
        self.deger_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.deger_label.setMinimumWidth(100)
        yatay_layout.addWidget(self.deger_label)
        
        ana_layout.addLayout(yatay_layout)
        
        # Bilgi etiketi
        bilgi = QLabel("Sesi ayarlamak için döndürün")
        bilgi.setAlignment(Qt.AlignCenter)
        ana_layout.addWidget(bilgi)
        
        # Stil ayarları
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
                padding: 10px;
            }
            QDial {
                background-color: #fff;
                min-width: 200px;
                min-height: 200px;
            }
        """)
    
    def deger_degisti(self):
        # Dial değeri değiştiğinde etiketi güncelle
        deger = self.dial.value()
        self.deger_label.setText(f"{deger}%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = DialUygulamasi()
    pencere.show()
    sys.exit(app.exec_())

