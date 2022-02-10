from flask import Blueprint, render_template, request, flash, redirect, url_for
from .utils import validate_name, validate_email, validate_password
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from .models import User, Group, GroupUser
from .db_manager import db

controllers = Blueprint('controllers', __name__)
groups = Blueprint('groups', __name__)

@controllers.route('/')
def home():
    return render_template('home.html', user=current_user)

@controllers.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstName').capitalize()
        last_name = request.form.get('lastName').capitalize()
        email = request.form.get('email').lower()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not validate_email(email):
            flash('Invalid email id !! Please check and try again !!', category='error')
        elif not validate_name(first_name):
            flash('First Name is invalid !! Should contain only alphabets and length should be more than 2 !!',
                  category='error')
        elif not validate_name(last_name):
            flash('Last Name is invalid !! Should contain only alphabets and length should be more than 2 !!',
                  category='error')
        elif not validate_password(password1):
            flash("Invalid password. Length should be more than 6 !!", category='error')
        elif password2 != password1:
            flash("Password mismatch !! Please enter same passwords !!", category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash("User is already registered !!")
            else:
                #user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password1,
                #                                                                                                method='sha256'))
                user = User(first_name=first_name, last_name=last_name, email=email, password=password1)
                db.session.add(user)
                db.session.commit()
                flash('You are successfully registered !! Now, Admin will check and gives access to chat-bar. '
                        'Please wait. Thanks !!', category='success')
                return redirect(url_for('controllers.home'))
    return render_template('register.html', user=current_user)

@controllers.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('controllers.home'))

    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')

        if not validate_email(email):
            flash('Invalid email id !! Please check and try again !!', category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                #if check_password_hash(user.password, password):
                if user.password == password:
                    if str(user.roles) != 'na':
                        login_user(user, remember=True)
                        flash(user.first_name + "- You are logged-in successfully !!", category='success')
                        return redirect(url_for('controllers.home'))
                    else:
                        flash('Your registration is not approved by admin yet !! Please contact admin !!', category='error')
                else:
                    flash('Wrong password !! Try again, or Please connect to admin !!', category='error')
            else:
                flash('Invalid email id !! Please try again!! If new user, then register first !!', category='error')
    return render_template('login.html', user=current_user)

@controllers.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged-out successfully !!")
    return redirect(url_for('controllers.login'))

@groups.route('/')
@login_required
def get_groups():
    group_ids = GroupUser.query.filter_by(user_id=current_user.id).all()
    list_of_groups = []
    for group_id in group_ids:
        list_of_groups.append(Group.query.filter_by(id=group_id.group_id).first())
    return render_template('group.html', user=current_user, groups=list_of_groups)

@groups.route('/add/<int:group_id>', methods=['GET', 'POST'])
@login_required
def add_member(group_id):
    if group_id:
        group = Group.query.filter_by(id=group_id).first()
        if group and group.admin_id == current_user.id:
            if request.method == 'POST':
                member_id = int(request.form.get('member'))
                group_members = GroupUser.query.filter_by(group_id=group.id).all()
                for member in group_members:
                    if member.user_id == member_id:
                        flash('User is already part of the group - '  + group.name + '!!', category='success')
                        return redirect(url_for('groups.get_groups'))
                group_user = GroupUser(user_id=member_id, group_id=group.id)
                db.session.add(group_user)
                db.session.commit()
                flash('User is added to the group successfully !!', category='success')
            else:
                users = User.query.filter(User.role_id != 3).all()
                return  render_template('add_member.html', user=current_user, users=users, group=group)
        else:
            flash('Invalid operation !! Unauthorized access !!', category='error')
    else:
        flash('Unknown URI is triggered !!', category='error')
    return redirect(url_for('groups.get_groups'))

@groups.route('/show/<int:group_id>')
@login_required
def show_member(group_id):
    if group_id:
        group = Group.query.filter_by(id=group_id).first()
        group_user = GroupUser.query.filter(GroupUser.user_id==current_user.id, GroupUser.group_id==group_id).first()
        if group and group_user:
            group_members = GroupUser.query.filter_by(group_id=group.id).all()
            return render_template('show_member.html', user=current_user, members=group_members, group=group)
        else:
            flash('Invalid operation !! Unauthorized access !!', category='error')
    else:
        flash('Unknown URI is triggered !!', category='error')
    return redirect(url_for('groups.get_groups'))

@groups.route('/remove/<int:group_id>', methods=['GET', 'POST'])
@login_required
def remove_member(group_id):
    if group_id:
        group = Group.query.filter_by(id=group_id).first()
        if group and group.admin_id == current_user.id:
            if request.method == 'POST':
                member_id = int(request.form.get('member'))
                member = GroupUser.query.filter(GroupUser.user_id==member_id, GroupUser.group_id==group.id).first()
                user_name = member.user.first_name
                db.session.delete(member)
                db.session.commit()
                flash(user_name + ' is removed from the group successfully !!', category='success')
            else:
                group_members = GroupUser.query.filter_by(group_id=group.id).all()
                return  render_template('remove_member.html', user=current_user, members=group_members, group=group)
        else:
            flash('Invalid operation !! Unauthorized access !!', category='error')
    else:
        flash('Unknown URI is triggered !!', category='error')
    return redirect(url_for('groups.get_groups'))

@groups.route('/update/<int:group_id>', methods=['GET', 'POST'])
@login_required
def update_group(group_id):
    if group_id:
        group = Group.query.filter_by(id=group_id).first()
        if group and group.admin_id == current_user.id:
            if request.method == 'POST':
                group_name = str(request.form.get('name')).strip()
                group_admin = int(request.form.get('admin'))
                if group_name:
                    new_group = Group.query.filter_by(name=group_name).first()
                    if new_group:
                       flash('Group name - ' + group_name + ' is already exist !! Try with some other name !!', category='error')
                    else:
                        group.name = group_name
                        group.admin_id = group_admin
                        db.session.commit()
                        flash('Group information is updated successfully !!', category='success')
                else:
                    flash('Invalid group name !!', category='error')
            else:
                group_members = GroupUser.query.filter_by(group_id=group.id).all()
                return render_template('update_group.html', user=current_user, group=group, members=group_members)
        else:
            flash('Invalid operation !! Unauthorized access !!', category='error')
    else:
        flash('Unknown URI is triggered !!', category='error')
    return redirect(url_for('groups.get_groups'))

@groups.route('/delete/<group_id>', methods=['GET', 'POST'])
@login_required
def delete_group(group_id):
    if group_id:
        group = Group.query.filter_by(id=group_id).first()
        if group and group.admin_id == current_user.id:
            if request.method == 'POST':
                group_name = group.name
                db.session.delete(group)
                db.session.commit()
                flash(group_name + ' is deleted successfully !!', category='success')
            else:
                return render_template('delete_group.html', user=current_user, group=group)
        else:
            flash('Invalid operation !! Unauthorized access !!', category='error')
    else:
        flash('Unknown URI is triggered !!', category='error')
    return redirect(url_for('groups.get_groups'))

@groups.route('/create', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        name = str(request.form.get('name')).strip()
        if name:
            admin = current_user.id
            new_group = Group.query.filter_by(name=name).first()
            if new_group:
                flash('Group name - ' + name + ' is already exist !! Try with some other name !!', category='error')
            else:
                group = Group(name=name, admin_id=admin)
                db.session.add(group)
                db.session.flush()
                db.session.refresh(group)
                group_user = GroupUser(user_id = admin, group_id = group.id)
                db.session.add(group_user)
                db.session.commit()
                flash('Group - ' + name + ' is create successfully !!', category='success')
                return redirect(url_for('groups.get_groups'))
        else:
            flash('Invalid group name !!', category='error')
    return render_template('create_group.html', user=current_user)