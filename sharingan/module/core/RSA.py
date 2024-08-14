class RSA:
    def __init__(self):
        self.name = 'rsa'
        self.key = None
        self.mode = 'rsa-oaep'

    def decrypt(self):
        print('Decrypt')

    def set_key(self, text):
        self.key = text

    def set_mode(self, text):
        self.mode = str.lower(text)
