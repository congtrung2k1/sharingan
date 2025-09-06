from PyQt5.QtWidgets import QTabWidget, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import Qt
from sharingan.core import stylesmanager
import idaapi, idc, ida_bytes, ida_kernwin, ida_lines, ida_name
import threading

class ASMLine:
    def __init__(self, ea):
        self.colored_instruction = ida_lines.generate_disasm_line(ea)
        assert self.colored_instruction, f'Bad address... {hex(ea)}'
        self.label = ida_name.get_short_name(ea)
        self.address = ea
        self.padding = ' ' * 2

    @property
    def colored_address(self):
        return ida_lines.COLSTR('%08X' % self.address, ida_lines.SCOLOR_PREFIX)
    
    @property
    def colored_label(self):
        if not self.label:
            return None
        pretty_name = ida_lines.COLSTR(self.label, ida_lines.SCOLOR_CNAME) + ':'
        return ' '.join(['', self.colored_address, self.padding, pretty_name])
    
    @property
    def colored_blank(self):
        return ' '.join(['', self.colored_address])

    @property
    def colored_asmline(self):
        return ' '.join(['', self.colored_address, self.padding, self.colored_instruction])
    
class UIHooks(ida_kernwin.UI_Hooks):
    def ready_to_run(self):
        pass

    def get_lines_rendering_info(self, out, widget, rin):
        pass

    def populating_widget_popup(self, widget, popup, ctx):
        pass

class ASMView(ida_kernwin.simplecustviewer_t):
    def __init__(self):
        super().__init__()
        self.ui_hooks = UIHooks()
        self.ui_hooks.get_lines_rendering_info = self.highlight_lines

    def Create(self):
        if not super().Create('Before'):
            return False
        self._twidget = self.GetWidget()
        self.widget = ida_kernwin.PluginForm.TWidgetToPyQtWidget(self._twidget)
        self.ui_hooks.hook()
        return True
    
    def OnClose(self):
        self.ui_hooks.unhook()
    
    def disassemble(self, start_ea, end_ea):
        next_addr = start_ea
        self.ClearLines()
        while next_addr <= end_ea:
            line = ASMLine(next_addr)
            if line.label:
                self.AddLine(line.colored_blank)
                self.AddLine(line.colored_label)
            self.AddLine(line.colored_asmline)
            next_addr = idc.next_head(next_addr)
    
    def highlight_lines(self, out, widget, rin):
        if widget != self._twidget:
            return
        for _, line in enumerate(rin.sections_lines[0]):
            splace = ida_kernwin.place_t_as_simpleline_place_t(line.at)
            line_info = self.GetLine(splace.n)
            if not line_info:
                continue
            colored_text, _, _ = line_info
            line_input = ida_lines.tag_remove(colored_text)
            address = int(line_input.split()[0], 16)
            if address == 0x66204CF8:
                color = ida_kernwin.CK_EXTRA1
                e = ida_kernwin.line_rendering_output_entry_t(line)
                e.bg_color = color
                e.flags = ida_kernwin.LROEF_FULL_LINE
                out.entries.push_back(e)

class DisassembleTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(50, 100)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        main_tab = self
        while type(main_tab).__name__ != "Disassembler":
            main_tab = main_tab.parent()
        self.main_tab = main_tab
        self.cached_start_ea = None
        self.cached_end_ea = None
        self.mutex = threading.Lock()

        lbl_start_ea = QLabel('Start EA')
        lbl_end_ea = QLabel('End EA')
        self.start_ea = QLineEdit(self)
        self.end_ea = QLineEdit(self)
        self.start_ea.setPlaceholderText('Start')
        self.end_ea.setPlaceholderText('End')
        self.start_ea.editingFinished.connect(self.disassemble)
        self.end_ea.editingFinished.connect(self.disassemble)
        btn_choose = QPushButton('Choose', parent=self)
        btn_choose.clicked.connect(self.choose_function)
        cmb_todo = QComboBox(self)
        btn_resolve = QPushButton('Resolve', self)
        btn_resolve.clicked.connect(self.resolve)
        btn_revert = QPushButton('Revert', self)
        btn_revert.clicked.connect(self.revert)

        self.asm_before = ASMView()
        self.asm_after = ASMView()
        assert self.asm_before.Create(), 'Fail loading ASMView before'
        assert self.asm_after.Create(), 'Fail loading ASMView after'

        layout_toolbar = QHBoxLayout()
        layout_toolbar.addWidget(lbl_start_ea)
        layout_toolbar.addWidget(self.start_ea)
        layout_toolbar.addWidget(lbl_end_ea)
        layout_toolbar.addWidget(self.end_ea)
        layout_toolbar.addWidget(btn_choose)
        layout_toolbar.addWidget(cmb_todo)
        layout_toolbar.addWidget(btn_resolve)
        layout_toolbar.addWidget(btn_revert)
        layout_asm = QHBoxLayout()
        layout_asm.addWidget(self.asm_before.widget)
        layout_asm.addWidget(self.asm_after.widget)
        layout = QVBoxLayout(self)
        layout.addLayout(layout_toolbar, stretch=1)
        layout.addLayout(layout_asm, stretch=10)

    def resolve(self):
        print('Resolve')

    def revert(self):
        print('Revert')

    def choose_function(self):
        func = idaapi.choose_func("Choose function to deobfuscate", idc.get_screen_ea())
        if func is None:
            return
        
        start_func = func.start_ea
        end_func = func.end_ea

        func_name = idc.get_func_name(start_func)
        tab_title = func_name if func_name else hex(start_func)

        self.main_tab.setTabText(self.main_tab.indexOf(self), tab_title)
        self.start_ea.clear()
        self.end_ea.clear()
        self.start_ea.setText(hex(start_func))
        self.start_ea.editingFinished.emit()
        self.end_ea.setText(hex(end_func))
        self.end_ea.editingFinished.emit()

    def disassemble(self):
        self.mutex.acquire()
        try:
            start_ea_txt = self.start_ea.text()
            end_ea_txt = self.end_ea.text()
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
        self.asm_before.disassemble(start_ea, end_ea)
        self.asm_after.disassemble(start_ea, end_ea)
        print (raw)
        self.mutex.release()

class Disassembler(QTabWidget):
    def __init__(self, parent=None):
        super(Disassembler, self).__init__(parent)
        self.setTabsClosable(True) 
        self.setMovable(True)
        self.setObjectName('disassembler')
        self.tabCloseRequested.connect(self.close_tab)
        self.btn_add_tab = QPushButton(' + ')
        self.btn_add_tab.setObjectName('new_tab')
        self.btn_add_tab.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.btn_add_tab.clicked.connect(self.add_new_tab)
        self.setCornerWidget(self.btn_add_tab, Qt.TopRightCorner)
        self.setStyleSheet(stylesmanager.get_stylesheet())

        self.add_new_tab()

    def add_new_tab(self):
        tab_content = DisassembleTab(self)
        self.addTab(tab_content, f"Tab {self.count() + 1}")

    def close_tab(self, index):
        self.removeTab(index)