from sharingan.base.customitembase import CustomItemBase

class Scatter(CustomItemBase):
    def __init__(self, parent=None):
        super(Scatter, self).__init__(parent)
        self.set_label_text('Scatter')

    def deobfuscate(self, start_ea, end_ea):
        print('Deobf Scatter') 

    def detect(self, start_ea, end_ea):
        print('Scan Internal')