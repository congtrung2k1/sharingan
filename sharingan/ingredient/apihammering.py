from sharingan.base.customitembase import CustomItemBase

class APIHammering(CustomItemBase):
    def __init__(self, parent=None):
        super(APIHammering, self).__init__(parent)
        self.set_label_text('APIHammering')

    def deobfuscate(self, start_ea, end_ea):
        print('Deobf APIHammering')

    def detect(self, start_ea, end_ea):
        print('Scan Internal')