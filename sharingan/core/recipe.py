from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as QtWidgets
from sharingan.base.customdragdroprecipe import CustomDragDropRecipe
from sharingan.core import stylesmanager


class Recipe(QWidget):
    def __init__(self, disassembler=None):
        super(Recipe, self).__init__()
        self.setMinimumSize(50, 100)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.disassembler = disassembler
        self.list_recipe = CustomDragDropRecipe(self)
        self.list_recipe.setObjectName('list_recipe')
        self.list_recipe.setStyleSheet(stylesmanager.get_stylesheet())

        self.btn_scan = QPushButton('Scan', self)
        self.btn_scan.clicked.connect(self.scan)
        self.btn_delete = QPushButton('Delete')
        self.btn_delete.clicked.connect(self.delete)
        self.btn_cook = QPushButton('Cook')
        self.btn_cook.clicked.connect(self.cook)
        self.btn_apply = QPushButton('Apply')
        self.btn_apply.clicked.connect(self.apply)

        self.layout_button = QHBoxLayout()
        self.layout_button.addWidget(self.btn_delete)
        self.layout_button.addWidget(self.btn_cook)
        self.layout_button.addWidget(self.btn_apply)
        self.layout_button.addWidget(self.btn_scan)
        self.layout_button.setAlignment(Qt.AlignRight)

        self.start_ea = 0x0
        self.end_ea = 0x0

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout_button)
        self.layout.addWidget(self.list_recipe)
        self.setLayout(self.layout)

    def delete(self):
        list_indexes = self.list_recipe.selectedIndexes()
        if list_indexes:
            for index in list_indexes:
                item = self.list_recipe.itemFromIndex(index)
                self.list_recipe.removeItemWidget(item)
                self.list_recipe.takeItem(index.row())
        else:
            for i in range(self.list_recipe.count()):
                item = self.list_recipe.item(i)
                self.list_recipe.removeItemWidget(item)
            self.list_recipe.clear()

    def apply(self):
        if self.disassembler and hasattr(self.disassembler, 'tab_line_edits') and self.disassembler.tab_line_edits:
            active_index = self.disassembler.currentIndex()
            if active_index != -1 and active_index < len(self.disassembler.tab_line_edits):
                input_start, input_end = self.disassembler.tab_line_edits[active_index]
                self.start_ea = int(input_start.text(), 16)
                self.end_ea = int(input_end.text(), 16)
        if self.list_recipe.count() != 0:
            for i in range(self.list_recipe.count()):
                item = self.list_recipe.item(i)
                ingredient = self.list_recipe.itemWidget(item)
                if ingredient and hasattr(ingredient, 'deobfuscate'):
                    ingredient.deobfuscate(self.start_ea, self.end_ea)

    def cook(self):
        print('Cook')

    def scan(self):
        print('Scanning')

