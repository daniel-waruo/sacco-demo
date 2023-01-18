from django.template.loader import render_to_string

from ussd.base_screens import Screen
from ussd.screen_utils import get_screen


class EnterPinScreen(Screen):
    state = 'enter_pin'
    type = 'CON'

    def render(self):
        response = render_to_string(
            self.data.get('template', 'ussd/enter_pin_default.txt'),
            context={
                **self.context,
                'errors': self.errors
            }
        )
        return response

    def next_screen(self, current_input):
        return get_screen("transaction_complete")


class TransactionCompleteScreen(Screen):
    state = 'transaction_complete'
    type = 'END'
    required_fields = []

    def render(self):
        response = render_to_string(
            self.data.get('template', 'ussd/transaction_complete_default.txt'),
            context={
                **self.context,
                'errors': self.errors
            }
        )
        return response
