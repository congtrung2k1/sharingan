from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget, QComboBox, QHBoxLayout
from sharingan.module.core.Add import Add

class CustomItemAdd(QWidget):
    def __init__(self, parent=None):
        super(CustomItemAdd, self).__init__(parent)

        self.ingredient = Add()

        self.lbl_text = QLabel("Add")
        self.lbl_text.setStyleSheet('font-weight: bold; font-size: 14pt;  color: rgb(87, 133, 78)')

        self.led_key = QLineEdit()
        self.led_key.setPlaceholderText('Key')
        self.led_key.textChanged.connect(self.change_key)
        self.cmb_type_key = QComboBox()
        self.cmb_type_key.addItems(['Base64', 'Hex', 'UTF-8'])
        self.cmb_type_key.currentTextChanged.connect(self.change_key_type)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_text)
        self.layout_line1 = QHBoxLayout()
        self.layout_line1.addWidget(self.led_key)
        self.layout_line1.addWidget(self.cmb_type_key)
        self.layout.addLayout(self.layout_line1)
        self.setLayout(self.layout)

    def change_key_type(self, text):
        self.ingredient.set_key_type(text)

    def change_key(self, text):
        self.ingredient.set_key(text)