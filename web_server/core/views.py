import email
import json
import logging
import traceback

from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource
from firebase_admin import auth

from web_server import api
from web_server.utils.auth import pb, check_token
from web_server.core.helper import generate_tags_from_form
from web_server.core.models import save_user, retrieve_user_by_email, fetch_content, update_user_tags
from web_server.common.constants import (
    API_STATUS_ERROR, API_STATUS_FAILURE, API_STATUS_PARTIAL, API_STATUS_SUCCESS)

core_blueprint = Blueprint('core', __name__)

logger = logging.getLogger(__name__)


class Ping(Resource):
    def get(self):
        return jsonify({"message": "pong"})


class Signup(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        if email is None or password is None:
            return make_response(
                jsonify({'status': API_STATUS_ERROR,
                'message': 'Error missing email or password'}), 400)
        try:
            user = auth.create_user(
                display_name=first_name,
                email=email,
                password=password
            )
            if user.uid:
                save_user(uid=user.uid, email=email,
                          first_name=first_name, last_name=last_name)
            return make_response(
                jsonify({'status': API_STATUS_SUCCESS,
                        'message': f'Successfully created user {user.uid}'}), 200
            )
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
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
            return make_response(jsonify({'status': API_STATUS_SUCCESS, 'token': jwt}), 200)
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            return make_response(jsonify({'status': API_STATUS_ERROR, 'message': 'There was an error logging in'}), 400)


class SaveUserDetails(Resource):
    def post(self):
        user_details = request.json
        try:
            tags = generate_tags_from_form(user_details)
            # store tags in db
            update_user_tags(email=user_details['email'], tags=tags)
            return make_response(jsonify({'status': API_STATUS_SUCCESS, 'message': 'saved user information'}))
        except:
            return make_response(jsonify({'status': API_STATUS_ERROR, 'message': 'There was an error saving user details'}), 400)


class RetrieveAdviceContent(Resource):
    def post(self):
        user_email = request.json.get("email")
        page = request.json.get("page")
        per_page = request.json.get("per_page")
        try:
            user_details = retrieve_user_by_email(email=user_email)
            matched_content = fetch_content(
                tags=user_details["tags"], page=page, per_page=per_page)
            if matched_content:
                return make_response(jsonify({'status': API_STATUS_SUCCESS, 'matched_content': matched_content}))
            if not matched_content:
                default_content = fetch_content(
                    tags=['default'], page=page, per_page=per_page)
                return make_response(jsonify({'status': API_STATUS_SUCCESS, 'default_content': default_content}))
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            return make_response(jsonify({'status': API_STATUS_ERROR, 'message': e}), 500)


class AdviceFeedback(Resource):
    def post(self):
        user_email = request.json.get("email")
        page = request.json.get("page")
        per_page = request.json.get("per_page")
        # advice_id =
        try:
            user_details = retrieve_user_by_email(email=user_email)
            matched_content = fetch_content(
                tags=user_details["tags"], page=page, per_page=per_page)
            if matched_content:
                return make_response(jsonify({'status': API_STATUS_SUCCESS, 'matched_content': matched_content}))
            if not matched_content:
                default_content = fetch_content(
                    tags=['default'], page=page, per_page=per_page)
                return make_response(jsonify({'status': API_STATUS_SUCCESS, 'default_content': default_content}))
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            return make_response(jsonify({'status': API_STATUS_ERROR, 'message': e}), 500)


api.add_resource(Ping, '/ping')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(SaveUserDetails, '/save-user-details')
api.add_resource(RetrieveAdviceContent, '/advice')
api.add_resource(AdviceFeedback, '/feedback')
