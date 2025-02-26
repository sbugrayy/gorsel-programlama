from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tab Widget Örneği")
        self.setGeometry(100, 100, 400, 300)
        self.UI()
        self.createMenuBar()
    
    def createMenuBar(self):
        # MenuBar oluşturma
        self.menuBar = QMenuBar()
        
        # File Menüsü
        fileMenu = self.menuBar.addMenu("File")
        openAction = QAction("Open", self)
        saveAction = QAction("Save", self)
        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)
        
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        
        # Edit Menüsü
        editMenu = self.menuBar.addMenu("Edit")
        cutAction = QAction("Cut", self)
        copyAction = QAction("Copy", self)
        pasteAction = QAction("Paste", self)
        
        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)
        
        # View Menüsü
        viewMenu = self.menuBar.addMenu("View")
        zoomInAction = QAction("Zoom In", self)
        zoomOutAction = QAction("Zoom Out", self)
        
        viewMenu.addAction(zoomInAction)
        viewMenu.addAction(zoomOutAction)
        
        # Help Menüsü
        helpMenu = self.menuBar.addMenu("Help")
        aboutAction = QAction("About", self)
        helpMenu.addAction(aboutAction)
        
        # MenuBar'ı ana layout'a ekleme
        self.layout().setMenuBar(self.menuBar)

    def UI(self):
        # Ana layout oluşturma
        mainLayout = QVBoxLayout()
        
        # Tab Widget oluşturma
        self.tabs = QTabWidget()
        
        # Tab'ları oluşturma
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        
        # Tab'ları TabWidget'a ekleme
        self.tabs.addTab(self.tab1, "Sekme 1")
        self.tabs.addTab(self.tab2, "Sekme 2")
        self.tabs.addTab(self.tab3, "Sekme 3")
        
        # Her bir tab için layout oluşturma
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        
        # Ana layout'a TabWidget'ı ekleme
        mainLayout.addWidget(self.tabs)
        self.setLayout(mainLayout)

    def tab1UI(self):
        layout = QVBoxLayout()
        label = QLabel("Bu birinci sekme")
        button = QPushButton("Tıkla")
        layout.addWidget(label)
        layout.addWidget(button)
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        name = QLineEdit()
        surname = QLineEdit()
        label = QLabel("Bu ikinci sekme")
        layout.addWidget(label)
        layout.addRow("İsim:", name)
        layout.addRow("Soyisim:", surname)
        self.tab2.setLayout(layout)

    def tab3UI(self):
        layout = QHBoxLayout()
        button1 = QPushButton("Sol")
        button2 = QPushButton("Sağ")
        label = QLabel("Bu üçüncü sekme")
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        self.tab3.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()