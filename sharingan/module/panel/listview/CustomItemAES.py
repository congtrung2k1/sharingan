from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QPushButton
from sharingan.module.core.AES import AES

class CustomItemAES(QWidget):
    def __init__(self):
        super(CustomItemAES, self).__init__()

        self.ingredient = AES()

        self.lbl_text = QLabel("AES")
        self.btn_delete = QPushButton("Delete")
        self.lbl_text.setStyleSheet('font-weight: bold; font-size: 14pt;  color: rgb(87, 133, 78)')

        self.led_key = QLineEdit()
        self.led_key.setPlaceholderText('Key')
        self.led_key.textChanged.connect(self.change_key)
        self.cmb_type_key = QComboBox()
        self.cmb_type_key.addItems(['Base64', 'Hex', 'UTF-8'])
        self.cmb_type_key.currentTextChanged.connect(self.change_type_key)

        self.led_iv = QLineEdit()
        self.led_iv.setPlaceholderText('IV')
        self.led_iv.textChanged.connect(self.change_iv)
        self.cmb_type_iv = QComboBox()
        self.cmb_type_iv.addItems(['Base64', 'Hex', 'UTF-8'])
        self.cmb_type_iv.currentTextChanged.connect(self.change_type_iv)

        self.cmb_mode = QComboBox()
        self.cmb_mode.addItems(['MODE_EBC', 'MODE_CBC', 'MODE_GCM'])
        self.cmb_mode.currentTextChanged.connect(self.change_mode)

        self.layout_line1 = QHBoxLayout()
        self.layout_line1.addWidget(self.led_key)
        self.layout_line1.addWidget(self.cmb_type_key)
        self.layout_line2 = QHBoxLayout()
        self.layout_line2.addWidget(self.led_iv)
        self.layout_line2.addWidget(self.cmb_type_iv)
        self.layout_line2.addWidget(self.cmb_mode)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_text)
        self.layout.addLayout(self.layout_line1)
        self.layout.addLayout(self.layout_line2)
        self.setLayout(self.layout)

    def change_key(self, text):
        self.ingredient.set_key(text)

    def change_iv(self, text):
        self.ingredient.set_iv(text)

    def change_mode(self, text):
        self.ingredient.set_mode(text)

    def change_type_iv(self, text):
        self.ingredient.set_type_iv(text)

    def change_type_key(self, text):
        self.ingredient.set_type_key(text)
