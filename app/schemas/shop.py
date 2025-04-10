from app.extensions import ma
from marshmallow import fields, validate

class ShopRegisterSchema(ma.Schema):
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    seats = fields.Int(required=True)
    workers = fields.Int(required=True)
    open_time = fields.Str(required=True)
    close_time = fields.Str(required=True)
    lunch_time = fields.Str(required=True)
    slots_per_hour = fields.Int(required=True)
    fee_structure = fields.Str(required=True)
    proof = fields.Str(required=True)  # image/file placeholder
