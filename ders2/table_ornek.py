from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import random

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tablo Örneği")
        self.setGeometry(100, 100, 600, 400)
        self.UI()

    def UI(self):
        # Ana layout
        layout = QVBoxLayout()
        
        # Tablo oluşturma
        self.table = QTableWidget()
        self.table.setRowCount(10)  # Satır sayısı
        self.table.setColumnCount(4)  # Sütun sayısı
        
        # Sütun başlıkları
        headers = ["ID", "İsim", "Yaş", "Puan"]
        self.table.setHorizontalHeaderLabels(headers)
        
        # Rastgele veri oluşturma ve tabloya ekleme
        isimler = ["Ali", "Ayşe", "Mehmet", "Fatma", "Can", "Zeynep", "Ahmet", "Elif", "Murat", "Selin"]
        
        for row in range(10):
            # ID
            id_item = QTableWidgetItem(str(random.randint(10000, 99999)))
            self.table.setItem(row, 0, id_item)
            
            # İsim
            isim = random.choice(isimler)
            isim_item = QTableWidgetItem(isim)
            self.table.setItem(row, 1, isim_item)
            
            # Yaş
            yas = random.randint(18, 65)
            yas_item = QTableWidgetItem(str(yas))
            self.table.setItem(row, 2, yas_item)
            
            # Puan
            puan = random.randint(0, 100)
            puan_item = QTableWidgetItem(str(puan))
            self.table.setItem(row, 3, puan_item)
        
        # Butonlar
        yenile_btn = QPushButton("Verileri Yenile")
        yenile_btn.clicked.connect(self.verileri_yenile)
        
        # Layout'a widget'ları ekleme
        layout.addWidget(self.table)
        layout.addWidget(yenile_btn)
        self.setLayout(layout)

    def verileri_yenile(self):
        isimler = ["Buğra", "Ayşe", "Efe", "Aleyna", "Ömer", "Bornova", "Murat", "Ahmet", "Coşkun", "Gündüz"]
        for row in range(10):
            self.table.setItem(row, 1, QTableWidgetItem(random.choice(isimler)))
            self.table.setItem(row, 2, QTableWidgetItem(str(random.randint(18, 65))))
            self.table.setItem(row, 3, QTableWidgetItem(str(random.randint(0, 100))))

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()