class AES:
    def __init__(self):
        self.name = 'aes'
        self.key = None
        self.key_type = 'base64'
        self.iv = None
        self.iv_type = 'base64'
        self.mode = 'mode_ebc'

    def set_key(self, key):
        self.key = key

    def set_iv(self, iv):
        self.iv = iv

    def set_mode(self, mode):
        self.mode = str.lower(mode)

    def set_type_key(self, type):
        self.key_type = str.lower(type)

    def set_type_iv(self, type):
        self.iv_type = str.lower(type)

    def decrypt(self):
        print('Decrypt')


