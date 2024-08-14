class Salsa20:
    def __init__(self):
        self.name = 'salsa20'
        self.key = None
        self.key_type = 'base64'
        self.nonce = None
        self.nonce_type = 'base64'
        self.counter = 0
        self.rounds = None

    def decrypt(self):
        print('Decrypt')

    def set_key(self, text):
        self.key = text

    def set_nonce(self, text):
        self.nonce = text

    def set_rounds(self, text):
        self.rounds = text

    def set_counter(self, text):
        self.counter = text

    def set_key_type(self, text):
        self.key_type = str.lower(text)

    def set_nonce_type(self, text):
        self.nonce_type = str.lower(text)