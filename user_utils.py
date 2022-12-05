from google.cloud import datastore
import os
import hashlib


def get_client():
    """Get the Client object for the datastore."""

    return datastore.Client()


def verify_password(given, actual):
    salt = actual[:32]
    key = actual[32:]

    to_check = hashlib.pbkdf2_hmac(
        'sha256', given.encode('utf-8'), salt, 100000)

    if key == to_check:
        return True
    else:
        return False


def new_user(email, first_name, last_name, password):
    """Create a new user"""
    client = get_client()
    key = client.key('user')
    entity = datastore.Entity(key)
    entity.update(
        {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password
        }
    )

    client.put(entity)


def get_user(email):
    """Get user information from the DB"""
    client = get_client()
    query = client.query(kind='user')
    query.add_filter('email', '=', email)
    result = query.fetch()

    try: 
        user = next(result)
    except:
        user = None

    return user


def generate_password_hash(password):
    """Hash the password given by the user."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    stored = salt + key

    return stored
