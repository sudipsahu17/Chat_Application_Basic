from flask import Blueprint, request, render_template

controllers = Blueprint('controllers', __name__)

@controllers.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        pass
    return render_template('signup.html')

@controllers.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('login.html')

@controllers.route('/logout')
def logout():
    return render_template('home.html')

