class Base64:
    def __init__(self):
        self.name = 'base64'
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    def set_alphabet(self, text):
        self.alphabet = text

    def decrypt(self):
        print('Decrypt')