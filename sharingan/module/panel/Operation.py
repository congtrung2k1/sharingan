from PyQt5.QtWidgets import QWidget, QListWidgetItem, QVBoxLayout, QAbstractItemView, QListWidget


class Operation(QWidget):
    def __init__(self, parent=None):
        super(Operation, self).__init__(parent)

        self.list_operation = QListWidget(self)
        self.list_operation.setAcceptDrops(False)
        self.list_operation.setDragEnabled(True)
        self.list_operation.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)

        self.list_operation.setStyleSheet('''
                QWidget {
                    font-size: 22pt;
                    color: rgb(77, 134, 169);
                }
                QListWidget::item:selected {
                    background: rgb(216, 231, 241);
                }
                QListWidget::item {
                    border-bottom: 1px solid rgb(194, 231, 240);
                    background-color: #dcecf6;
                    padding: 10px;
                }
        ''')
        
        self.list_algorithm = ['AES', 'Salsa20', 'RSA', 'RC4', 'Base64', 'XOR', 'Add', 'Sub', 'Equation', 'Emulation']
        for operation in self.list_algorithm:
            QListWidgetItem(operation, self.list_operation)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_operation)
        self.setLayout(self.layout)
