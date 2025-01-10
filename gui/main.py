from PySide6.QtWidgets import QApplication, QMainWindow
import sys

from gui.window import Ui_MainWindow
from gui.model import TreeModel, TreeItem


def main():
    # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QApplication.html
    app = QApplication(sys.argv)

    # Create QWidget object
    # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QWidget.html
    window = QMainWindow()
    window_ui = Ui_MainWindow()
    window_ui.setupUi(window)

    headers = ["Column 1", "Number"]
    data = [
        ["Item 1", 1, [["SubItem 1.1", 1.1], ["SubItem 1.2", 1.2]]],
        ["Item 2", 2, [["SubItem 2.1", 2.1]]],
        ["Item 3", 3],
    ]

    def add_items(parent, elements):
        for element in elements:
            item = TreeItem(element[:2], parent)
            parent.appendChild(item)
            if len(element) > 2:
                add_items(item, element[2])

    root_item = TreeItem(headers)
    add_items(root_item, data)

    model = TreeModel(headers, [])
    model.rootItem = root_item
    window_ui.treeView.setModel(model)

    # Show window
    window.show()

    # Application loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
