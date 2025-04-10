from app.extensions import db
from bson import ObjectId

class UserModel:
    def __init__(self):
        # self.collection = db.db.users
        self.collection = db['users']

    def create_user(self, data):
        return self.collection.insert_one(data)

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})

    def find_by_id(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def update_token(self, user_id, refresh_token):
        return self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"refresh_token": refresh_token}}
        )

    def get_all_users(self):
        return list(self.collection.find())
