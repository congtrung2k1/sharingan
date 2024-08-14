from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMainWindow

from sharingan.module.panel import Ingredient
from sharingan.module.panel.Answer import Answer
from sharingan.module.panel.Operation import Operation
from sharingan.module.panel.Recipe import Recipe
from sharingan.module.panel.Config import Config
from sharingan.module.panel.Demo import Demo


class MainWindow(QMainWindow):
    def __init__(self, objEP, parent=None):
        super(MainWindow, self).__init__(parent)

        self.list_operation = Operation()
        self.list_recipe = Recipe()
        self.demo = Demo()
        self.list_config = Config()
        self.answers = Answer()
        Ingredient.init()

        self.layout_recipe = QHBoxLayout()
        self.layout_recipe.addWidget(self.list_operation, stretch=1)
        self.layout_recipe.addWidget(self.list_recipe, stretch=3)
        self.layout_recipe.addWidget(self.demo, stretch=2)
        self.layout_recipe.addWidget(self.list_config, stretch=1)

        self.list_config.btn_get_list.clicked.connect(self.answers.get_list_encrypted_msg)
        self.list_config.btn_clear.clicked.connect(self.answers.clear_table)
        self.list_config.btn_fill_up.clicked.connect(self.answers.fill_up)
        self.list_recipe.btn_cook.clicked.connect(self.answers.cook)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.layout_recipe)
        self.main_layout.addWidget(self.answers)
        objEP.parent.setLayout(self.main_layout)

