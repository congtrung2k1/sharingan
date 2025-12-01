import idaapi, os
  

class ManageStyleSheet:
    stylesheet = None

    @staticmethod
    def load_stylesheet():
        path_plugin = idaapi.get_ida_subdirs("plugins")
        for path in path_plugin:
            path_stylesheet = os.path.join(path, 'sharingan', 'core', 'styles.qss')
            if os.path.exists(path_stylesheet):
                with open(path_stylesheet, 'r') as file:
                    ManageStyleSheet.stylesheet = file.read()
                    break
    
    @staticmethod
    def get_stylesheet():
        if not ManageStyleSheet.stylesheet:
            ManageStyleSheet.load_stylesheet()
        return ManageStyleSheet.stylesheet