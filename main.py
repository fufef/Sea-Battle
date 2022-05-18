import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from game_preparing import GamePreparing
from game import Game
from menu import Menu


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("resources/Icon.png"))
        self.setWindowTitle("Sea Battle")
        self.setFixedSize(1200, 800)

        self.central_widget = QtWidgets.QWidget(self)
        self.stacked_widget = QtWidgets.QStackedWidget(self.central_widget)
        self.stacked_widget.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.setCentralWidget(self.central_widget)

        self.stacked_widget.addWidget(Menu(self))
        self.stacked_widget.addWidget(GamePreparing(self))
        self.stacked_widget.addWidget(Game(self))

    def change_window(self, number):
        try:
            self.stacked_widget.setCurrentIndex(number)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())