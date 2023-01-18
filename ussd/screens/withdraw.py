from django.template.loader import render_to_string

from ussd.base_screens import Screen
from ussd.screen_utils import get_screen


class WithdrawScreen(Screen):
    state = 'withdraw'
    type = 'CON'

    def render(self):
        response = render_to_string(
            'ussd/account_enquiry.txt',
            context={
                **self.context,
                'errors': self.errors
            }
        )
        return response

    def next_screen(self, current_input):
        return get_screen(
            "withdraw_agent",
        )


class GetWithdrawAgentScreen(Screen):
    state = 'withdraw_agent'
    type = 'CON'

    def render(self):
        response = "Enter agent number"
        return response

    def next_screen(self, current_input):
        return get_screen(
            "withdraw_amount",
            data={
                "agent": current_input
            }
        )


class GetAmountScreen(Screen):
    state = 'withdraw_amount'
    type = 'CON'
    required_fields = ['agent']

    def render(self):
        response = "Enter amount to withdraw."
        return response

    def next_screen(self, current_input):
        return get_screen(
            "withdraw_confirm",
            data={
                **self.data,
                "amount": current_input
            }
        )


class ConfirmWithdrawScreen(Screen):
    state = 'withdraw_confirm'
    type = 'CON'
    required_fields = ['amount', 'agent']

    def render(self):
        response = render_to_string('ussd/withdraw_confirm.txt', context=self.data)
        return response

    def next_screen(self, current_input):
        if current_input == 1:
            return get_screen(
                "enter_pin",
            )
        if current_input == 2:
            return get_screen("main_menu")
        return get_screen('enter_pin')
