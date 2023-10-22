import sys
import os
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QDesktopWidget, QLineEdit, QLabel, QFileDialog)
from PyQt5.QtGui import QFont, QIcon
from cv2 import imread
import matplotlib.pyplot as plt
# from main import Main

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.center()
        self.resize(1200, 500)

        btn_browse = QPushButton('Browse', self)
        btn_browse.clicked.connect(self.browse_folder)
        btn_browse.resize(70, 30)
        btn_browse.move(50, 50)

        self.line = QLabel('Path', self)
        self.line.resize(400, 30)
        self.line.move(150, 50)

        btn_start = QPushButton('Start', self)
        btn_start.clicked.connect(self.StartProgram)
        btn_start.resize(70, 30)
        btn_start.move(50, 100)
        
        self.setWindowTitle('Tokodust')
        self.setWindowIcon(QIcon('icon_3.png'))
        self.show()


    def center(self):
    
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        # self.move(qr.topLeft())

    def StartProgram(self):
        # Main()
        im = imread(self.line.text())
        plt.imshow(im)
        plt.show()

    def browse_folder(self):
        self.line.setText('')  # На случай, если в списке уже есть элементы
        self.directory = QFileDialog.getOpenFileUrl(self, "Выберите видео")
        # print(self.directory[0])

        if self.directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.line.setText(self.directory[0].toString()[7:])  # добавить файл в label
        # return self.directory


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())