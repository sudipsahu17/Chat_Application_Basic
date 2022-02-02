from flask import Blueprint, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .models import User
from .db_manager import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

class AdminUserView(ModelView):
    column_list = ('id', 'first_name', 'last_name', 'email', 'role')
    column_exclude_list = ('password')
    form_columns = ('id', 'first_name', 'last_name', 'email')
    form_excluded_columns = ('password', 'role')
    column_labels = dict(id='User ID')
    column_sortable_list = ('first_name', 'last_name', 'email')
    column_searchable_list = ('first_name', 'last_name', 'email')

def admin_user_view(app):
    admin = Admin(app)
    admin.add_view(AdminUserView(User, db.session))