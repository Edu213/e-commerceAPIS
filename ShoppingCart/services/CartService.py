from logger.LoggerBase import log
from models.CartModel import CartModel
from pymongo import ReturnDocument

class CartService:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_user_car(self, user_id):
        try:
            log.debug(user_id)
            query = {'user_id': str(user_id)}
            cart = self.db_conn.db.cars.find_one(query)
            log.debug({'cart': cart})

            return cart
        
        except Exception as e:
            error_msg = f'Error fetching cart from the database {e}'
            raise Exception(error_msg)

    def add_product_to_car(self, user_id, product):
        try:
            # Check if there is a cart linked to an user
            cart = self.get_user_car(user_id)

            # if there is no cart linked to an user, we create a new one
            if cart is None:
                cart_id = self.db_conn.id_counter.get_next_id()
                cart = {
                    '_id': cart_id,
                    'user_id': str(user_id),
                    'products': [product]
                }
                self.db_conn.db.cars.insert_one(cart)
            
            # Add the product to the cart
            updated_car = self.db_conn.db.cars.find_one_and_update(
                {'user_id': str(user_id)},
                {'$push': {'products': product}},
                return_document=ReturnDocument.AFTER
            )

            return updated_car

        except Exception as e:
            log.critical(e.messages)
            error_msg = f'Error fetching cart from the database {e}'
            raise Exception(error_msg)

    def calculate_total_price(self, user_id):
        try:
            # Check if there is a cart linked to an user
            cart = self.get_user_car(user_id)
            log.debug(cart)
            total_price = 0

            for product in cart['products']:
                log.debug(f"Name: {product['name']} Price: {product['price']}")
                total_price = total_price + float(product['price'])
            
            log.debug({'total_price': total_price})

            return total_price
        except Exception as e: 
            error_msg = f'Error fetching cart from the database {e}'
            raise Exception(error_msg)

if __name__ == '__main__':
    db = CartModel()
    db.connect_to_database()

    CartService(db).calculate_total_price('12345')
