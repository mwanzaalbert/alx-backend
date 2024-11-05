from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext

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

# Instantiate the Babel object
babel = Babel(app)

@babel.localeselector
def get_locale():
    # 1. Check if the locale parameter is in the URL query string
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    # 2. Check if the user is logged in and has a preferred locale
    if g.get('user') and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    # 3. Fall back to the accepted language from request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])

def get_user():
    """Retrieve a user based on the login_as parameter."""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None

@app.before_request
def before_request():
    """Retrieve and set the user in the global context before each request."""
    g.user = get_user()

@app.route('/')
def index():
    return render_template('6-index.html')

if __name__ == '__main__':
    app.run(debug=True)
