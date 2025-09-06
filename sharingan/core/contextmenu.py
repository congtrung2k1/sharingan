import idaapi, ida_kernwin

TODO_LIST = 'sharingan:todo'
FIND_OBFU = 'sharingan:find_obfu'
REVERT = 'sharingan:revert'

class HookRightClick(idaapi.UI_Hooks):
    def finish_populating_widget_popup(self, widget, popup):
        if idaapi.get_widget_type(widget) == ida_kernwin.BWN_DISASM:
            ida_kernwin.attach_action_to_popup(widget, popup, TODO_LIST, None, 0)
            ida_kernwin.attach_action_to_popup(widget, popup, FIND_OBFU, None, 0)
            ida_kernwin.attach_action_to_popup(widget, popup, REVERT, None, 0)
        return 0
    
class handler_add_todo(idaapi.action_handler_t):
    def activate(self, ctx):
        print('Add todo list')

    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS
    
class handler_find_obfus(idaapi.action_handler_t):
    def activate(self, ctx):
        print('Find obfuscated code')

    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS
    
class handler_revert(idaapi.action_handler_t):
    def activate(self, ctx):
        print('Revert code')

    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS
    
class InitHookMenu():
    def __init__(self):
        action_add_todo = idaapi.action_desc_t(TODO_LIST, 'Add todo list', handler_add_todo(), None, None, -1)
        action_find_obfu = idaapi.action_desc_t(FIND_OBFU, 'Find obfuscated code', handler_find_obfus(), None, None, -1)
        action_revert = idaapi.action_desc_t(REVERT, 'Revert code', handler_revert(), None, None, -1)
        assert idaapi.register_action(action_add_todo), "Action registration failed"
        assert idaapi.register_action(action_find_obfu), "Action registration failed"
        assert idaapi.register_action(action_revert), "Action registration failed"
        self.hook_menu = HookRightClick()
        self.hook_menu.hook()

    def cleanup(self):
        self.hook_menu.unhook()
        idaapi.unregister_action(TODO_LIST)
        idaapi.unregister_action(FIND_OBFU)
        idaapi.unregister_action(REVERT)
