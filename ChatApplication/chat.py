from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from flask_socketio import join_room, leave_room, emit, send
from . import socketio
from .models import Message
from .db_manager import db
import time

from ChatApplication.models import Group, GroupUser

chats = Blueprint('chats', __name__)

group = None

@chats.route('/<int:group_id>')
@login_required
def chat(group_id):
    global group
    if group_id:
        group = Group.query.filter_by(id=group_id).first()
        if group:
            is_member = GroupUser.query.filter(GroupUser.user_id == current_user.id, GroupUser.group_id == group.id).first()
            if is_member:
                older_messages = Message.query.filter_by(group_id=group.id).all()
                return render_template('chat.html', user=current_user, group=group, messages=older_messages)
            else:
                flash('Unauthorized access !! You are not part of this group !!', category='error')
        else:
            flash('Group not exist !! Invalid group id !!', category='error')
    else:
        flash('Unknown URI is triggered !!', category='error')
    return redirect(url_for('groups.get_groups'))

@socketio.on('join')
def on_user_join(data):
    room = data['room']
    join_room(room)

@socketio.on('leave')
def on_user_leave(data):
    #username = data['username']
    room = data['room']
    leave_room(room)
    # time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    # send({"msg": "offline !!", "username": username, "time_stamp": time_stamp}, room=room)

@socketio.on('user_message')
def on_user_message(data):
    msg = data['msg']
    uid = data['uid']
    username = data['username']
    room = data['room']
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    message = Message(msg_txt=msg, sender_id=int(uid), group_id=int(room))
    db.session.add(message)
    db.session.commit()
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)

# @socketio.on('message')
# def message_handler(msg):
#     print(msg)