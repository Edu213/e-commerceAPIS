from marshmallow import Schema, fields

class ExpiryDateSchema(Schema):
    month = fields.Str(required=True)
    year = fields.Str(required=True)