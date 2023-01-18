def parse_text(message):
    return message["text"]["body"]


def parse_interactive(message):
    return message["interactive"]["list_reply"]["id"]


def parse_button(message):
    return message["interactive"]["button_reply"]["id"]


def parse_contact(message):
    contact = message['contacts'][0]
    return {
        'name': contact['name']['formatted_name'],
        'phone': contact['phones'][0]['wa_id'],
    }


def parse_contacts(message):
    contacts = message['contacts']

    return list(
        map(
            lambda contact: {
                'name': contact['name']['formatted_name'],
                'phone': contact['phones'][0]['wa_id'],
            },
            contacts
        )
    )


def parse_image(message):
    image = message['image']
    return image
