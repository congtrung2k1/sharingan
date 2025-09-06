from sharingan.base.customitembase import CustomItemBase

class JmpClean(CustomItemBase):
    def __init__(self, parent=None):
        super(JmpClean, self).__init__(parent)
        self.set_label_text('JmpClean')

    def deobfuscate(self, start_ea, end_ea):
        print('Deobf JmpClean')

    def detect(self, start_ea, end_ea):
        print('Scan Internal')