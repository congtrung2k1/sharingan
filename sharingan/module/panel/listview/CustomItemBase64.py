from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QComboBox, QHBoxLayout
from sharingan.module.core.Base64 import Base64

class CustomItemBase64(QWidget):
    def __init__(self, parent=None):
        super(CustomItemBase64, self).__init__(parent)

        self.ingredient = Base64()

        self.lbl_text = QLabel('Base64')
        self.lbl_text.setStyleSheet('font-weight: bold; font-size: 14pt; color: rgb(87, 133, 78)')

        self.led_alphabet = QLineEdit()
        self.led_alphabet.setPlaceholderText('Alphabet')
        self.led_alphabet.textChanged.connect(self.change_alphabet)
        self.led_alphabet.setText('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
        self.led_alphabet.setReadOnly(True)

        self.cmb_type_alphabet = QComboBox()
        self.cmb_type_alphabet.addItems(['Standard', 'Custom'])
        self.cmb_type_alphabet.currentTextChanged.connect(self.change_mode)

        self.layout_line1 = QHBoxLayout()
        self.layout_line1.addWidget(self.led_alphabet)
        self.layout_line1.addWidget(self.cmb_type_alphabet)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_text)
        self.layout.addLayout(self.layout_line1)
        self.setLayout(self.layout)

    def change_alphabet(self, text):
        self.ingredient.set_alphabet(text)

    def change_mode(self, text):
        if text == 'Custom':
            self.led_alphabet.setReadOnly(False)
        else:
            self.led_alphabet.setReadOnly(True)
            self.led_alphabet.setText('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
            self.ingredient.set_alphabet('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
