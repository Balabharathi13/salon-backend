from flask import Flask
from .config import Config
from .extensions import db, jwt, bcrypt, cors, ma
from .routes import register_blueprints
import pymongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    # global mongo_client, mongo_db
    # mongo_client = pymongo.MongoClient("mongodb://localhost:27017/pure_relax_db")
    # db = mongo_client.get_default_database()
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    ma.init_app(app)

    # Register Blueprints
    register_blueprints(app)

    return app
