import sys
import json
import os
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from styles import MAIN_STYLE

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('soru_bankasi.ui', self)
        self.setStyleSheet(MAIN_STYLE)

        # Video
        self.video_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.videoLabel.setLayout(QtWidgets.QVBoxLayout())
        self.videoLabel.layout().addWidget(self.video_widget)
        self.video_player.setVideoOutput(self.video_widget)
        self.video_player.setMedia(QMediaContent(QUrl.fromLocalFile("login_video.mp4")))
        self.video_player.play()

        # Menü bağlantıları
        self.actionYeniSoruEkle.triggered.connect(self.yeni_soru_ekle)
        self.actionSoruSec.triggered.connect(self.soru_sec)

        self.soru_bankasi_dosyasi = "soru_bankasi.json"
        self.sorulari_yukle()

    def sorulari_yukle(self):
        if os.path.exists(self.soru_bankasi_dosyasi):
            with open(self.soru_bankasi_dosyasi, 'r', encoding='utf-8') as f:
                self.sorular = json.load(f)
        else:
            self.sorular = []

    def sorulari_kaydet(self):
        with open(self.soru_bankasi_dosyasi, 'w', encoding='utf-8') as f:
            json.dump(self.sorular, f, ensure_ascii=False, indent=4)

    def yeni_soru_ekle(self):
        dialog = YeniSoruDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.sorulari_kaydet()

    def soru_sec(self):
        dialog = SoruSecimDialog(self)
        dialog.exec_()

class YeniSoruDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('yeni_soru.ui', self)
        self.setStyleSheet(MAIN_STYLE)
        self.parent = parent

        self.ekleButton.clicked.connect(self.soru_ekle)
        self.sorulari_listele()

    def sorulari_listele(self):
        self.soruListesi.clear()
        for soru in self.parent.sorular:
            self.soruListesi.addItem(f"Soru: {soru['soru']}")

    def soru_ekle(self):
        soru = self.soruText.toPlainText()
        yanitlar = [
            self.yanit1.text(),
            self.yanit2.text(),
            self.yanit3.text(),
            self.yanit4.text(),
            self.yanit5.text()
        ]

        dogru_yanit = None
        for i, radio in enumerate([self.radioButton1, self.radioButton2,
                                 self.radioButton3, self.radioButton4,
                                 self.radioButton5]):
            if radio.isChecked():
                dogru_yanit = i
                break

        if not soru or not all(yanitlar) or dogru_yanit is None:
            QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun ve doğru yanıtı seçin!")
            return

        yeni_soru = {
            "soru": soru,
            "yanitlar": yanitlar,
            "dogru_yanit": dogru_yanit
        }

        self.parent.sorular.append(yeni_soru)
        self.sorulari_listele()

        # Formu temizle
        self.soruText.clear()
        for yanit in [self.yanit1, self.yanit2, self.yanit3, self.yanit4, self.yanit5]:
            yanit.clear()
        for radio in [self.radioButton1, self.radioButton2, self.radioButton3,
                     self.radioButton4, self.radioButton5]:
            radio.setChecked(False)

class SoruSecimDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('soru_secimi.ui', self)
        self.setStyleSheet(MAIN_STYLE)
        self.parent = parent

        self.dosyaSecButton.clicked.connect(self.dosya_sec)
        self.yazdirButton.clicked.connect(self.yazdir)
        self.sorulari_listele()

    def sorulari_listele(self):
        self.soruListesi.clear()
        for i, soru in enumerate(self.parent.sorular):
            item = QtWidgets.QListWidgetItem()
            item.setText(f"Soru {i+1}: {soru['soru']}\nYanıtlar: {', '.join(soru['yanitlar'])}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.soruListesi.addItem(item)

    def dosya_sec(self):
        dosya, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Dosya Seç", "", "Text Files (*.txt);;All Files (*)"
        )
        if dosya:
            self.hedef_dosya = dosya

    def yazdir(self):
        if not hasattr(self, 'hedef_dosya'):
            QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen önce hedef dosyayı seçin!")
            return

        secili_sorular = []
        for i in range(self.soruListesi.count()):
            item = self.soruListesi.item(i)
            if item.checkState() == Qt.Checked:
                secili_sorular.append(self.parent.sorular[i])

        if not secili_sorular:
            QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen en az bir soru seçin!")
            return

        with open(self.hedef_dosya, 'w', encoding='utf-8') as f:
            for i, soru in enumerate(secili_sorular, 1):
                f.write(f"Soru {i}:\n{soru['soru']}\n\n")
                for j, yanit in enumerate(soru['yanitlar']):
                    f.write(f"{chr(65+j)}) {yanit}\n")
                f.write(f"\nDoğru Yanıt: {chr(65+soru['dogru_yanit'])}\n\n")
                f.write("-" * 50 + "\n\n")

        QtWidgets.QMessageBox.information(self, "Başarılı", "Sorular başarıyla yazdırıldı!")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())