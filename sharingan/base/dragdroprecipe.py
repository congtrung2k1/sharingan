from PySide6.QtCore import QDataStream, Qt
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView, QListView
from sharingan.base.ingredient import Ingredient
import importlib, inspect, os
import idaapi


class DragDropRecipe(QListWidget):
    def __init__(self, parent=None):
        super(DragDropRecipe, self).__init__(parent)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setSelectionMode(QListView.ExtendedSelection)

    def set_signal_toggle(self, signal_toggle):
        self.signal_toggle = signal_toggle

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if mime.hasText() or mime.hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def mimeData(self, items):
        mime = super(DragDropRecipe, self).mimeData(items)
        if items:
            item = items[0]  # Handle single item for simplicity
            text = item.text()  # Assuming the item's text is the id_algorithm
            mime.setText(text)
            # Optionally, add custom data to ensure id_algorithm is included
            mime.setData('application/x-id-algorithm', text.encode('utf-8'))
        return mime

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item is None:
            return
        row = self.row(item)
        mime = self.mimeData([item])
        drag = QDrag(self)
        drag.setMimeData(mime)
        drop_action = drag.exec(Qt.MoveAction)
        # drop outside to remove
        if drop_action != Qt.MoveAction:
            self.takeItem(row)
            print(f"Removed ingredient at row {row} (dropped outside)")

    def dropEvent(self, event):        
        if event.source() == self:
            super(DragDropRecipe, self).dropEvent(event)
            event.acceptProposedAction()
            return

        id_algorithm = None
        mime = event.mimeData()
        # Check for custom MIME type first
        if mime.hasFormat('application/x-id-algorithm'):
            data = mime.data('application/x-id-algorithm')
            if not data.isEmpty():
                id_algorithm = bytes(data).decode('utf-8')
        elif mime.hasFormat('application/x-qabstractitemmodeldatalist'):
            # Fallback to standard MIME type
            stream = QDataStream(mime.data('application/x-qabstractitemmodeldatalist'))
            while not stream.atEnd():
                row = stream.readInt32()
                col = stream.readInt32()
                item_data = {}
                for _ in range(stream.readInt32()):  # Number of data entries
                    role = stream.readInt32()
                    value = stream.readQVariant()
                    item_data[role] = value
                    if role == Qt.DisplayRole:
                        id_algorithm = value
        else:
            event.ignore()
            return

        # Insert item to list widget
        if id_algorithm:
            obj_algorithm = self.classify_algorithm(id_algorithm)
            self.insert_ingredient_recipe(obj_algorithm, event)
        else:
            # Handle reordering
            if event:
                event.ignore()

    def insert_ingredient_recipe(self, obj_algorithm, event):
        if isinstance(obj_algorithm, Ingredient):
            list_adapter_item = QListWidgetItem()
            list_adapter_item.setSizeHint(obj_algorithm.sizeHint())
            to_index = self.count()
            if event:
                ix = self.indexAt(event.pos())
                if ix.isValid():
                    to_index = ix.row()
            self.insertItem(to_index, list_adapter_item)
            self.setItemWidget(list_adapter_item, obj_algorithm)
            if event:
                event.acceptProposedAction()

    # find module to import
    def classify_algorithm(self, algorithm):
        algorithm = algorithm.lower()
        path_plugin = idaapi.get_ida_subdirs("plugins")
        for path in path_plugin:
            path_module = os.path.join(path, 'sharingan', 'ingredient', f'{algorithm}.py')
            if os.path.isfile(path_module):
                try:
                    module = importlib.import_module(f"sharingan.ingredient.{algorithm}")
                    for name_class, ingredient in inspect.getmembers(module, inspect.isclass):
                        if issubclass(ingredient, Ingredient) and ingredient != Ingredient:
                            ingre = ingredient()
                            ingre.set_signal_toggle(self.signal_toggle)
                            return ingre
                except Exception as e:
                    print(f"Error loading module {algorithm}: {path_module}")
        return None