from marshmallow import Schema, fields, validate

class ReviewSchema(Schema):
    shop_id = fields.String(required=True)
    rating = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.String(required=False)
