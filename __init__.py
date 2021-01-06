from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '7442317533b7095d2d16a5138ad43679'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

    bcrypt = Bcrypt(app)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_message = f"Login Required"
    login_manager.login_message_category = "danger"
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Classification

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
    app.run(debug=True)
