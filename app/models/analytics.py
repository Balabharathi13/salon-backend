from app.extensions import db
from bson.objectid import ObjectId
from datetime import datetime, timedelta

class AnalyticsModel:
    def __init__(self):
        # self.bookings = db.db.bookings
        self.bookings = db['bookings']
        # self.workers = db.db.workers
        self.workers = db['workers']

    def get_booking_stats(self, shop_id):
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        week_ago = today - timedelta(days=7)

        def count_from(date):
            return self.bookings.count_documents({"shop_id": shop_id, "date": {"$gte": date}})

        return {
            "today": count_from(today),
            "yesterday": count_from(yesterday),
            "this_week": count_from(week_ago)
        }

    def get_worker_performance(self, shop_id):
        pipeline = [
            {"$match": {"shop_id": shop_id}},
            {"$group": {
                "_id": "$worker_id",
                "total_tasks": {"$sum": 1}
            }},
            {"$lookup": {
                "from": "workers",
                "localField": "_id",
                "foreignField": "_id",
                "as": "worker_info"
            }},
            {"$unwind": "$worker_info"},
            {"$project": {
                "worker_name": "$worker_info.name",
                "total_tasks": 1
            }}
        ]
        return list(self.bookings.aggregate(pipeline))
