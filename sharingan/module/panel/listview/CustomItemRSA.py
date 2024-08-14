from PyQt5.QtWidgets import QPlainTextEdit, QComboBox, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QLineEdit
from sharingan.module.core.RSA import RSA


class CustomItemRSA(QWidget):
    def __init__(self, parent=None):
        super(CustomItemRSA, self).__init__(parent)

        self.ingredient = RSA()

        self.lbl_text = QLabel("RSA")
        self.lbl_text.setStyleSheet('font-weight: bold; font-size: 14pt;  color: rgb(87, 133, 78)')

        self.plt_key = QPlainTextEdit()
        self.plt_key.setPlaceholderText('RSA Private Key (PEM)')
        self.plt_key.textChanged.connect(self.change_key)

        self.cmb_encryption_scheme = QComboBox()
        self.cmb_encryption_scheme.addItems(['RSA-OAEP'])
        self.cmb_encryption_scheme.currentTextChanged.connect(self.change_mode)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_text)
        self.layout.addWidget(self.plt_key)
        self.layout.addWidget(self.cmb_encryption_scheme)
        self.setLayout(self.layout)

    def change_key(self):
        self.ingredient.set_key(self.plt_key.toPlainText())

    def change_mode(self, text):
        self.ingredient.set_mode(text)

