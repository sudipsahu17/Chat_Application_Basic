from flask import Flask

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'raktim'

    from .views import views
    from .controllers import controllers
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(controllers, url_prefix='/')

    from .db_manager import create_db_cursor, create_schema
    create_db_cursor(app)
    from .models import User
    create_schema(app)

    from .views import admin_user_view
    admin_user_view(app)

    return app