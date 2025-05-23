from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

from models import db
db.init_app(app)

login = LoginManager(app)
login.login_view = 'login'

import routes

if __name__ == '__main__':
    app.run(debug=True)
