from app.extensions import db
from bson.objectid import ObjectId
from datetime import datetime

class BookingModel:
    def __init__(self):
        # self.collection = db.db.bookings
        self.collection = db['bookings']

    def create_booking(self, data):
        return self.collection.insert_one(data)

    def get_bookings_by_customer(self, customer_id):
        return list(self.collection.find({"customer_id": customer_id}))

    def get_bookings_by_shop(self, shop_id):
        return list(self.collection.find({"shop_id": shop_id}))

    def get_booking_by_id(self, booking_id):
        return self.collection.find_one({"_id": ObjectId(booking_id)})

    def update_status(self, booking_id, status):
        return self.collection.update_one({"_id": ObjectId(booking_id)}, {"$set": {"status": status}})

    def assign_worker(self, booking_id, worker_id):
        return self.collection.update_one({"_id": ObjectId(booking_id)}, {"$set": {"worker_id": worker_id}})

    def get_bookings_by_slot(self, shop_id, date, slot):
        return list(self.collection.find({
            "shop_id": shop_id,
            "date": date,
            "slot": slot
        }))
