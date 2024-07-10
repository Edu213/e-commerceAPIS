from marshmallow import Schema, fields, validate

class OrderSchema(Schema):
    """Schema for validating order data."""
    
    _id = fields.Integer(required=True)
    customer_id = fields.String(required=True)
    products = fields.List(fields.Dict(keys=fields.String(), values=fields.Raw()), required=True)
    total_price = fields.Float(required=True)
    status = fields.String(required=True, validate=validate.OneOf(['pending', 'shipped', 'delivered'])) 
    tracking_info = fields.Dict(keys=fields.String(), values=fields.Raw(), required=True)
