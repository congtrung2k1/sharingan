from PySide6.QtWidgets import QWidget, QListWidgetItem, QVBoxLayout, QAbstractItemView, QListWidget, QCheckBox, QSizePolicy
from sharingan.core.stylesmanager import ManageStyleSheet
import idaapi
import sys, os
            

class Operation(QWidget):
    def __init__(self, parent=None):
        super(Operation, self).__init__(parent)
        self.setMinimumSize(50, 100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.list_operation = QListWidget(self)
        self.list_operation.setAcceptDrops(False)
        self.list_operation.setDragEnabled(True)
        self.list_operation.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.list_operation.setObjectName('list_operation')
        self.list_operation.setStyleSheet(ManageStyleSheet.get_stylesheet())
        self.list_algorithm = self.init_list()
        for operation in self.list_algorithm:
            QListWidgetItem(operation, self.list_operation)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_operation)
        self.setLayout(self.layout)

    # load module into operation
    def init_list(self) -> list:
        path_plugin = idaapi.get_ida_subdirs("plugins")
        for path in path_plugin:
            module_dir = os.path.join(path, 'sharingan', 'ingredient')
            if os.path.isdir(module_dir):
                sys.path.append(module_dir)
                list_module = os.listdir(module_dir)
                ingrediet = []
                for module in list_module:
                    filename, ext = os.path.splitext(module)
                    if ext == '.py':
                        ingrediet.append(filename.lower().capitalize())
                return ingrediet
        return []


