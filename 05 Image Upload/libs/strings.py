"""
libs.strings
By default, users `en-gb.json` fiel inside the `strings` top-level folder.
If language changes, set 'lib.string.default_locale` and run `libs.strings.refresh()`
"""

import json

default_locale = "en-gb"
cached_strings = {}


def refresh():
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


def set_default_locale(locale):
    global default_locale
    default_locale = locale

refresh()