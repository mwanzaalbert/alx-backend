#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Flask web application with internationalization and timezone support.

The app provides language and timezone settings based on URL parameters, user
preferences, or defaults, and displays the current time formatted to the user's
timezone and locale.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext, format_datetime
import pytz
from datetime import datetime
from pytz.exceptions import UnknownTimeZoneError
from typing import Optional, Dict

app = Flask(__name__)

# Mock user database
users: Dict[int, Dict[str, Optional[str]]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for supported languages based on user preferences.

    Returns:
        str: The best matching language code based on the URL parameter,
        user preference, or headers.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.get('user') and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """
    Determine the best timezone for the user.

    Returns:
        str: The best matching timezone, or default timezone if none is found.
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass
    if g.get('user') and g.user.get('timezone'):
        try:
            return pytz.timezone(g.user['timezone']).zone
        except UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


def get_user() -> Optional[Dict[str, Optional[str]]]:
    """
    Retrieve a user based on the login_as parameter.

    Returns:
        Optional[Dict[str, Optional[str]]]: The user dictionary if found,
        otherwise None.
    """
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request() -> None:
    """Set the user in the global context before each request."""
    g.user = get_user()


@app.route('/')
def index() -> str:
    """
    Render the index page, displaying the current time formatted to the user's
    timezone.

    Returns:
        str: The rendered HTML template for the index page.
    """
    # Determine the current time in the inferred timezone
    user_timezone = get_timezone()
    try:
        timezone = pytz.timezone(user_timezone)
    except UnknownTimeZoneError:
        timezone = pytz.timezone(app.config['BABEL_DEFAULT_TIMEZONE'])
    current_time = datetime.now(timezone)
    formatted_time = format_datetime(current_time, format="medium")

    return render_template('index.html', current_time=formatted_time)


if __name__ == '__main__':
    app.run(debug=True)
