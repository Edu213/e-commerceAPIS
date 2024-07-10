import os
from pymongo import MongoClient
from Logger.Logger import log

class AutoIncrementId:
    def __init__(self, db, collection_name):
        self.counter_collection = db[collection_name]
        self.collection_name = collection_name

    def get_next_id(self):
        counter_document = self.counter_collection.find_one_and_update({}, {'$inc': {'counter': 1}}, upsert=True, return_document=True)
        return counter_document['counter']

class PaymentModel:
    COLLECTION_NAME = 'payment_data'

    def __init__(self):
        self.client = None
        self.db = None
        self.id_counter = None

    def connect_to_database(self):
        mongodb_user = os.environ.get('MONGODB_USER')
        mongodb_pass = os.environ.get('MONGODB_PASS')
        mongodb_host = os.environ.get('MONGODB_HOST')

        missing_vars = [var for var, val in locals().items() if val is None]
        if missing_vars:
            missing_vars_str = ', '.join(missing_vars)
            log.critical(f'Variables required not found: {missing_vars_str}')
            raise ValueError(f'Set enviroment variables: {missing_vars_str}')
        
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

            self.db = self.client[self.COLLECTION_NAME]
            self.id_counter = AutoIncrementId(self.db, 'id_counter')
            if self.db.list_collection_names():
                log.info('Connected to MongoDB succesfully')
        except Exception as e:
            log.critical(f'Failed to connect to MongoDB: {e}')
            raise
            
    def close_connection(self):
        if self.client:
            self.client.close()

if __name__ == '__main__':
    payment_model = PaymentModel()
    try:
        payment_model.connect_to_database()
    except Exception as e:
        log.critical(e)
    finally:
        payment_model.close_connection()
        log.info('Connection close')