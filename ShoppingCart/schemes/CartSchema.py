from marshmallow import Schema, fields
from .ProductSchema import ProductSchema

class CartSchema(Schema):
    user_id = fields.Integer(required=True)
    products = fields.List(fields.Nested(ProductSchema))