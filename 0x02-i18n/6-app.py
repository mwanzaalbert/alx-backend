#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Flask web application with internationalization using Flask-Babel.

This module configures a Flask application to support multiple languages
(English and French), and allows locale selection based on URL parameters,
user preferences, or request headers.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext
from typing import Optional, Dict

app: Flask = Flask(__name__)

# Mock user database
users: Dict[int, Dict[str, Optional[str]]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """
    Configuration class for setting language and timezone options.

    Attributes:
        LANGUAGES (list): Supported languages for the application.
        BABEL_DEFAULT_LOCALE (str): Default locale for the application.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the application.
    """
    LANGUAGES: list[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


# Apply the configuration to the app
app.config.from_object(Config)

app.url_map.strict_slashes = False

# Instantiate the Babel object for internationalization support
babel = Babel(app)

gettext.__doc__ = """ Dynamically assigns texts to html elements"""

@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for supported languages based on user preferences.

    Checks for a `locale` parameter in the URL query string, then the logged-in
    user's preferred locale, and finally the `Accept-Language` header from the
    request if no other option is available.

    Returns:
        str: The best matching language code based on the URL parameter,
        user preference, or headers.
    """
    # 1. Check if the locale parameter is in the URL query string
    locale: Optional[str] = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    # 2. Check if the user is logged in and has a preferred locale
    if g.get('user') and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    # 3. Fall back to the accepted language from request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Optional[Dict[str, Optional[str]]]:
    """
    Retrieve a user based on the login_as parameter.

    The function attempts to retrieve the user dictionary from the `users`
    dictionary based on the `login_as` query parameter.

    Returns:
        Optional[Dict[str, Optional[str]]]: The user dictionary if found,
        otherwise None.
    """
    try:
        user_id: int = int(request.args.get("login_as"))
        return users.get(user_id, None)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request() -> None:
    """
    Retrieve and set the user in the global context before each request.

    This function sets `g.user` to the user dictionary returned by
    `get_user()`, making it accessible in other parts of the application.
    """
    g.user = get_user()


@app.route('/')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: The rendered HTML template for the index page.
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
