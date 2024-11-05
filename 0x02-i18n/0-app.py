#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A simple Flask web application that renders a template for the index page.

This module defines a Flask application and a single route that renders
the `0-index.html` template.
"""

from flask import Flask, render_template

app: Flask = Flask(__name__)


@app.route('/')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: The rendered HTML template for the index page.
    """
    return render_template('0-index.html')


if __name__ == '__main__':
    # Run the Flask application in debug mode.
    app.run(debug=True)
