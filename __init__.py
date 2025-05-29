from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
login = LoginManager()
login.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)

    from models.user import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes import register_routes
    register_routes(app)

    return app