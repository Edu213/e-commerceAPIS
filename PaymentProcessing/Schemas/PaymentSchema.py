from marshmallow import Schema, fields, ValidationError
from .ExpiringDateSchema import ExpiryDateSchema
from .BillingAddresSchema import BillingAddressSchema
from Logger.Logger import log
from datetime import datetime

class PaymentSchema(Schema):
    user_id = fields.Str(required=True)
    cardholder_name = fields.Str(required=True)
    card_number = fields.Str(required=True)
    expiry_date = fields.Nested(ExpiryDateSchema)
    billing_address = fields.Nested(BillingAddressSchema)
    registered_at = fields.DateTime(load_default=datetime.now)

if __name__ == '__main__':
    data = {
        "user_id": "12345",
        "cardholder_name": "Erick Vazquez",
        "card_number": "4111111111111111",
        "expiry_date": {
            "month": "12",
            "year": "2025"
        },
        "billing_address": {
            "street": "Calle Oyamel",
            "city": "Alvaro Obregon",
            "state": "Ciudad de Mexico",
            "postal_code": "01740",
            "country": "Mexico"
        }
    }

    payment_schema = PaymentSchema()

    try:
        payment_object = payment_schema.load(data)
        log.debug({'payment_object': payment_object})
    except ValidationError as err:
        log.debug({'errors': err.messages})