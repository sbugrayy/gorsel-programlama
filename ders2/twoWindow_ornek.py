from PyQt5.QtWidgets import *
import sys

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İkinci Pencere")
        self.setGeometry(450, 100, 300, 200)
        self.UI()

    def UI(self):
        layout = QVBoxLayout()
        label = QLabel("Hoşgeldiniz! Bu ikinci pencere.")
        backButton = QPushButton("Ana Pencereye Dön")
        backButton.clicked.connect(self.close)  
        
        layout.addWidget(label)
        layout.addWidget(backButton)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ana Pencere")
        self.setGeometry(100, 100, 300, 200)
        self.UI()

    def UI(self):
        layout = QVBoxLayout()
        label = QLabel("Ana Pencere")
        self.openButton = QPushButton("İkinci Pencereyi Aç")
        self.openButton.clicked.connect(self.openSecondWindow)
        
        layout.addWidget(label)
        layout.addWidget(self.openButton)
        self.setLayout(layout)

    def openSecondWindow(self):
        self.second = SecondWindow()
        self.second.show()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()