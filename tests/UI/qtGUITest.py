import sys
# import PyQt6
from PyQt6.QtCore import QSize
import PyQt6.QtWidgets as QtW

# https://www.pythonguis.com/tutorials/pyqt6-signals-slots-events/
class MainWindow(QtW.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virtual Assistant")
        self.setMinimumSize(QSize(400, 580))
        # self.setFixedSize(QSize(400, 580))
        # window.setGeometry(100, 100, 280, 80)

        # openingTxt = QtW.QLabel('<h1>Welcome, awaiting input:</h1>', parent=window)

        # self.debugButton = QtW.QPushButton("Debug")

        # self.ttsOnButton = QtW.QPushButton("tts")
        # self.ttsOnButton.setCheckable(True)
        # self.ttsOnButton.setChecked(False)

        # self.speechIn = QtW.QPushButton("Talk to me!")

        # self.sendButton = QtW.QPushButton("Send Input")

        # self.inputBox = QtW.QLineEdit()

        # layout = QVBoxLayout()
        
        # container = QtW.QWidget()
        # container.setLayout(layout)

        self.button_is_checked = True
        self.button = QtW.QPushButton("Press Me!")
        self.button.setCheckable(True) # makes it so that it can toggle when clicked
        self.button.clicked.connect(self.mainButtonClicked)
        # self.button.clicked.connect(self.mainButtonToggled)
        # self.button.released.connect(self.mainButtonReleased)
        # self.button.setChecked(self.button_is_checked) # sets the initial state of the button
        
        # Set the central widget of the Window.
        self.setCentralWidget(self.button)

    def mainButtonClicked(self):
        # print("Hello!")
        self.button.setText("You already clicked me.") # change the text of the button
        self.button.setEnabled(False) # disable the button widget

        self.setWindowTitle("My Oneshot App") # change the window title

    def mainButtonToggled(self, checked):
        # print("Checked?", checked)

        self.button_is_checked = checked
        print(self.button_is_checked)

    def mainButtonReleased(self):
        self.button_is_checked = self.button.isChecked()
        print(self.button_is_checked)

if __name__ == "__main__":
    app = QtW.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # app.exec()
    sys.exit(app.exec())

# app = QtW.QApplication(sys.argv)

# # window = QtW.QWidget()
# # window = QtW.QPushButton("Push Me")
# window = QtW.QMainWindow()
# window.setWindowTitle('PyQt5 App')
# window.setGeometry(100, 100, 280, 80)
# window.move(60, 15)
# helloMsg = QtW.QLabel('<h1>Hello World!</h1>', parent=window)
# helloMsg.move(60, 15)

# window.show()

# sys.exit(app.exec())