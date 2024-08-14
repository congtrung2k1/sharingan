from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QPlainTextEdit, QVBoxLayout, QCheckBox

from sharingan.module.core.Dispatcher import Dispatcher
from sharingan.module.panel import Ingredient


class Demo(QWidget):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)

        self.lbl_input = QLabel('Input')
        self.lbl_input.setStyleSheet('font-weight: bold; font-size: 18pt;')
        self.btn_clear = QPushButton('Test')
        self.btn_clear.clicked.connect(self.test_sample)
        self.chk_auto = QCheckBox('Auto')
        self.layout_demo = QHBoxLayout()
        self.layout_demo_label = QHBoxLayout()
        self.layout_demo_button = QHBoxLayout()
        self.layout_demo_label.addWidget(self.lbl_input)
        self.layout_demo_button.addWidget(self.chk_auto)
        self.layout_demo_button.addWidget(self.btn_clear)
        self.layout_demo_button.setAlignment(Qt.AlignRight)
        self.layout_demo.addLayout(self.layout_demo_label)
        self.layout_demo.addLayout(self.layout_demo_button)

        self.plt_input = QPlainTextEdit()
        self.plt_input.textChanged.connect(self.auto_decrypt)

        self.lbl_output = QLabel('Output')
        self.lbl_output.setStyleSheet('font-weight: bold; font-size: 18pt;')

        self.plt_output = QPlainTextEdit()
        self.plt_output.setReadOnly(True)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout_demo)
        self.layout.addWidget(self.plt_input)
        self.layout.addWidget(self.lbl_output)
        self.layout.addWidget(self.plt_output)
        self.setLayout(self.layout)

    def test_sample(self):
        test_case = self.plt_input.toPlainText()
        dispatcher = Dispatcher(Ingredient.my_list, [], [], [], test_case)
        result = dispatcher.test_sample()
        self.plt_output.setPlainText(result)

    def auto_decrypt(self):
        if self.chk_auto.isChecked():
            test_case = self.plt_input.toPlainText()
            dispatcher = Dispatcher(Ingredient.my_list, [], [], [], test_case)
            result = dispatcher.test_sample()
            self.plt_output.setPlainText(result)

    


