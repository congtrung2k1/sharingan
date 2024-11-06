from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListView
from PyQt5.QtCore import Qt

from sharingan.module.panel.listview.CustomDragDropRecipe import CustomDragDropRecipe
from sharingan.module.panel import Ingredient


class Recipe(QWidget):
    def __init__(self, parent=None):
        super(Recipe, self).__init__(parent)
        self.list_recipe = CustomDragDropRecipe(self)
        self.list_recipe.setSelectionMode(QListView.ExtendedSelection)
        self.list_recipe.setAcceptDrops(True)
        self.list_recipe.setStyleSheet('''
                QListWidget::item {
                    border-bottom: 1px solid rgb(215, 231, 195);
                    background-color: rgb(226, 239, 218)
                }
                QListWidget::item:selected {
                    background: lightgreen;
                }
        ''')

        self.layout_banner = QHBoxLayout()
        self.lbl_recipe = QLabel('Recipe')
        self.lbl_recipe.setStyleSheet('font-weight: bold; font-size: 18pt;')
        self.btn_delete = QPushButton('Delete')
        self.btn_delete.clicked.connect(self.delete_items)
        self.btn_cook = QPushButton('Cook')
        self.btn_init = QPushButton('Init')
        self.btn_init.setShortcut("Ctrl+S")
        self.btn_init.clicked.connect(self.init)
        self.layout_banner.addWidget(self.lbl_recipe)
        self.layout_button = QHBoxLayout()
        self.layout_button.addWidget(self.btn_delete)
        self.layout_button.addWidget(self.btn_init)
        self.layout_button.addWidget(self.btn_cook)
        self.layout_button.setAlignment(Qt.AlignRight)
        self.layout_banner.addLayout(self.layout_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout_banner)
        self.layout.addWidget(self.list_recipe)
        self.setLayout(self.layout)

    def delete_items(self):
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
            Ingredient.my_list.clear()

    def init(self):
        Ingredient.my_list.clear()
        for i in range(self.list_recipe.count()):
            item_widget = self.list_recipe.item(i)
            item = self.list_recipe.itemWidget(item_widget)
            Ingredient.my_list.append(item.ingredient)
