"""Unified translation system for Python and JavaScript.

Loads translations from JSON files and provides a _() function for Python.
Uses the same JSON files as the JavaScript frontend.
"""

import json
import os
from threading import local

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "web", "locales")

# Thread-local storage for locale
_thread_local = local()


def set_locale(locale):
    """Set the current locale for this thread."""
    _thread_local.locale = locale


def get_locale():
    """Get the current locale for this thread, defaulting to 'en'."""
    return getattr(_thread_local, "locale", "en")


def load_translations(locale):
    """Load translations for a given locale from JSON file."""
    json_path = os.path.join(JSON_DIR, f"{locale}.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to English if locale not found
        if locale != "en":
            return load_translations("en")
        return {}


def _(message):
    """Translate a message using the current locale.

    Args:
        message: The English string to translate

    Returns:
        The translated string, or the original if translation not found
    """
    locale = get_locale()
    translations = load_translations(locale)

    # Return translation if available, otherwise return original (English)
    return translations.get(message, message)


def init_translations(locale="en"):
    """Initialize translations for the given locale."""
    set_locale(locale)
