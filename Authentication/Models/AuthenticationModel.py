"""Module for managing user authentication and database connection.

This module contains classes and methods for handling user authentication,
connecting to a MongoDB database, and managing database operations related
to user authentication. It includes a class `AuthenticationModel` for
managing the MongoDB connection and a script that can be run independently
to establish and close the database connection.

Classes:
    AuthenticationModel: A class for managing authentication data and database connection.

Scripts:
    if __name__ == '__main__': A script to instantiate and use the AuthenticationModel class.
"""

import os
from pymongo import MongoClient
from Logger.LoggerBase import log

class AuthenticationModel:
    """Class for managing authentication data and database connection."""

    def __init__(self):
        """Initialize the AuthenticationModel."""
        self.client = None
        self.db = None

    def connect_to_database(self):
        """Connect to the MongoDB database.

        This method retrieves necessary environment variables for MongoDB connection.
        It sets up the MongoDB client with the provided credentials and initializes the database.
        Raises:
            ValueError: If required environment variables are not set.
            Exception: If connection to MongoDB fails.
        """
        mongodb_user = os.environ.get('MONGODB_USER')
        mongodb_pass = os.environ.get('MONGODB_PASS')
        mongodb_host = os.environ.get('MONGODB_HOST')

        missing_vars = [var for var, val in locals().items() if val is None]
        if missing_vars:
            missing_vars_str = ', '.join(missing_vars)
            log.critical(f'Variables required not found: {missing_vars_str}')
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

            self.db = self.client['Authentication'] 
            if 'Users' in self.db.list_collection_names():
                log.info('Connected to MongoDB successfully')
            else:
             log.critical('Collection "Users" not found in the database')
        except Exception as e:
            log.critical(f'Failed to connect to MongoDB: {e}')
            raise
            
    def close_connection(self):
        """Close the connection to the MongoDB database."""
        if self.client:
            self.client.close()
    
if __name__ == '__main__':
    authentication_connection = AuthenticationModel()
    try:
        authentication_connection.connect_to_database()
        log.info('Connected to database')
    except Exception as e:
        log.critical(f'Error: {e}')
    finally:
        authentication_connection.close_connection()
        log.info('Connection closed')
