import json

import requests

from whatsapp.models import Message

WABA_PHONE_ID = '110400311680161'
FACEBOOK_ACCESS_TOKEN = 'EAAIVJzFWSBEBAFGa6NiE9MbHZAdFgEnbYD6A7zxMO4p0liEVD8wwUJqhZCcZApkeo3CzToZCCXZAgKuu8Vt661PFoeaL7IQBtdcOMEBb8Xr2YT9HKLHKzaS0h1lC0515cjZBjW5C6qxJW9uikvju1eWRTOE17yx1dm7xI5CHxE7B673ur7hvkx'


def send_whatsapp(to: str, message: str = None, body=None):
    url = f"https://graph.facebook.com/v13.0/{WABA_PHONE_ID}/messages"
    if message:
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "recipient_type": "individual",
            "text": {
                "body": message
            }
        })
    else:
        if not body.get('to'):
            body['to'] = to
        body["messaging_product"] = "whatsapp"
        payload = json.dumps(body, indent=2)
        print(payload)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {FACEBOOK_ACCESS_TOKEN}"
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=1000)
        print(response.text)
    except ConnectionError:
        print("failed connection")


def get_hook_data(data):
    data = data["entry"][0]["changes"][0]["value"]

    if data.get("contacts"):
        sender = data["contacts"][0]
        phone = sender["wa_id"]
        session_id = f"whatsapp:{phone}"
        name = sender["profile"]["name"]
        message = data["messages"][0]
        if not Message.objects.filter(message_id=message["id"]).exists():
            Message.objects.create(message_id=message["id"])

            url = f"https://graph.facebook.com/v13.0/{WABA_PHONE_ID}/messages"
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": message["id"]
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {FACEBOOK_ACCESS_TOKEN}"
            }
            try:
                response = requests.request("POST", url, headers=headers, data=payload, timeout=1000)
                print(response.text)
            except ConnectionError:
                print("failed connection")
            # create an instance of message on our local database
            return phone, session_id, name, message
    return None
