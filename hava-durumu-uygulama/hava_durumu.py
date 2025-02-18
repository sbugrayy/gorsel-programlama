import sys
import requests
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame,
                            QMenuBar, QMenu, QAction)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

class HavaDurumuUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_key = "569cff57344af0dacc069966bdf83d3a"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.icon_url = "http://openweathermap.org/img/wn/{}@2x.png"
        self.tema = "acik"  # Varsayılan tema
        
        self.setWindowTitle("Hava Durumu")
        
        # Menü bar oluşturma
        menubar = self.menuBar()
        options_menu = menubar.addMenu('Ayarlar')
        
        # Tema değiştirme alt menüsü
        tema_menu = QMenu('Tema', self)
        options_menu.addMenu(tema_menu)
        
        # Tema seçenekleri
        acik_tema = QAction('Açık Tema', self)
        acik_tema.triggered.connect(lambda: self.tema_degistir("acik"))
        tema_menu.addAction(acik_tema)
        
        koyu_tema = QAction('Koyu Tema', self)
        koyu_tema.triggered.connect(lambda: self.tema_degistir("koyu"))
        tema_menu.addAction(koyu_tema)
        
        self.tema_degistir("acik")  # Varsayılan temayı uygula
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Arama bölümü
        search_frame = QFrame()
        self.search_frame = search_frame  # Tema değişimi için referans
        search_layout = QHBoxLayout(search_frame)
        
        self.sehir_input = QLineEdit()
        self.sehir_input.setPlaceholderText("Şehir adı girin...")
        self.sehir_input.setMinimumWidth(300)
        self.sehir_input.returnPressed.connect(self.hava_durumu_getir)
        
        self.ara_button = QPushButton("Ara")
        self.ara_button.clicked.connect(self.hava_durumu_getir)
        
        search_layout.addWidget(self.sehir_input)
        search_layout.addWidget(self.ara_button)
        
        # Sonuç bölümü
        self.sonuc_frame = QFrame()
        self.sonuc_frame.setMinimumHeight(400)
        sonuc_layout = QVBoxLayout(self.sonuc_frame)
        
        # Şehir ve sıcaklık bilgisi
        self.sehir_label = QLabel()
        self.sehir_label.setAlignment(Qt.AlignCenter)
        self.sehir_label.setFont(QFont("Arial", 24, QFont.Bold))
        
        self.hava_icon = QLabel()
        self.hava_icon.setAlignment(Qt.AlignCenter)
        
        self.sicaklik_label = QLabel()
        self.sicaklik_label.setAlignment(Qt.AlignCenter)
        self.sicaklik_label.setFont(QFont("Arial", 48))
        
        self.durum_label = QLabel()
        self.durum_label.setAlignment(Qt.AlignCenter)
        self.durum_label.setFont(QFont("Arial", 18))
        
        # Detay bilgileri
        detay_frame = QFrame()
        detay_layout = QHBoxLayout(detay_frame)
        
        # Nem bilgisi
        nem_widget = QWidget()
        nem_layout = QVBoxLayout(nem_widget)
        self.nem_icon = QLabel()
        self.nem_icon.setPixmap(QPixmap("icons/humidity.png").scaled(32, 32))
        self.nem_label = QLabel()
        nem_layout.addWidget(self.nem_icon, alignment=Qt.AlignCenter)
        nem_layout.addWidget(self.nem_label, alignment=Qt.AlignCenter)
        
        # Rüzgar bilgisi
        ruzgar_widget = QWidget()
        ruzgar_layout = QVBoxLayout(ruzgar_widget)
        self.ruzgar_icon = QLabel()
        self.ruzgar_icon.setPixmap(QPixmap("icons/wind.png").scaled(32, 32))
        self.ruzgar_label = QLabel()
        ruzgar_layout.addWidget(self.ruzgar_icon, alignment=Qt.AlignCenter)
        ruzgar_layout.addWidget(self.ruzgar_label, alignment=Qt.AlignCenter)
        
        detay_layout.addWidget(nem_widget)
        detay_layout.addWidget(ruzgar_widget)
        
        # Son güncelleme
        self.guncelleme_label = QLabel()
        self.guncelleme_label.setAlignment(Qt.AlignCenter)
        
        # Widget'ları layout'a ekleme
        sonuc_layout.addWidget(self.sehir_label)
        sonuc_layout.addWidget(self.hava_icon)
        sonuc_layout.addWidget(self.sicaklik_label)
        sonuc_layout.addWidget(self.durum_label)
        sonuc_layout.addWidget(detay_frame)
        sonuc_layout.addWidget(self.guncelleme_label)
        
        # Ana layout'a ekleme
        layout.addWidget(search_frame)
        layout.addWidget(self.sonuc_frame)
        
        # Pencere boyutu
        self.setMinimumSize(500, 600)
        
        # İlk açılışta sonuç frame'ini gizle
        self.sonuc_frame.hide()
    
    def hava_durumu_getir(self):
        sehir = self.sehir_input.text()
        if not sehir:
            return
        
        params = {
            "q": sehir,
            "appid": self.api_key,
            "units": "metric",
            "lang": "tr"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                # Hava durumu ikonunu al
                icon_code = data['weather'][0]['icon']
                icon_url = self.icon_url.format(icon_code)
                icon_response = requests.get(icon_url)
                icon_pixmap = QPixmap()
                icon_pixmap.loadFromData(icon_response.content)
                self.hava_icon.setPixmap(icon_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                
                # Diğer bilgileri güncelle
                self.sehir_label.setText(f"{data['name']}, {data['sys']['country']}")
                self.sicaklik_label.setText(f"{int(data['main']['temp'])}°C")
                self.durum_label.setText(data['weather'][0]['description'].capitalize())
                self.nem_label.setText(f"Nem\n%{data['main']['humidity']}")
                self.ruzgar_label.setText(f"Rüzgar\n{data['wind']['speed']} m/s")
                
                guncelleme_zamani = datetime.fromtimestamp(data['dt']).strftime('%H:%M:%S')
                self.guncelleme_label.setText(f"Son Güncelleme: {guncelleme_zamani}")
                
                self.sonuc_frame.show()
            else:
                self.sonuc_frame.hide()
        
        except Exception as e:
            self.sonuc_frame.hide()
            print(f"Hata: {str(e)}")

    def tema_degistir(self, tema):
        self.tema = tema
        if tema == "acik":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f0f2f5;
                }
                QFrame {
                    background-color: white;
                    border-radius: 10px;
                }
                QLineEdit {
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 14px;
                    background-color: white;
                    color: #333;
                }
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
                QLabel {
                    color: #333;
                }
                QMenuBar {
                    background-color: #f0f2f5;
                    color: #333;
                }
                QMenuBar::item:selected {
                    background-color: #1a73e8;
                    color: white;
                }
                QMenu {
                    background-color: white;
                    color: #333;
                }
                QMenu::item:selected {
                    background-color: #1a73e8;
                    color: white;
                }
            """)
        else:  # koyu tema
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1f1f1f;
                }
                QFrame {
                    background-color: #2d2d2d;
                    border-radius: 10px;
                }
                QLineEdit {
                    padding: 10px;
                    border: 1px solid #3d3d3d;
                    border-radius: 5px;
                    font-size: 14px;
                    background-color: #2d2d2d;
                    color: white;
                }
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
                QLabel {
                    color: white;
                }
                QMenuBar {
                    background-color: #1f1f1f;
                    color: white;
                }
                QMenuBar::item:selected {
                    background-color: #1a73e8;
                    color: white;
                }
                QMenu {
                    background-color: #2d2d2d;
                    color: white;
                }
                QMenu::item:selected {
                    background-color: #1a73e8;
                    color: white;
                }
            """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = HavaDurumuUygulamasi()
    pencere.show()
    sys.exit(app.exec_()) 