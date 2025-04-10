from app.extensions import ma
from marshmallow import fields

class BookingSchema(ma.Schema):
    shop_id = fields.Str(required=True)
    service = fields.Str(required=True)
    date = fields.Str(required=True)       # format: YYYY-MM-DD
    slot = fields.Str(required=True)       # e.g. "10:00-10:30"
