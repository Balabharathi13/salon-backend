from app.extensions import ma
from marshmallow import fields

class WorkerSchema(ma.Schema):
    name = fields.Str(required=True)
    contact = fields.Str(required=True)
    experience = fields.Int(required=True)
