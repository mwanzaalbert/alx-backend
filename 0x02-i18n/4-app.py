#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Flask web application with internationalization using Flask-Babel.

This module configures a Flask application to support multiple languages
(English and French), sets default locale and timezone configurations,
and includes a locale selector that prioritizes the `locale` URL parameter
before checking the 'Accept-Language' header.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, gettext

app: Flask = Flask(__name__)


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


# Apply the configuration to the app
app.config.from_object(Config)

app.url_map.strict_slashes = False

# Instantiate the Babel object for internationalization support
babel: Babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for supported languages based on user preferences.

    First, check if the 'locale' parameter is provided in the URL query string.
    If valid, this locale is used. Otherwise, it falls back to the language
    best matching the 'Accept-Language' header from the request.

    Returns:
        str: The best matching language code based on URL parameter or headers.
    """
    # Check if the locale parameter is in the URL query string
    locale: str = request.args.get('locale', '')
    if locale in app.config['LANGUAGES']:
        return locale
    # Fall back to the accepted language from request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: The rendered HTML template for the index page.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(host='0.0.0.0', port=5000)
