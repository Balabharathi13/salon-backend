from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)


print(client)

# db = client['vi-admin-with-region']
db = client['my_database']
jwt = JWTManager()
bcrypt = Bcrypt()
cors = CORS()
ma = Marshmallow()
