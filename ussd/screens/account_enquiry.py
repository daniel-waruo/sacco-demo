from django.template.loader import render_to_string

from ussd.base_screens import Screen
from ussd.screen_utils import get_screen


class AccountEnquiryScreen(Screen):
    state = 'account_enquiry'
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
            "enter_pin",

        )

