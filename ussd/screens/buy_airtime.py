from django.template.loader import render_to_string

from ussd.base_screens import Screen
from ussd.screen_utils import get_screen


class BuyAirtimeScreen(Screen):
    state = 'buy_airtime'
    type = 'CON'

    def render(self):
        response = render_to_string(
            'ussd/buy_airtime.txt',
            context={
                **self.context,
                'errors': self.errors
            }
        )
        return response

    def next_screen(self, current_input):
        return get_screen("buy_airtime_phone")


class BuyAirtimePhoneScreen(Screen):
    state = 'buy_airtime_phone'
    type = 'CON'

    def render(self):
        response = "Enter your phone number e.g 07XX"
        return response

    def next_screen(self, current_input):
        return get_screen(
            "buy_airtime_amount",
            data={
                "phone": f"+254{current_input}"
            }
        )


class BuyAirtimeAmountScreen(Screen):
    state = 'buy_airtime_amount'
    type = 'CON'
    required_fields = ["phone"]

    def render(self):
        response = "Enter amount of airtime you want to buy"
        return response

    def next_screen(self, current_input):
        return get_screen(
            "buy_airtime_confirm",
            data={
                "amount": current_input,
                **self.data
            }
        )


class BuyAirtimeConfirmScreen(Screen):
    state = 'buy_airtime_confirm'
    type = 'CON'
    required_fields = ["phone", "amount"]

    def render(self):
        response = render_to_string(
            'ussd/buy_airtime_confirm.txt',
            context=self.data
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