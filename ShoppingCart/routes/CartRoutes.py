from flask import Blueprint, jsonify, request
from logger.LoggerBase import log
from services.CartService import CartService
from schemes.ProductSchema import ProductSchema
from marshmallow import ValidationError

class CartRoutes(Blueprint):
    def __init__(self, cart_service: CartService):
        super().__init__('Carts', __name__)
        self.cart_service = cart_service
        self.register_routes()

    def register_routes(self):
        self.route('/api/cart/<int:user_id>', methods=['GET'])(self.get_user_cart)
        self.route('/api/cart/product/<int:user_id>', methods=['POST'])(self.add_product_to_cart)
        self.route('/api/cart/total/<int:user_id>', methods=['GET'])(self.get_total_price)
        self.route('/healthcheck')(self.healthcheck)

    def get_user_cart(self, user_id):
        try:
            cart = self.cart_service.get_user_car(user_id)
            return jsonify(cart), 200
        
        except Exception as error_msg:
            log.critical(error_msg)
            return jsonify({'error': str(error_msg)}), 500
        
    def add_product_to_cart(self, user_id):
        try:
            req_body = request.get_json()

            if not req_body:
                return jsonify({'error': 'Invalid data'})
            
            product = ProductSchema().load(req_body)
            new_car = self.cart_service.add_product_to_car(user_id, product)
            
            if new_car == None:
                msg = f"Cannot add the product to the cart from user with id {user_id}"
                log.critical(msg)
                return jsonify('error:', msg)
            
            return jsonify({'message': 'product added succesfully'}), 201
    
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        
        except Exception as error_msg: 
            log.critical(error_msg)

            return jsonify({'error': str(error_msg)}), 500

    def get_total_price(self, user_id):
        try:
            total_price = self.cart_service.calculate_total_price(user_id)
            return jsonify({'total_price': total_price}), 200
        
        except Exception as error_msg:
            log.critical(error_msg)
            return jsonify({'error': str(error_msg)}), 500
        
    def healthcheck(self):
        return jsonify({'status': 'up'})