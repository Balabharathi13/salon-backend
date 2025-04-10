from app.extensions import db
from bson.objectid import ObjectId

class ShopModel:
    def __init__(self):
        # self.collection = db.db.shops
        self.collection = db['shops']

    def register_shop(self, data):
        return self.collection.insert_one(data)

    def get_shop_by_owner(self, owner_id):
        return self.collection.find_one({"owner_id": owner_id})

    def approve_shop(self, shop_id):
        return self.collection.update_one({"_id": ObjectId(shop_id)}, {"$set": {"approved": True}})

    def get_approved_shops(self):
        return list(self.collection.find({"approved": True}))

    def get_all_shops(self):
        return list(self.collection.find())

    def find_by_location(self, location):
        return list(self.collection.find({"location": location, "approved": True}))
