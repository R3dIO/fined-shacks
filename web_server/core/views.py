import logging

from flask import Blueprint, jsonify
from flask_restful import Resource

from web_server import api

core_blueprint = Blueprint('core', __name__)

logger = logging.getLogger(__name__)


class Ping(Resource):
    def get(self):
        return jsonify({"message": "pong"})


api.add_resource(Ping, '/ping')
