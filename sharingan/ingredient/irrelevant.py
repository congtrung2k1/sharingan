from sharingan.base.customitembase import CustomItemBase

class Irrelevant(CustomItemBase):
    def __init__(self, parent=None):
        super(Irrelevant, self).__init__(parent)
        self.set_label_text('Irrelevant')

    def deobfuscate(self, start_ea, end_ea):
        print('Deobf Irrelevant')

    def detect(self, start_ea, end_ea):
        print('Scan Internal')