from flask import Blueprint, jsonify, request
from Logger.LoggerProduct import log
from Services.ProductServices import ProductServices

class ProductRoutes(Blueprint):
    """
    Blueprint subclass for handling product related routes.

    Args:
        product_service (PorductServices): An instance of the ProductServices class for handling product related operations.

    Attributes:
        product_service (ProducServices): An instance of ProductServices class.

    """
    def __init__(self, product_service):
        """
        Initialize ProductRoutes instance.

        Args: 
            product_service (ProductServices): An instance of ProductServices
        """
        super().__init__('product', __name__)
        self.product_service = product_service
        self.register_routes()

    def register_routes(self):
        """
        Register routes for product related operations.
        """
        self.route('/products', methods=['GET'])(self.get_products)
        self.route('/products/<int:product_id>', methods=['GET'])(self.get_product_by_id)
        self.route('/products', methods=['POST'])(self.add_product)
        self.route('/products/<int:product_id>', methods=['PUT'])(self.update_product)
        self.route('/products/<int:product_id>', methods=['DELETE'])(self.delete_product)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    def get_products(self):
        """
        Retrieve all products from the database.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        try: 
            self.products = self.product_service.get_all_products()
            return jsonify(self.products), 200
        except Exception as e:
            log_message = f'Error fetching data from the database: {e}'
            log.exception(log_message)
            return jsonify({'error': log_message}), 500
        
    def get_product_by_id(self, product_id):
        """
        Retrieve product by its ID from the database.

        Args:
            product_id (int): The ID of the product to retrieve.
        
        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        try:
            self.product = self.product_service.get_product_by_id(product_id)
            if self.product:
                return jsonify(self.product), 200
            else: 
                return jsonify({'error': 'Product not found'}), 404
        except Exception as e:
            log_message = f'Error fetching data from the database: {e}'
            log.exception(log_message)
            return jsonify({'error': log_message}), 500
        
    def add_product(self):
        """
        Add a new product to the database

        Returns:
            tuple: A tuple containing JSON response and HTTP status code. 
        """
        try:
            request_body = request.get_json()

            if not request_body:
                return jsonify({'error': 'Invalid data'}), 400

            new_product = {
                'name': request_body.get('name'),
                'description': request_body.get('description'), 
                'price': request_body.get('price'),
                'quantity': request_body.get('quantity'),
                'category': request_body.get('category'),
                'brand': request_body.get('brand')
            }            

            created_product = self.product_service.add_product(new_product)
            return jsonify(created_product), 201
        except Exception as e:
            log_message = f'Error putting data in database: {e}'
            log.exception(log_message)
            return jsonify({'error': log_message}), 500
        
    def update_product(self, product_id):
        """
        Update product information in the database.

        Args: 
            product_id (int): The ID of the product to update.
        
            Returns:
                tuple: A tuple containing JSON response and HTTP status code. 
        """
        try:
            request_body = request.get_json()

            if not request_body:
                return jsonify({'error': 'Invalid data'}), 400

            updated_data = {
                'name': request_body.get('name'),
                'description': request_body.get('descriptioin'), 
                'price': request_body.get('price'),
                'quantity': request_body.get('quantity'),
                'category': request_body.get('category'),
                'brand': request_body.get( 'brand')
            }            

            update_product = self.product_service.update_product(product_id, updated_data)
            return update_product
        except Exception as e:
            log_message = f'Error updating information: {e}'
            log.exception(log_message)
            return jsonify({'error': log_message}), 500
        
    def delete_product(self, product_id):
        """
        Delete a product from the database.

        Args:
            product_id (int): The ID of the product to delete.

        Returns: 
            tuple: A tuple containing JSON response and HTTP status code.
        """
        deleted_product = self.product_service.delete_product(product_id)
        return deleted_product
    def healthcheck(self):
        """
        Perform a health check of the application.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        return jsonify({'status': 'UP'}), 200
