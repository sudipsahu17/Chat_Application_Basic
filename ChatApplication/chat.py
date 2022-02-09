from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

chats = Blueprint('chats', __name__)

@chats.route('/')
@login_required
def chat():
    return str(current_user.email)