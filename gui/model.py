import pickle

from PySide6.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    Qt,
    QMimeData,
    QByteArray,
    QDataStream,
    QIODevice,
)

MIMETYPE = "application/x-json-treeview-item"


class TreeItem:
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class TreeModel(QAbstractItemModel):
    def __init__(self, headers, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(headers)
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsDropEnabled
        return super().flags(index) | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def setupModelData(self, data, parent):
        for item in data:
            parent.appendChild(TreeItem(item, parent))

    def mimeTypes(self):
        return [MIMETYPE]

    def mimeData(self, indexes):
        mimeData = QMimeData()

        data = [
            index.internalPointer().itemData
            for index in indexes
            if index.isValid() and index.column() == 0
        ]

        pickled_data = pickle.dumps(data)

        mimeData.setData(MIMETYPE, pickled_data)
        return mimeData

    def dropMimeData(self, data, action, row, column, parent):
        if action == Qt.IgnoreAction:
            return True
        if not data.hasFormat(MIMETYPE):
            return False

        encodedData = data.data(MIMETYPE).data()
        newItems = pickle.loads(encodedData)

        parentItem = self.rootItem if not parent.isValid() else parent.internalPointer()

        if row == -1:
            row = parentItem.childCount()

        for item in newItems:
            parentItem.childItems.insert(row, TreeItem(item, parentItem))
            row += 1

        self.layoutChanged.emit()
        return True

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction
