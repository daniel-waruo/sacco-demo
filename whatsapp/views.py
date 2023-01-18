import json
import sys
import threading
import traceback

from asgiref.sync import sync_to_async, async_to_sync
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .screen_utils import get_screen
from .base_screens import Screen
from .sessions import Session
from .text_parsers import parse_text
from .utils import send_whatsapp, get_hook_data


def get_message_body(session: Session, message):
    # check if in trigger word and set session appropriately
    trigger_words = ['hi', 'hallo', 'lipa']
    try:
        text = parse_text(message)
        if not session.state or text.lower().strip() in trigger_words:
            session.reset()
            # return the default first screen
            screen = get_screen('main_menu')
            return session.render(screen)
    except KeyError:
        pass

    # get current session
    current_screen: Screen = session.current_screen(get_screen_func=get_screen)

    # get the next screen
    next_screen = current_screen.next_screen(message)
    if not next_screen:
        session.reset()
    return session.render(next_screen)


def bot_processing(data):
    try:
        data = get_hook_data(data)
        if not data:
            return
        phone, session_id, name, message = data
        # session id is the buyer id
        session = Session(
            session_id,
            context={
                'phone': phone,
                'name': name
            }
        )

        message = get_message_body(session, message)

        if message:
            if isinstance(message, dict):
                send_whatsapp(to=phone, body=message)
                return
            send_whatsapp(to=phone, message=message)
    except Exception as e:
        print("-" * 60)
        print(e)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)


bot_processing_async = sync_to_async(bot_processing, thread_sensitive=False)


async def whatsapp_bot_async(request):
    try:
        if request.method == "GET":
            return HttpResponse(request.GET.get('hub.challenge'))
        data = json.loads(request.body)
        t = threading.Thread(target=bot_processing, args=[data], daemon=True)
        t.start()
        return HttpResponse("Success")
    except Exception as e:
        print("-" * 60)
        print(e)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)
    return HttpResponse("Successful")


whatsapp_bot = csrf_exempt(async_to_sync(whatsapp_bot_async))
