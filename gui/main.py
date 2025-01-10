from PySide6.QtWidgets import QApplication, QMainWindow
import sys

from gui.window import Ui_MainWindow


def main():
    # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QApplication.html
    app = QApplication(sys.argv)

    # Create QWidget object
    # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QWidget.html
    window = QMainWindow()
    window_ui = Ui_MainWindow()
    window_ui.setupUi(window)


    # Show window
    window.show()

    # Application loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
