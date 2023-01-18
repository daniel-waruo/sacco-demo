from ussd.base_screens import Screen


class MiniStatementScreen(Screen):
    state = 'mini_statement'
    type = 'END'

    def render(self):
        return "Successful .We have send you the mini statement on SMS."
