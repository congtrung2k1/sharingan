class Add:
    def __init__(self):
        self.name = 'add'
        self.key = None
        self.key_type = 'base64'

    def set_key(self, text):
        self.key = text

    def set_key_type(self, text):
        self.key_type = str.lower(text)

    def decrypt(self):
        print('Decrypt')