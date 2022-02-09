from flask import Flask
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'riktam'
    app.config['SESSION_PASSWORD_SALT'] = 'riktam'
    app.config['SESSION_PASSWORD_HASH'] = 'sha256_crypt'

    from .controllers import controllers, groups
    from .chat import chats
    app.register_blueprint(controllers, url_prefix='/')
    app.register_blueprint(groups, url_prefix='/groups')
    app.register_blueprint(chats, url_prefix='/chats')

    from .db_manager import create_db_cursor, create_schema
    create_db_cursor(app)

    login_manager = LoginManager()
    login_manager.login_view = 'controllers.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .models import User
    create_schema(app)

    from .views import admin_user_view
    admin_user_view(app)

    return app