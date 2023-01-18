from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .base_screens import Screen
from .screen_utils import get_screen
from .sessions import Session


@csrf_exempt
def ussd_bot(request):
    code = "gas"
    if request.method == 'POST':
        phone_number = request.POST.get('phoneNumber')
        session_id = f"{code}:{phone_number}"
        text = request.POST.get('text')
        # initialize the gas session
        session = Session(
            session_id,
            context={
                'phone': phone_number,
            }
        )
        # load the default screen
        if not text:
            # if new gas session clear the session state
            session.session_state.reset()
            # return the default first screen
            screen = get_screen('main_menu')
            return session.render_ussd(screen)
        else:
            # get current_text
            current_input = text.split("*")[-1]
            # get current session
            current_screen: Screen = session.current_screen()
            try:
                current_input = int(current_input)
            except ValueError:
                return session.render_ussd(current_screen)
            # get the next screen
            next_screen = current_screen.next_screen(current_input)
            return session.render_ussd(next_screen)
    return HttpResponse("Invalid HTTP method", status=403)
