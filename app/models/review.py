from app.extensions import db
from bson import ObjectId

class ReviewModel:
    def __init__(self):
        # self.collection = db.db.reviews
        self.collection = db['reviews']

    def add_review(self, data):
        return self.collection.insert_one(data)

    def get_reviews_by_shop(self, shop_id):
        reviews = self.collection.find({"shop_id": shop_id})
        return [{
            "_id": str(r["_id"]),
            "customer_id": str(r["customer_id"]),
            "shop_id": r["shop_id"],
            "rating": r["rating"],
            "comment": r.get("comment", "")
        } for r in reviews]
