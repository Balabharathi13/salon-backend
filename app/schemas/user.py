from marshmallow import Schema, fields, validate

class UserUpdateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    role = fields.String(required=True, validate=validate.OneOf(["customer", "shop_owner", "admin"]))
