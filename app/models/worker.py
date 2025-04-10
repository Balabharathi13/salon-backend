from app.extensions import db
from bson.objectid import ObjectId

class WorkerModel:
    def __init__(self):
        # self.collection = db.db.workers
        self.collection = db['workers']

    def add_worker(self, data):
        return self.collection.insert_one(data)

    def get_workers_by_shop(self, shop_id):
        return list(self.collection.find({"shop_id": shop_id}))

    def get_worker_by_id(self, worker_id):
        return self.collection.find_one({"_id": ObjectId(worker_id)})

    def update_worker(self, worker_id, data):
        return self.collection.update_one({"_id": ObjectId(worker_id)}, {"$set": data})

    def delete_worker(self, worker_id):
        return self.collection.delete_one({"_id": ObjectId(worker_id)})
