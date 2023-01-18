from django.template.loader import render_to_string

from ussd.base_screens import Screen
from ussd.screen_utils import get_screen


class UtilityPaymentScreen(Screen):
    state = 'utility_payments'
    type = 'CON'

    def render(self):
        response = render_to_string(
            'ussd/utility_payments.txt',
            context={
                **self.context,
                'errors': self.errors
            }
        )
        return response

    def next_screen(self, current_input):
        return get_screen(
            "utility_phone_account",
            data={
                "utility": current_input
            }
        )


class UtilityPaymentAccountScreen(Screen):
    state = 'utility_phone_account'
    type = 'CON'
    required_fields = ["utility"]

    def render(self):
        response = render_to_string(
            'ussd/select_account.txt',
            context={
                **self.context,
                'errors': self.errors
            }
        )
        return response

    def next_screen(self, current_input):
        return get_screen(
            "utility_payments_amount",
            data=self.data
        )


class UtilityPaymentAmountScreen(Screen):
    state = 'utility_payments_amount'
    type = 'CON'
    required_fields = ["utility"]

    def render(self):
        response = "Enter amount you want to pay"
        return response

    def next_screen(self, current_input):
        return get_screen(
            "utility_payments_confirm",
            data={
                "amount": current_input,
                **self.data
            }
        )


class UtilityPaymentConfirmScreen(Screen):
    state = 'utility_payments_confirm'
    type = 'CON'
    required_fields = ["amount", "utility"]

    def render(self):
        utilities = [
            "DSTV",
            "Go TV",
            "Nairobi Water",
            "JTL"
        ]
        response = render_to_string(
            'ussd/utility_payments_confirm.txt',
            context={
                **self.data,
                "utility": utilities[self.data["utility"]]
            }
        )
        return response

    def next_screen(self, current_input):
        if current_input == 1:
            return get_screen(
                "enter_pin",
            )
        if current_input == 2:
            return get_screen("main_menu")
        return get_screen('enter_pin')
