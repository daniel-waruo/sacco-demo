from django.template.loader import render_to_string

from ussd.base_screens import Screen
from ussd.screen_utils import get_screen


class SendMoneyScreen(Screen):
    state = 'send_money'
    type = 'CON'

    def render(self):
        """return choose egg menu screen"""
        # choose products under brand and send it to the template
        response = render_to_string(
            'ussd/send_money.txt',
            context={
                **self.context,
                'errors': self.errors
            }
        )
        return response

    def next_screen(self, current_input):
        return get_screen("send_money_account")


class SendMoneyAccountScreen(Screen):
    state = 'send_money_account'
    type = 'CON'

    def render(self):
        response = "Enter account number of person you want to transfer to."
        return response

    def next_screen(self, current_input):
        return get_screen(
            "send_money_amount",
            data={
                "account_2": current_input
            }
        )


class SendMoneyAmountScreen(Screen):
    state = 'send_money_amount'
    type = 'CON'
    required_fields = ["account_2"]

    def render(self):
        response = "Enter amount of money you want to send."
        return response

    def next_screen(self, current_input):
        return get_screen(
            "send_money_account_confirm",
            data={
                "amount": current_input,
                "account_1": self.data["account_2"] + 2343,
                "account_2": self.data["account_2"]
            }
        )


class SendMoneyConfirmScreen(Screen):
    state = 'send_money_account_confirm'
    type = 'CON'
    required_fields = ["amount", "account_1", "account_2"]

    def render(self):
        response = render_to_string('ussd/send_money_confirm.txt', context=self.data)
        return response

    def next_screen(self, current_input):
        if current_input == 1:
            return get_screen(
                "enter_pin",
            )
        if current_input == 2:
            return get_screen("main_menu")
        return get_screen('enter_pin')
