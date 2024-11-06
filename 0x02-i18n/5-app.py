#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Flask web application with internationalization using Flask-Babel.

This module configures a Flask application to support multiple languages
(English and French), sets default locale and timezone configurations,
and handles user context for locale preferences based on user login.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext


class Config:
    """
    Configuration class for setting language and timezone options.

    Attributes:
        LANGUAGES (list): Supported languages for the application.
        BABEL_DEFAULT_LOCALE (str): Default locale for the application.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the application.
    """
    LANGUAGES: list = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


app: Flask = Flask(__name__)

# Apply the configuration to the app
app.config.from_object(Config)

app.url_map.strict_slashes = False

# Instantiate the Babel object for internationalization support
babel = Babel(app)

gettext.__doc__ = """ Dynamically assigns texts to html elements"""

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for supported languages based on user preferences.

    First, check if the 'locale' parameter is provided in the URL query string.
    If valid, this locale is used.
    If a user is logged in, their locale preference
    is checked next. Finally, it falls back to the language best matching the
    'Accept-Language' header.

    Returns:
        str: The best matching language code based on URL parameter,
        user preference, or headers.
    """
    locale: str = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.get('user') and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """
    Retrieve a user based on the login_as parameter.

    Returns:
        dict or None: The user dictionary if found, otherwise None.
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

    This function is executed before each request and sets the `g.user`
    variable with the retrieved user information.
    """
    g.user = get_user()


@app.route('/')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: The rendered HTML template for the index page.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
