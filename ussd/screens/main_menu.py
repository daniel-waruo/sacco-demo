from django.template.loader import render_to_string

from ussd.base_screens import Screen
from ussd.screen_utils import get_screen


class MainMenuScreen(Screen):
    state = 'main_menu'
    type = 'CON'

    def render(self):
        """return choose egg menu screen"""
        # choose products under brand and send it to the template
        response = render_to_string(
            'ussd/main_menu.txt',
            context={
                **self.context,
                'errors': self.errors
            }
        )
        return response

    def next_screen(self, current_input):
        """return choose egg menu screen"""
        # choose products under brand and send it to the template
        if str(current_input) == "1":
            return get_screen("account_enquiry")
        if str(current_input) == "2":
            return get_screen("withdraw")
        if str(current_input) == "3":
            return get_screen("send_money")
        if str(current_input) == "4":
            return get_screen("buy_airtime")
        if str(current_input) == "5":
            return get_screen("mini_statement")
        if str(current_input) == "6":
            return get_screen("utility_payments")
        return get_screen("main_menu")


