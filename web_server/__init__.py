import datetime
import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_restful import Api


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['DB_NAME'] = os.environ.get('DB_NAME')

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

JWT_ACCESS_TOKEN_TIMEDELTA = datetime.timedelta(minutes=20)
JWT_REFRESH_TOKEN_TIMEDELTA = datetime.timedelta(hours=6)

mongo = PyMongo(app)

api = Api(app)

CORS(app)
