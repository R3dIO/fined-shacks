import logging

from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource
from firebase_admin import auth

from web_server import api, pb
from web_server.utils.auth import check_token

core_blueprint = Blueprint('core', __name__)

logger = logging.getLogger(__name__)


class Ping(Resource):
    def get(self):
        return jsonify({"message": "pong"})


class Signup(Resource):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        if email is None or password is None:
            return {'message': 'Error missing email or password'}, 400
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            return {'message': f'Successfully created user {user.uid}'}, 200
        except:
            return {'message': 'Error creating user'}, 400


class Logout(Resource):
    @check_token
    def get(self):
        return jsonify({"message": "pong"})


class Login(Resource):
    def get(self):
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = pb.auth().sign_in_with_email_and_password(email, password)
            jwt = user['idToken']
            return {'token': jwt}, 200
        except:
            return {'message': 'There was an error logging in'}, 400


api.add_resource(Ping, '/ping')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
