from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext, format_datetime
import pytz
from datetime import datetime
from pytz.exceptions import UnknownTimeZoneError

app = Flask(__name__)

# Mock user database
users = {
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
def get_locale():
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.get('user') and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
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

def get_user():
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None

@app.before_request
def before_request():
    g.user = get_user()

@app.route('/')
def index():
    # Determine current time in inferred timezone
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
