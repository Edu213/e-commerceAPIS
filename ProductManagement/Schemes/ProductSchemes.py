from marshmallow import schema, fields, validates, ValidationError

class ProductSchemes:
    """Schema for validating product data"""

    product_id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=False)
    price = fields.Float(required=True)
    quantify = fields.Integer(required=True)
    category = fields.String(required=True)
    brand = fields.String(required=True)

    @validates('name')
    def validates_name(self, value):
        """Validate minimum length of product name"""
        if len(value) < 5:
            raise ValidationError('Product name must be at least five characteres long')

    @validates('description')
    def validates_description(self, value):
        """Validate minimum length for product description"""
        if value and len(value) < 10:
            raise ValidationError('Description must be at least ten characters long')
        
    @validates('price')
    def validates_price(self, value):
        """Validate that product price is greater than zero"""
        if value <= 0:
            raise ValidationError('Price must be greater than 0')

    @validates('quantity')
    def validates_quantify(self, value):
        """Validate that product quantity is a non-negative integer"""
        if value < 0:
            raise ValidationError('Quantify mus be a non-negative integer')

    @validates('category')
    def validates_category(self, value):
        """Validate minimum length of category name"""
        if len(value) < 5:
            raise ValidationError('Category name must be at least five characters long')

    @validates('brand')
    def validates_brand(self, value):
        """Validate minimum length of brand name"""
        if len(value) < 2:
            raise ValidationError('Brand must be at least two characters long')
            
