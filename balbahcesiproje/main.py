import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QListWidget, QMessageBox, QCheckBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

def veritabani_baglan():
    return sqlite3.connect('adres.db')

def veritabani_olustur():
    conn = veritabani_baglan()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tc_kimlik TEXT UNIQUE,
                        sifre TEXT
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS adresler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tc_kimlik TEXT,
                        sehir TEXT,
                        ilce TEXT,
                        bina_adi TEXT,
                        adres TEXT,
                        telefon TEXT,
                        FOREIGN KEY(tc_kimlik) REFERENCES kullanicilar(tc_kimlik)
                      )''')
    conn.commit()
    conn.close()

class GirişFormu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Giriş / Kayıt')
        self.setGeometry(0, 0, 360, 640)

        self.ad_label = QLabel('Ad Soyad:')
        self.ad_input = QLineEdit()

        self.email_label = QLabel('E-Posta:')
        self.email_input = QLineEdit()

        self.telefon_label = QLabel('Telefon:')
        self.telefon_input = QLineEdit()

        self.tc_label = QLabel('TC Kimlik No:')
        self.tc_input = QLineEdit()

        self.sifre_label = QLabel('Şifre:')
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)

        self.dogruluk_checkbox = QCheckBox('Bilgilerimin doğruluğundan eminim.')

        self.giris_button = QPushButton('Giriş Yap')
        self.kayit_button = QPushButton('Kayıt Ol')

        self.giris_button.clicked.connect(self.giris_yap)
        self.kayit_button.clicked.connect(self.kayit_ol)

        layout = QVBoxLayout()
        layout.addWidget(self.ad_label)
        layout.addWidget(self.ad_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.telefon_label)
        layout.addWidget(self.telefon_input)
        layout.addWidget(self.tc_label)
        layout.addWidget(self.tc_input)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_input)
        layout.addWidget(self.dogruluk_checkbox)
        layout.addWidget(self.giris_button)
        layout.addWidget(self.kayit_button)

        self.setLayout(layout)

    def giris_yap(self):
        tc = self.tc_input.text()
        sifre = self.sifre_input.text()

        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE tc_kimlik = ? AND sifre = ?", (tc, sifre))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.hosgeldiniz(user[1])
        else:
            self.hata_mesaji('Giriş bilgileri hatalı!')

    def kayit_ol(self):
        if not self.dogruluk_checkbox.isChecked():
            self.hata_mesaji("Lütfen bilgilerin doğruluğunu onaylayınız.")
            return

        tc = self.tc_input.text()
        sifre = self.sifre_input.text()

        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE tc_kimlik = ?", (tc,))
        user = cursor.fetchone()

        if user:
            self.hata_mesaji('Bu TC ile kayıtlı bir kullanıcı var!')
        else:
            cursor.execute("INSERT INTO kullanicilar (tc_kimlik, sifre) VALUES (?, ?)", (tc, sifre))
            conn.commit()
            conn.close()
            self.hosgeldiniz(tc)

    def hosgeldiniz(self, tc):
        self.close()
        self.adres_durumu_formu = AdresDurumuFormu(tc)
        self.adres_durumu_formu.show()

    def hata_mesaji(self, mesaj):
        QMessageBox.warning(self, 'Hata', mesaj)

class AdresDurumuFormu(QWidget):
    def __init__(self, tc):
        super().__init__()
        self.tc = tc
        self.adresler = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Adres Durumu')
        self.setGeometry(0, 0, 360, 640)

        self.adres_liste_widget = QListWidget()

        self.sirala_button = QPushButton('Adres Sıralama')
        self.sirala_button.clicked.connect(self.sirala)

        self.deprem_button = QPushButton('Deprem Oldu')
        self.deprem_button.clicked.connect(self.deprem_oldu)

        self.adres_ekle_button = QPushButton('Adres Ekle')
        self.adres_ekle_button.clicked.connect(self.adres_ekle)

        self.adresleri_listele_button = QPushButton('Adresleri Listele')
        self.adresleri_listele_button.clicked.connect(self.adresleri_guncelle)

        layout = QVBoxLayout()
        layout.addWidget(self.adres_liste_widget)
        layout.addWidget(self.sirala_button)
        layout.addWidget(self.deprem_button)
        layout.addWidget(self.adres_ekle_button)
        layout.addWidget(self.adresleri_listele_button)

        self.setLayout(layout)
        self.adresleri_guncelle()

    def adresleri_guncelle(self):
        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT sehir, adres, bina_adi FROM adresler WHERE tc_kimlik = ?", (self.tc,))
        self.adresler = cursor.fetchall()
        conn.close()

        self.adres_liste_widget.clear()
        for adres in self.adresler:
            self.adres_liste_widget.addItem(f"{adres[0]} - {adres[1]} ({adres[2]})")

    def sirala(self):
        sorted_items = sorted(self.adresler, key=lambda x: x[2], reverse=True)
        self.adres_liste_widget.clear()
        for adres in sorted_items:
            self.adres_liste_widget.addItem(f"{adres[0]} - {adres[1]} ({adres[2]})")

    def adres_ekle(self):
        self.adres_ekleme_formu = AdresEkleFormu(self.tc, self)
        self.adres_ekleme_formu.show()

    def deprem_oldu(self):
        cevap = QMessageBox.question(self, 'Deprem Durumu', 'Güvende misiniz?', QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            QMessageBox.warning(self, 'Durum', 'Güvenli adres seçildi!')
        else:
            QMessageBox.warning33z(self, 'Durum', 'Durumunuz bildirildi. Uygulama kapanıyor.')
            self.close()

class AdresEkleFormu(QWidget):
    def __init__(self, tc, parent_form=None):
        super().__init__()
        self.tc = tc
        self.parent_form = parent_form
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Adres Ekleme')
        self.setGeometry(0, 0, 360, 640)

        self.sehir_input = QLineEdit()
        self.ilce_input = QLineEdit()
        self.bina_adi_input = QLineEdit()
        self.adres_input = QLineEdit()
        self.telefon_input = QLineEdit()

        self.kaydet_button = QPushButton('Kaydet')
        self.baska_adres_ekle_button = QPushButton('Başka Adres Ekle')
        self.adreslerimi_listele_button = QPushButton('Adreslerimi Listele')

        self.kaydet_button.clicked.connect(self.adres_kaydet)
        self.baska_adres_ekle_button.clicked.connect(self.baska_adres_ekle)
        self.adreslerimi_listele_button.clicked.connect(self.adresleri_listele)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Şehir:'))
        layout.addWidget(self.sehir_input)
        layout.addWidget(QLabel('İlçe:'))
        layout.addWidget(self.ilce_input)
        layout.addWidget(QLabel('Bina Adı:'))
        layout.addWidget(self.bina_adi_input)
        layout.addWidget(QLabel('Adres:'))
        layout.addWidget(self.adres_input)
        layout.addWidget(QLabel('Telefon:'))
        layout.addWidget(self.telefon_input)
        layout.addWidget(self.kaydet_button)
        layout.addWidget(self.baska_adres_ekle_button)
        layout.addWidget(self.adreslerimi_listele_button)

        self.setLayout(layout)

    def adres_kaydet(self):
        sehir = self.sehir_input.text()
        ilce = self.ilce_input.text()
        bina_adi = self.bina_adi_input.text()
        adres = self.adres_input.text()
        telefon = self.telefon_input.text()

        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO adresler (tc_kimlik, sehir, ilce, bina_adi, adres, telefon) VALUES (?, ?, ?, ?, ?, ?)",
                       (self.tc, sehir, ilce, bina_adi, adres, telefon))
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Adres Eklendi', 'Adres başarıyla kaydedildi!')
        if self.parent_form:
            self.parent_form.adresleri_guncelle()

    def baska_adres_ekle(self):
        self.sehir_input.clear()
        self.ilce_input.clear()
        self.bina_adi_input.clear()
        self.adres_input.clear()
        self.telefon_input.clear()

    def adresleri_listele(self):
        if self.parent_form:
            self.parent_form.adresleri_guncelle()
        self.close()

class KapakSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Deprem Uygulaması")
        self.setGeometry(0, 0, 360, 640)

        self.resim_label = QLabel()
        # pixmap = QPixmap("C:/Users/AYŞENUR/OneDrive/Masaüstü/Visual-Programming-PyQT-Lecture-Notes/DKU/kapakfoto.png")
        # self.resim_label.setPixmap(pixmap.scaled(550, 350, Qt.KeepAspectRatio))
        self.resim_label.setAlignment(Qt.AlignCenter)

        self.hosgeldiniz_label = QLabel("Hoşgeldiniz")
        self.hosgeldiniz_label.setAlignment(Qt.AlignCenter)
        self.hosgeldiniz_label.setFont(QFont("Arial", 16))

        self.devam_button = QPushButton("Devam Et")
        self.devam_button.clicked.connect(self.devam_et)

        layout = QVBoxLayout()
        layout.addWidget(self.resim_label)
        layout.addWidget(self.hosgeldiniz_label)
        layout.addWidget(self.devam_button)

        self.setLayout(layout)

        self.setStyleSheet("""
               QLabel {
                font-family: Arial;
                font-size: 25px;
            }              
            QLineEdit {
                padding: 8px;
                border: 1px solid #aaa;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton {
                background-color: "blue;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: "blue";
            }
        """)

    def devam_et(self):
        self.close()
        self.giris_formu = GirişFormu()
        self.giris_formu.show()

def main():
    veritabani_olustur()
    app = QApplication(sys.argv)
    kapak = KapakSayfasi()
    kapak.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()