import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret")
    # MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/saloon_db")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt_secret")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # 1 day
