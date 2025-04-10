from app.extensions import ma
from marshmallow import fields, validate

class RegisterSchema(ma.Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(required=True, validate=validate.OneOf(["customer", "shop_owner"]))

class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
