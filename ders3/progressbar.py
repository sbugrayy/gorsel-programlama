import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QProgressBar, QLabel, QPushButton)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont

class YuklemePenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fotoğraf Yükleme")
        self.setFixedSize(600, 500)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.ana_layout = QVBoxLayout(central_widget)
        
        # Başlık etiketi
        baslik = QLabel("Fotoğraf Yükleniyor...")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setFont(QFont("Arial", 14, QFont.Bold))
        self.ana_layout.addWidget(baslik)
        
        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ccc;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)
        self.ana_layout.addWidget(self.progress)
        
        # Yüzde etiketi
        self.yuzde_label = QLabel("0%")
        self.yuzde_label.setAlignment(Qt.AlignCenter)
        self.yuzde_label.setFont(QFont("Arial", 12))
        self.ana_layout.addWidget(self.yuzde_label)
        
        # Fotoğraf etiketi
        self.foto_label = QLabel()
        self.foto_label.setAlignment(Qt.AlignCenter)
        self.ana_layout.addWidget(self.foto_label)
        
        # Yeniden Başlat butonu (başlangıçta gizli)
        self.yenile_buton = QPushButton("Yeniden Başlat")
        self.yenile_buton.clicked.connect(self.yeniden_baslat)
        self.yenile_buton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.yenile_buton.hide()
        self.ana_layout.addWidget(self.yenile_buton)
        
        # Timer ayarları
        self.timer = QTimer()
        self.timer.timeout.connect(self.guncelle_progress)
        self.timer.start(50)  # Her 50 milisaniyede bir güncelle
        
        # Stil ayarları
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
                padding: 10px;
            }
        """)
    
    def guncelle_progress(self):
        deger = self.progress.value()
        if deger < 100:
            self.progress.setValue(deger + 1)
            self.yuzde_label.setText(f"{deger + 1}%")
        else:
            self.timer.stop()
            self.yukleme_tamamlandi()
    
    def yukleme_tamamlandi(self):
        # Başlığı güncelle
        self.findChild(QLabel).setText("Fotoğraf Yüklendi!")
        
        # Progress bar ve yüzde etiketini gizle
        self.progress.hide()
        self.yuzde_label.hide()
        
        try:
            # Fotoğrafı yükle ve göster
            dosya_yolu = "ders3/resim.png"  # Tam dosya yolu
            pixmap = QPixmap(dosya_yolu)
            
            if pixmap.isNull():
                raise Exception("Fotoğraf yüklenemedi!")
                
            # Fotoğrafı pencereye sığacak şekilde yeniden boyutlandır
            scaled_pixmap = pixmap.scaled(550, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.foto_label.setPixmap(scaled_pixmap)
            
            # Yeniden başlat butonunu göster
            self.yenile_buton.show()
            
        except Exception as e:
            # Hata durumunda kullanıcıya bilgi ver
            self.findChild(QLabel).setText("Hata: Fotoğraf yüklenemedi!")
            self.foto_label.setText("Lütfen 'resim.png' dosyasının\nders3 klasöründe olduğundan emin olun.")
            self.foto_label.setStyleSheet("QLabel { color: red; }")
            self.yenile_buton.show()
    
    def yeniden_baslat(self):
        # Progress bar ve yüzde etiketini göster
        self.progress.show()
        self.yuzde_label.show()
        
        # Değerleri sıfırla
        self.progress.setValue(0)
        self.yuzde_label.setText("0%")
        
        # Başlığı güncelle
        self.findChild(QLabel).setText("Fotoğraf Yükleniyor...")
        
        # Fotoğrafı temizle
        self.foto_label.clear()
        
        # Butonu gizle
        self.yenile_buton.hide()
        
        # Timer'ı yeniden başlat
        self.timer.start(50)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = YuklemePenceresi()
    pencere.show()
    sys.exit(app.exec_())
