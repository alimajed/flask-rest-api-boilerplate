import json


default_locale = "en-us"
cached_strings = {}


def refresh():
    print("refreshing")
    global cached_strings
    with open(f"app/common/strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()
