import inspect


def get_screens():
    from .screens import screens
    from .base_screens import Screen
    screen_urls = []
    for key, value in screens.items():
        if inspect.isclass(value):
            if issubclass(value, Screen) and not value == Screen:
                screen_urls.append(value)
    return screen_urls


def _get_screen(state: str, screen_urls: list, data: dict, errors=None, context: dict = None):
    """searches the screen_urls list and returns the screen"""
    states = [x.state for x in screen_urls]
    if state in states:
        screen_index = states.index(state)
        screen_class = screen_urls[screen_index]
        return screen_class(data, errors, context)
    raise Exception(f"invalid screen url name:{state} not found in urls")


def get_screen(state, data=None, context=None, errors=None):
    return _get_screen(state=state, screen_urls=get_screens(), data=data, errors=errors, context=context)
