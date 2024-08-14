from PyQt5.QtWidgets import QWidget, QTableWidget, QHeaderView, QVBoxLayout

from sharingan.module.core.Dispatcher import Dispatcher
from sharingan.module.panel import Ingredient


class Answer(QWidget):
    def __init__(self, parent=None):
        super(Answer, self).__init__(parent)

        self.tbl_answer = QTableWidget()
        self.tbl_answer.setColumnCount(3)
        self.tbl_answer.setRowCount(100)
        self.tbl_answer.setHorizontalHeaderLabels(['Address', 'Encrypted String', 'Answer'])
        self.tbl_answer.horizontalHeader().setStretchLastSection(True)
        self.tbl_answer.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.header = self.tbl_answer.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tbl_answer)
        self.setLayout(self.layout)

    def get_list_encrypted_msg(self):
        # Implement backend get encrypted msg here
        print('Get List!!!')

    def clear_table(self):
        self.tbl_answer.clear()
        self.tbl_answer.setHorizontalHeaderLabels(['Address', 'Encrypted String', 'Answer'])

    def fill_up(self):
        # Implement set comment to disassembly view here
        print('Fill Up!!!')

    def cook(self):
        # Decrypt string and fill up the table
        encrypted_string = []
        memory_block = []
        memory_region = []
        dispatcher = Dispatcher(Ingredient.my_list, encrypted_string, memory_block, memory_region, '')
        dispatcher.process()
