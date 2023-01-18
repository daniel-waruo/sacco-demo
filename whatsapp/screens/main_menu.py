from django.template.loader import render_to_string

from ..base_screens import Screen
from ..screen_utils import get_screen
from ..text_parsers import parse_interactive


class MainMenuScreen(Screen):
    state = 'main_menu'

    def render(self):
        phone = self.context['phone']
        text = render_to_string(
            'bot/home.txt',
            context={
                'display_name': 'Daniel',
                'errors': self.errors
            }
        )
        # organizations = Organization.objects.filter(
        #     customers__phone=self.context['phone']
        # )
        return {
            "recipient_type": "individual",
            "to": phone,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": "Menu"
                },
                "body": {
                    "text": text
                },
                "action": {
                    "button": "Providers",
                    "sections": [
                        {
                            "title": "Providers",
                            "rows": list(
                                map(
                                    lambda organization: {
                                        'id': organization.id,
                                        'title': organization.name
                                    },
                                    []
                                ))
                        },
                    ]
                }
            }
        }

    def next_screen(self, current_input):
        try:
            text = parse_interactive(current_input)
        except Exception as e:
            print(e)
            return self.error_screen(['Invalid Menu Option.Please try again.'])
        print("this is the text")
        print(text)
        return get_screen('enter_amount', data={'organization_id': text})
