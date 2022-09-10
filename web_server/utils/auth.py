from functools import wraps
import json

from flask import request
from firebase_admin import auth

from web_server.common.constants import (FIREBASE_CONFIG_FILE, FIREBASE_CREDENTIALS)
from web_server.utils import pyrebase


pb = pyrebase.initialize_app(json.load(open(FIREBASE_CONFIG_FILE)))


def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'}, 400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message': 'Invalid token provided.'}, 400
        return f(*args, **kwargs)
    return wrap
