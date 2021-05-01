import os
from os import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class PhotosApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # utawianie rozmaru
        self.setMinimumSize(800, 600)

        # znaczace zmienne
        self.SCALE_FACTOR = 1.5
        self.iterator = 0
        self.buttons = {}
        self.fileNameList = []

        self.photo = QLabel()
        self.photo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.photo.setScaledContents(True)
        self.photo.setAlignment(Qt.AlignCenter)

        self.scrollArea = QScrollArea()
        # self.scrollArea.
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollArea.setWidget(self.photo)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # ustawianie głównego layoutu i widgetu
        self.mainLayout = QVBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addLayout(self.bottomLayout)
        self._initializeControlButtons()

        # ustawienia paska aplikacji
        self.setWindowTitle("Przeglądarka zdjęć")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet(
            "QMenuBar, QMenu, QPushButton"
            "{background: black;"
            "color: red;}"
            "QScrollArea, QLabel{"
            "background: #303030;"
            "color:white;}"
            "PhotosApp, QScrollArea{"
            "background:  #303030;}")

        # stworzenie menu
        self._initializeMenuBar()
        self.show()

    # __init__()
    def _resizeImage(self, name):
        if name == "zoom+":
            # self.scrollArea.resize(self.photo.size() * self.SCALE_FACTOR)
            self.photo.resize(self.photo.size() * self.SCALE_FACTOR)
        else:
            self.photo.resize(self.photo.size() / self.SCALE_FACTOR)

    def handleButtonClick(self, event):
        name = self.sender().text()
        if name in ["<", ">"]:
            self._changeImage(name)
        elif name in ["zoom+", "zoom-"]:
            self._resizeImage(name)

    def _changeImage(self, option):
        length = self.fileNameList.__len__()
        if length != 0:
            if option == "<" and length != 0:
                if self.iterator == 0:
                    self.iterator = length - 1
                else:
                    self.iterator -= 1
                self._initializeImageScreen(self.fileNameList[self.iterator])
            elif option == ">":
                if self.iterator == length - 1:
                    self.iterator = 0
                else:
                    self.iterator += 1
                self._initializeImageScreen(self.fileNameList[self.iterator])
            else:
                self._displayMessage("Zły przycisk")
        else:
            self._displayMessage("Brak załadowanych zdjęć")

    def _initializeControlButtons(self):
        buttonNames = ["<", "zoom+", "zoom-", ">"]
        for name in buttonNames:
            self.buttons[name] = QPushButton(
                name, clicked=self.handleButtonClick)
            self.bottomLayout.addWidget(self.buttons[name])

    def _initializeImageScreen(self, imageName: str):
        pix = QPixmap(f"{self.choosenDirectory}/{imageName}")
        self.photo.resize(pix.width(), pix.height())
        self.photo.setPixmap(pix)

    def _initializeMenuBar(self):
        self.menu = QMenuBar(self)
        self.setMenuBar(self.menu)
        self.file = QMenu("Plik", self)
        self.menu.addMenu(self.file)
        self.menu.addMenu(QMenu("Widok", self))
        self.menu.addMenu(QMenu("Pomoc", self))
        self._addActionsToFileView()

    def _openFolder(self, event):
        self.fileNameList.clear()
        self.choosenDirectory = str(
            QFileDialog.getExistingDirectory(self, "Wybierz folder"))
        if self.choosenDirectory == "":
            self._displayMessage("Brak określonej ścieżki")
        else:
            self._getImagesNames()

    def _addActionsToFileView(self):
        self.openFolderAction = QAction("Wybierz folder")
        self.openFolderAction.triggered.connect(self._openFolder)
        self.file.addAction(self.openFolderAction)

    def _getImagesNames(self):
        fileNames = os.listdir(self.choosenDirectory)
        for name in fileNames:
            if name.endswith(".jpg") or name.endswith(".png"):
                self.fileNameList.append(name)
        if self.fileNameList.__len__() == 0:
            self._displayMessage("Brak zdjęć w podanej lokalizacji")
        else:
            self._initializeImageScreen(self.fileNameList[0])

    def _displayMessage(self, message: str):
        self.photo.resize(200, 200)
        self.photo.setText(message)


if __name__ == '__main__':
    appHandler = QApplication([])
    photoApp = PhotosApp()
    sys.exit(appHandler.exec_())
