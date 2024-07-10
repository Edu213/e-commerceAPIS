from flask import jsonify
from Logger.LoggerProduct import log

class ProductServices:
    """
    ProductServices provides methods to interact with the product related 
    operations in the MongoDB database.

    Attributes:
        db_connector: The database connector instance to interact with MongoDB.
    """
    def __init__(self, db_connector):
        """
        Initializes ProductServices with the databse connector and counter for ID.

        Args: 
            db_connector: An instance of the database connector.
        """
        self.db_connector = db_connector
        self.initialize_counter()

    def initialize_counter(self):
        """
        Initialize the counter in the database if it doesn't already exist.
        """
        self.db = self.db_connector.db
        self.counters = self.db['Identifiers']

        if self.counters.count_documents({}) == 0:
            self.counters.insert_one({'_id': 'product_id', 'seq': 0})
        
    def next_value(self, sequence):
        """
        Gets the next value of the counter (ID) and increments it by one.

        Args:
            sequence (str): The name of the counter.
        Returns:
            int: The next value of the counter (ID)
        """
        sequence_document = self.counters.find_one_and_update(
            {'_id': sequence},
            {'$inc': {'seq': 1}},
            return_document=True
        )
        return sequence_document['seq']

    def get_all_products(self):
        """
        Fetches all products from the database.

        Returns:
            A list of products if successful, or an error message with a 500 status code if an exception occurs.
        """
        try:
            self.products = list(self.db_connector.db.Inventory.find())
            return self.products
        except Exception as e:
            log_message = f'Error fetching all products from the database: {e}'
            log.critical(log_message)
            return jsonify({'error': log_message}), 500
        
    def get_product_by_id(self, product_id):
        """
        Fetches a product from the database by its ID.

        Args:
            product_id: The ID of the product to fetch.

        Returns:
            The product if found, or an error message with a 500 status code if an exception occurs.
        """
        try: 
            self.product = self.db_connector.db.Inventory.find_one({'_id': product_id})
            return self.product
        except Exception as e:
            log_message = f'Error fetching the product id from the database: {e}'
            log.critical(log_message)
            return jsonify({'error': log_message}), 500
    
    def add_product(self, new_product):
        """
        Adds a new product to the database.

        Args:
            new_product: A dictionary representing the new product to add.
        
            Returns: 
                A success message with a 200 status code if successful, or an error message with a 500 status code if an exception occurs.
        """
        try:
            new_product['_id'] = self.next_value('product_id')
            self.new_product = self.db_connector.db.Inventory.insert_one(new_product)
            return jsonify({'message': 'Product created succesfully'}), 200
        except Exception as e:
            log_message = f'Error creating new product: {e}'
            log.critical(log_message)
            return jsonify({'error': log_message}), 500
        
    def update_product(self, product_id, updated_data):
        """
        Updates an existing product in the database.

        Args:
            updated_data: A dictionary with the updated product data.
            product_id: The ID of the product to update.

        Returns: 
            A success message with a 200 status code if successful, or an error message if the product is not found or if an exception occurs.
        """
        try:
            existing_product = self.db_connector.db.Inventory.find_one({'_id': product_id})
            print("Hola", product_id)
            if existing_product:
                self.updated_data = self.db_connector.db.Inventory.update_one({'_id': product_id}, {'$set': updated_data})
                return jsonify({'message': 'Product updated successfully'}), 200
            else:
                return jsonify({'error': 'Product with the given ID not found'}), 404
        except Exception as e:
            log_message = f'Error updating product: {e}'
            log.critical(log_message)
            return jsonify({'error': log_message}), 500
        
    def delete_product(self, product_id):
        """
        Deletes a product from the database.

        Args: 
            product_id: The ID of the product to delete.

        Returns: 
            A success message with a 200 status code if successful, or an error message if the product is not found or if an exception occurs.
        """
        try:
            existing_product = self.db_connector.db.Inventory.find_one({'_id': product_id})
            if existing_product:
                self.db_connector.db.Inventory.delete_one({'_id': product_id})
                return jsonify({'message': 'Product deleted successfully'}), 200
            else:
                return jsonify({'error': 'Product with the given ID not found'}), 404
        except Exception as e:
            log_message = f'Error deleting product: {e}'
            log.critical(log_message)
            return jsonify({'error': log_message}), 500
        
            
        

        
            
