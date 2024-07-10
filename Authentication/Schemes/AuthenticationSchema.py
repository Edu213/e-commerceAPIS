from marshmallow import Schema, fields, validate

class AuthenticationSchema(Schema):
    """Schema for validating authentication data.

    Attributes:
        email (fields.Email): A field representing the email address of the user.
            It is required and must be a valid email address.
        password (fields.Str): A field representing the password of the user.
            It is required and must be a string with a minimum length of 8 characters.
    """
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
