import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                          QLineEdit, QCompleter, QLabel)
from PyQt5.QtCore import Qt

class OtomatikTamamlama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Otomatik Tamamlama Örneği")
        self.setFixedSize(400, 200)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Başlık etiketi
        baslik = QLabel("Bir şehir adı yazın:")
        baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(baslik)
        
        # Şehir listesi
        sehirler = [
            "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara",
            "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl",
            "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum",
            "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum",
            "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay",
            "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri",
            "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya",
            "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir",
            "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop",
            "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa",
            "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman",
            "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova",
            "Karabük", "Kilis", "Osmaniye", "Düzce"
        ]
        
        # Metin kutusu ve otomatik tamamlayıcı
        self.metin_kutusu = QLineEdit()
        self.metin_kutusu.setPlaceholderText("Şehir adı girin...")
        
        # Otomatik tamamlayıcı ayarları
        tamamlayici = QCompleter(sehirler)
        tamamlayici.setCaseSensitivity(Qt.CaseInsensitive)  # Büyük/küçük harf duyarsız
        self.metin_kutusu.setCompleter(tamamlayici)
        
        # Stil ayarları
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                color: #333;
                padding: 10px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin: 10px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        
        layout.addWidget(self.metin_kutusu)
        layout.addStretch()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = OtomatikTamamlama()
    pencere.show()
    sys.exit(app.exec_()) 