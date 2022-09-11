import logging

from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource
from firebase_admin import auth

from web_server import api,app
from web_server.utils.auth import pb, check_token
from web_server.core.models import save_user
from web_server.core.helper import generate_tags_from_form


core_blueprint = Blueprint('core', __name__)

logger = logging.getLogger(__name__)


class Ping(Resource):
    def get(self):
        return jsonify({"message": "pong"})


class Signup(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        if email is None or password is None:
            return {'message': 'Error missing email or password'}, 400
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            save_user(uid=user.uid, email=email)
            return {'message': f'Successfully created user {user.uid}'}, 200
        except:
            return {'message': 'Error creating user'}, 400


class Logout(Resource):
    @check_token
    def get(self):
        return jsonify({"message": "pong"})


class Login(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        try:
            user = pb.auth().sign_in_with_email_and_password(email, password)
            jwt = user['idToken']
            return {'token': jwt}, 200
        except:
            return {'message': 'There was an error logging in'}, 400


class SaveUserDetails(Resource):
    def post(self):
        print(request)
        user_details = request.json
        print(user_details)
        try:
            tags = generate_tags_from_form(user_details)
            print(tags)

            # store tags in db
        except:
            return {'message': 'There was an error logging in'}, 400



api.add_resource(Ping, '/ping')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(SaveUserDetails, '/submit')
