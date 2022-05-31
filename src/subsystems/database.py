from flask_pymongo import PyMongo

from ..app import app

mongodb_client = PyMongo(app)
