from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from user_utils import get_user, generate_password_hash, new_user, verify_password

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    """Display the login page."""
    return render_template('login.html', page_title='Login')


@auth.route('/login', methods=['POST'])
def login_post():
    """Send a login request to the DB and log the user into the current session."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = get_user(email)

    if not user or not verify_password(password, user['password']):
        flash('Incorrect email or password.')
        return redirect(url_for('auth.login'))

    session['loggedin'] = True
    session['email'] = user['email']
    session['first_name'] = user['first_name']
    session['last_name'] = user['last_name']
    session['data_loaded'] = False

    return redirect(url_for('root'))


@auth.route('/signup')
def signup():
    """Show sign up page. Sends styles for list of favorite style to choose from."""

    return render_template('signup.html', page_title='Signup')


@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():
    """Process the signup form. Checks if the email is already used and hashes their password."""
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    user = get_user(email)

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    hashed_password = generate_password_hash(password)
    new_user(email, first_name, last_name, hashed_password)

    return redirect(url_for('auth.login'))


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    """Log out the current user."""
    session.pop('loggedin', None)
    session.pop('email')
    session.pop('first_name')
    session.pop('last_name')
    session.pop('data_loaded')

    return redirect(url_for('auth.login'))
