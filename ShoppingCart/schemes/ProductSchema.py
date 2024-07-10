from marshmallow import Schema, fields

class ProductSchema(Schema):
    """Schema for validating product data"""

    product_id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=False)
    price = fields.Float(required=True)
    category = fields.String(required=True)
    brand = fields.String(required=True)