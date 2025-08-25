from PyQt5.QtWidgets import QTabWidget, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QGridLayout
from sharingan.module import StylesManager
import idaapi, idc, ida_bytes
import threading

class DisassembleTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        main_tab = self
        while type(main_tab).__name__ != "Disassembler":
            main_tab = main_tab.parent()
        self.main_tab = main_tab
        self.cached_start_ea = None
        self.cached_end_ea = None
        layout = QVBoxLayout(self)
        self.mutex = threading.Lock()

        start_ea_lbl = QLabel('Start EA')
        end_ea_lbl = QLabel('End EA')
        self.start_ea_address = QLineEdit(self)
        self.end_ea_address = QLineEdit(self)
        self.start_ea_address.setPlaceholderText('Start')
        self.end_ea_address.setPlaceholderText('End')
        btn_choose = QPushButton('Choose', parent=self)
        btn_choose.clicked.connect(self.choose_function)
        btn_add_tab = QPushButton('+')
        btn_add_tab.clicked.connect(self.main_tab.add_new_tab)

        layout_toolbar = QGridLayout()
        layout_toolbar.setContentsMargins(10, 10, 10, 0)

        layout_toolbar.addWidget(start_ea_lbl, 0, 0, 1, 1)
        layout_toolbar.addWidget(end_ea_lbl, 1, 0, 1, 1)

        layout_toolbar.addWidget(self.start_ea_address, 0, 1, 1, 4)
        layout_toolbar.addWidget(self.end_ea_address, 1, 1, 1, 4)

        layout_toolbar.addWidget(btn_choose, 0, 5, 2, 1)
        layout_toolbar.addWidget(btn_add_tab, 0, 6, 2, 1)
        layout.addLayout(layout_toolbar, stretch=1)
        self.lbl_dis = QLabel('Disassembler')
        self.lbl_dis.setObjectName('disassembler')

        self.start_ea_address.editingFinished.connect(self.disassemble)
        self.end_ea_address.editingFinished.connect(self.disassemble)
        layout.addWidget(self.lbl_dis, stretch=10)

    def choose_function(self):
        func = idaapi.choose_func("Choose function to deobfuscate", idc.get_screen_ea())
        if func is None:
            return
        
        start_func = func.start_ea
        end_func = func.end_ea

        tab = self.sender()
        func_name = idc.get_func_name(start_func)
        tab_title = func_name if func_name else hex(start_func)

        self.main_tab.setTabText(self.main_tab.indexOf(self), tab_title)
        self.lbl_dis.setText(str(hex(start_func)))
        self.start_ea_address.clear()
        self.end_ea_address.clear()
        self.start_ea_address.setText(hex(start_func))
        self.start_ea_address.editingFinished.emit()
        self.end_ea_address.setText(hex(end_func))
        self.end_ea_address.editingFinished.emit()

    def disassemble(self):
        self.mutex.acquire()
        try:
            start_ea_txt = self.start_ea_address.text()
            end_ea_txt = self.end_ea_address.text()
            if start_ea_txt == "" or end_ea_txt == "": 
                self.mutex.release()
                return

            if start_ea_txt[:2].lower() == "0x":
                start_ea = int(start_ea_txt, 16)
            else:
                start_ea = int(start_ea_txt)
            if end_ea_txt[:2].lower() == "0x":
                end_ea = int(end_ea_txt, 16)
            else:
                end_ea = int(end_ea_txt)
            # print(self.cached_start_ea, self.cached_end_ea, "=>", start_ea, end_ea)
            assert(end_ea > start_ea)
            if self.cached_start_ea == start_ea and self.cached_end_ea == end_ea: 
                self.mutex.release()
                return
            self.cached_start_ea = start_ea
            self.cached_end_ea = end_ea
            assert(start_ea != None and end_ea != None)
        except:
            print("Error parsing address")
            self.mutex.release()
            return

        raw = ida_bytes.get_bytes(start_ea, end_ea - start_ea)
        print (raw)
        self.mutex.release()

class Disassembler(QTabWidget):

    def __init__(self, parent=None):
        super(Disassembler, self).__init__(parent)
        self.setTabsClosable(True) 
        self.setMovable(True)
        self.setObjectName('disassembler')
        self.setStyleSheet(StylesManager.get_stylesheet())
        self.tabCloseRequested.connect(self.close_tab)
        self.add_new_tab()

    def add_new_tab(self):
        tab_content = DisassembleTab(self)
        self.addTab(tab_content, f"Tab {self.count() + 1}")

    def close_tab(self, index):
        self.removeTab(index)

