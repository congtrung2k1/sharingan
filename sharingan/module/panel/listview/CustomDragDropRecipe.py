from PyQt5.QtCore import QDataStream, Qt
from PyQt5.QtWidgets import (QListWidget, QListWidgetItem, QAbstractItemView)
from sharingan.module.panel.listview.CustomItemAES import CustomItemAES
from sharingan.module.panel.listview.CustomItemBase64 import CustomItemBase64
from sharingan.module.panel.listview.CustomItemRC4 import CustomItemRC4
from sharingan.module.panel.listview.CustomItemRSA import CustomItemRSA
from sharingan.module.panel.listview.CustomItemSalsa20 import CustomItemSalsa20
from sharingan.module.panel.listview.CustomItemXOR import CustomItemXOR
from sharingan.module.panel.listview.CustomItemAdd import CustomItemAdd
from sharingan.module.panel.listview.CustomItemSub import CustomItemSub


class CustomDragDropRecipe(QListWidget):
    def __init__(self, parent=None):
        super(CustomDragDropRecipe, self).__init__(parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)


    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if (mime.hasText() or
                mime.hasFormat('application/x-qabstractitemmodeldatalist')):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        mime = event.mimeData()
        if mime.hasFormat('application/x-qabstractitemmodeldatalist'):
            id_algorithm = None
            stream = QDataStream(mime.data('application/x-qabstractitemmodeldatalist'))
            while not stream.atEnd():
                # Don't use row and col but must implement
                row = stream.readInt()
                col = stream.readInt()
                for data_size in range(stream.readInt()):
                    role, value = stream.readInt(), stream.readQVariant()
                    if role == Qt.DisplayRole:
                        id_algorithm = value
            # Insert item to list widget
            if id_algorithm:
                obj_algorithm = self.classify_algorithm(id_algorithm)
                list_adapter_item = QListWidgetItem()
                list_adapter_item.setSizeHint(obj_algorithm.sizeHint())
                # Get index of recipe list to insert
                # from_index = self.currentRow()
                to_index = self.count()
                ix = self.indexAt(event.pos())
                if ix.isValid():
                    to_index = ix.row()
                self.insertItem(to_index, list_adapter_item)
                self.setItemWidget(list_adapter_item, obj_algorithm)
            # Reorder by drag and drop
            else:
                # print('Reorder')
                if ((self.row(self.itemAt(event.pos())) == self.currentRow() + 1) or (self.currentRow() == self.count() - 1)):
                    event.ignore()
                else:
                    super(CustomDragDropRecipe, self).dropEvent(event)

    # def dragMoveEvent(self, event):
    #     if ((self.row(self.itemAt(event.pos())) == self.currentRow() + 1) or (self.currentRow() == self.count() - 1)):
    #         event.ignore()
    #     else:
    #         super(CustomDragDropRecipe, self).dragMoveEvent(event)

    def classify_algorithm(self, algorithm):
        switcher = {
            'AES': CustomItemAES(),
            'Base64': CustomItemBase64(),
            'RC4': CustomItemRC4(),
            'RSA': CustomItemRSA(),
            'Salsa20': CustomItemSalsa20(),
            'XOR': CustomItemXOR(),
            'Add': CustomItemAdd(),
            'Sub': CustomItemSub()
        }
        return switcher.get(algorithm, 'nothing')
