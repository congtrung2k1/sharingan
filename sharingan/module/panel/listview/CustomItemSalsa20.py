from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, QSpinBox, QHBoxLayout, QVBoxLayout, QComboBox
from sharingan.module.core.Salsa20 import Salsa20

class CustomItemSalsa20(QWidget):
    def __init__(self, parent=None):
        super(CustomItemSalsa20, self).__init__(parent)

        self.ingredient = Salsa20()

        self.lbl_text = QLabel("Salsa20")
        self.lbl_text.setStyleSheet('font-weight: bold; font-size: 14pt;  color: rgb(87, 133, 78)')

        self.led_key = QLineEdit()
        self.led_key.setPlaceholderText('Key')
        self.led_key.textChanged.connect(self.change_key)
        self.cmb_key_type = QComboBox()
        self.cmb_key_type.addItems(['Base64', 'Hex', 'UTF-8'])
        self.cmb_key_type.currentTextChanged.connect(self.change_key_type)

        self.led_nonce = QLineEdit()
        self.led_nonce.setPlaceholderText('Nonce')
        self.led_nonce.textChanged.connect(self.change_nonce)
        self.cmb_nonce_type = QComboBox()
        self.cmb_nonce_type.addItems(['Base64', 'Hex', 'UTF-8'])
        self.cmb_nonce_type.currentTextChanged.connect(self.change_nonce_type)

        self.sp_counter = QSpinBox(minimum=0, maximum=100, value=0)
        self.sp_counter.valueChanged.connect(self.change_counter)

        self.led_rounds = QLineEdit()
        self.led_rounds.setPlaceholderText('Rounds')
        self.led_rounds.textChanged.connect(self.change_rounds)

        self.layout_line1 = QHBoxLayout()
        self.layout_line1.addWidget(self.led_key)
        self.layout_line1.addWidget(self.cmb_key_type)

        self.layout_line2 = QHBoxLayout()
        self.layout_line2.addWidget(self.led_nonce)
        self.layout_line2.addWidget(self.cmb_nonce_type)

        self.layout_line3 = QHBoxLayout()
        self.layout_line3.addWidget(self.sp_counter)
        self.layout_line3.addWidget(self.led_rounds)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_text)
        self.layout.addLayout(self.layout_line1)
        self.layout.addLayout(self.layout_line2)
        self.layout.addLayout(self.layout_line3)
        self.setLayout(self.layout)

    def change_key(self, text):
        self.ingredient.set_key(text)

    def change_nonce(self, text):
        self.ingredient.set_nonce(text)

    def change_counter(self):
        self.ingredient.set_counter(self.sp_counter.value())

    def change_rounds(self, text):
        self.ingredient.set_rounds(text)

    def change_key_type(self, text):
        self.ingredient.set_key_type(text)

    def change_nonce_type(self, text):
        self.ingredient.set_nonce_type(text)