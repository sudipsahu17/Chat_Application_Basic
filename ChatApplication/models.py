from .db_manager import db
from datetime import datetime
import random
import string
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    password = db.Column(db.String(150), nullable=False, default=str(random_string))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='cascade'), nullable=False, default=3)
    group_admin = db.relationship('Group', backref='admin', cascade='all,delete-orphan')
    msg_writer = db.relationship('Message', backref='writer', cascade='all,delete-orphan')
    groups = db.relationship('GroupUser', backref='user', lazy='dynamic', cascade='all,delete-orphan')

    def __repr__(self):
        return self.email

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False)
    users = db.relationship('User', backref='roles', cascade='all,delete-orphan')

    def __repr__(self):
        return self.role

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    members = db.relationship('GroupUser', backref='group', lazy='dynamic', cascade='all,delete-orphan')
    msg = db.relationship('Message', backref='group', cascade='all,delete-orphan')

    def __repr__(self):
        return self.name

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    msg_txt = db.Column(db.String(15000), nullable=False)
    likes = db.Column(db.Integer, default=0)
    post_date = db.Column(db.DateTime, default=datetime.utcnow())
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='cascade'), nullable=False)

    def __repr__(self):
        return self.msg_txt

class GroupUser(db.Model):
    __tablename__ = 'groups_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='cascade'), nullable=False)