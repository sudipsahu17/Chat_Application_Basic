from flask import redirect, url_for, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from .models import User, Role, Message, Group, GroupUser
from .db_manager import db

class AdminMixin:
    def is_accessible(self):
        if current_user.is_authenticated and str(current_user.roles) == 'admin':
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        flash('Unauthorized access !! You are not authorized to access the admin panel !!', category='error')
        return redirect(url_for('controllers.login'))

class AdminUserView(AdminMixin, ModelView):
    column_list = ('id', 'first_name', 'last_name', 'email', 'password', 'roles')
    #column_exclude_list = ('password')
    form_columns = ('first_name', 'last_name', 'email', 'password', 'roles')
    #form_excluded_columns = ('password')
    #column_labels = dict(id='User ID')
    column_sortable_list = ('first_name', 'last_name', 'email')
    column_searchable_list = ('first_name', 'last_name', 'email')
    column_filters = ['roles']

class AdminHomeView(AdminMixin, AdminIndexView):
    pass

def admin_user_view(app):
    admin = Admin(app, 'ChatApp', url='/', index_view=AdminHomeView(name='Admin'))
    admin.add_view(AdminUserView(User, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(Group, db.session))
    admin.add_view(ModelView(GroupUser, db.session))
    admin.add_view(ModelView(Message, db.session))