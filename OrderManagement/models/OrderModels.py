
import os

from pymongo import MongoClient
from logger.logger_base import log
import os

class OrderModel:
    """Class representing a model for interacting with orders in a MongoDB database."""
    
    def __init__(self):
        """Initialize OrderModel."""
        self.client = None
        self.db = None

    def connect_to_database(self):
        """Connect to the MongoDB database."""
        mongodb_user = os.environ.get('MONGODB_USER')
        mongodb_pass = os.environ.get('MONGODB_PASS')
        mongodb_host = os.environ.get('MONGODB_HOST')

        missing_vars = [var for var, val in locals().items() if val is None]
        if missing_vars:
            missing_vars_str = ', '.join(missing_vars)
            log.critical(f'Variables required but not found: {missing_vars_str}')
            raise ValueError(f'Set environment variables: {missing_vars_str}')

        try:
            self.client = MongoClient(
                host=mongodb_host,
                port=27017,
                username=mongodb_user,
                password=mongodb_pass,
                authSource='admin',
                authMechanism='SCRAM-SHA-256',
                serverSelectionTimeoutMS=5000
            )
            self.db = self.client['orders']
            if self.db.list_collection_names():
                log.info('Connected to MongoDB database successfully')
        except Exception as e:
            log.critical(f'Failed to connect to the database: {e}')
            raise 

    def close_connection(self):
        """Close the connection to the MongoDB database."""
        if self.client:
            self.client.close()

if __name__ == '__main__':
    order_connection = OrderModel()
    try:
        order_connection.connect_to_database()
        log.info('Connection to the database was successful')
    except Exception as e:
        log.critical(f'An error occurred: {e}')
    finally:
        order_connection.close_connection()
        log.info('Connection to the database was successfully closed')
