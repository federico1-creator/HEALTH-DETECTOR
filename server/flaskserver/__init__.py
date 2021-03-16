from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskserver.config import Config
import os

# protegge attacchi da funzione secrets

db = SQLAlchemy()  # db structures as classes
bcrypt = Bcrypt()
login_manager = LoginManager()  # session handler
login_manager.login_view = 'login'  # function name same as url_for
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskserver.DB_Obj import Role
    from flaskserver.DB_Obj import User
    from flaskserver.DB_Obj import Post
    from flaskserver.DB_Obj import Comment
    from flaskserver.DB_Obj import UserData
    from flaskserver.DB_Obj import Doctor
    from flaskserver.users.utils import insert_roles

    app.app_context().push()

    if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')):
        print('Creating DB')
        app.app_context().push()
        db.create_all()
        insert_roles()
        if os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')):
            print('Success')

    from flaskserver.users.routes import users
    from flaskserver.posts.routes import posts
    from flaskserver.main.routes import main
    from flaskserver.errors.handlers import errors
    from flaskserver.doctors.routes import doctors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(doctors)

    return app
