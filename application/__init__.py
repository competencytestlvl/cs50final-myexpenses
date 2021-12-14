from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path


DB_NAME = "database.db"
# Initialize database
db = SQLAlchemy()


def create_app():
    """Creates instance of app with the default configurations."""
    app = Flask(__name__)
    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    # Remember to change the SECRET_KEY
    app.config["SECRET_KEY"] = "abc123"
    app.config["SESSION_TYPE"] = "filesystem"
    # Identify Database - SQLITE
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    # Initialize application
    db.init_app(app)

    from .item_models import User, Expenses

    # Create db
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        print(User.query.get(id))
        return User.query.get(int(id))

    return app


def create_database(app):
    # Create database if it does not already exists
    if not path.exists('application/' + DB_NAME):
        db.create_all(app=app)
        print('Created DB')