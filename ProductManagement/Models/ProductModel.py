import os
from pymongo import MongoClient
from Logger.LoggerProduct import log


class ProductModel:
    """
    ProductModel handles the connection to the MongoDB database for product related operations.
    """

    def __init__(self):
        """
        Initializes the ProductModel with attributes for the database client and connection.
        """
        self.client = None
        self.db = None
    
    def connect_to_database(self):
        """
        Connects to the MongoDB database using credentials from environment variables.

        Environment variables:
        - MONGODB_USERNAME: Username for MongoDB.
        - MONGODB_PASSWORD: Password for MongoDB.
        - MONGODB_HOST: Host address for MongoDB

        Raises:
            ValueError: If required environment variables are not set.
            Exception: If the connection to the database fails.
        """

        mongodb_username = os.environ.get('MONGODB_USERNAME')
        mongodb_password = os.environ.get('MONGODB_PASSWORD')
        mongodb_host = os.environ.get('MONGODB_HOST')

        missing_vars = [var for var, val in locals().items() if val is None]
        if missing_vars:
            missing_vars_str = ', '.join(missing_vars)
            log.critical(f'Variables required but not found: {missing_vars_str}')
            raise ValueError(f'Set environment variables: {missing_vars_str}')
        
        try:
            self.client = MongoClient(
                host = mongodb_host,
                port = 27017,
                username = mongodb_username,
                password = mongodb_password,
                authsource = 'admin',
                authMechanism = 'SCRAM-SHA-256', 
                serverSelectionTimeoutMS = 5000 
            )
            self.db = self.client['Products']
            if self.db.list_collection_names():
                log.info('Connected to MongoDB database successfully')
        except Exception as e:
            log.critical(f'Failed to connect to the database: {e}')
            raise

    def close_connection(self):
        """
        Closes the connection to the MongoDB database if it is open.
        """
        if self.client:
            self.client.close()
    
if __name__ == '__main__':
    """
    Main entry point for testing the connection to the MongoDB database.
    """
    comp_conn = ProductModel()
    try:
        comp_conn.connect_to_database()
        log.info('Connection to database was successful')
    except Exception as e:
        log.critical(f'An error occurred: {e}')
    finally:
        comp_conn.close_connection()
        log.info('Connection to database was successfully closed')