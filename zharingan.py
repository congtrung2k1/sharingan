import idaapi
from sharingan.mainwindow import MainWindow
from sharingan.core.stylesmanager import ManageStyleSheet
from sharingan.core.contextmenu import InitHookMenu


class PluginPanel(idaapi.PluginForm):
    current_instance = None

    def __init__(self):
        super().__init__()
        self.main_layout = None

    """Panel for the IDA GUI."""
    def OnCreate(self, form):
        self.parent = self.FormToPyQtWidget(form)
        self.main_layout = MainWindow(self)
        PluginPanel.current_instance = self

    def OnClose(self, form):
        PluginPanel.current_instance = None

class Sharingan(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP
    comment = 'Assist and ease obfuscation'
    wanted_name = 'Sharingan'
    wanted_hotkey = ''
    help = ''

    def init(self):
        """Init the IDA plugin."""
        idaapi.msg("Sharingan initialized!!!\n")
        self.hook_menu = InitHookMenu()
        return idaapi.PLUGIN_KEEP
    
    def run(self, arg):
        """Run the IDA plugin."""
        if PluginPanel.current_instance is not None:
            idaapi.msg("Sharingan is already running! Please check the opened tab.\n")
            return
        
        idaapi.msg('Running ' + self.wanted_name + '\n')
        self.sharingan_gui = PluginPanel()
        self.sharingan_gui.Show('Sharingan')
        ManageStyleSheet.load_stylesheet()
        recipe = self.sharingan_gui.main_layout.recipe
        self.hook_menu.register_recipe(recipe)
    
    def term(self):
        self.hook_menu.cleanup()


def PLUGIN_ENTRY():
    return Sharingan()