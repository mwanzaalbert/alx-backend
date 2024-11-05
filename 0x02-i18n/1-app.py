#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Flask web application with internationalization support using Flask-Babel.

This module configures a simple Flask application to support multiple languages
(English and French) and sets default locale and timezone configurations.
"""

from flask import Flask, render_template
from flask_babel import Babel

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

# Instantiate the Babel object for internationalization support
babel: Babel = Babel(app)


@app.route('/')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: The rendered HTML template for the index page.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
