from Models.PaymentModel import PaymentModel
from Logger.Logger import log
from Schemas.PaymentSchema import PaymentSchema

class PaymentService:
    COLLECTION_NAME = 'payment'

    def __init__(self, payment_model):
        self.db = payment_model.db[self.COLLECTION_NAME]
        self.id_counter = payment_model.id_counter

    def get_payments_data(self, user_id: str):
        try:
            query = { "user_id": user_id }
            payment_data = list(self.db.find(query))
            return payment_data
        
        except Exception as e:
            error_msg = f'Error fetching the payments data from the database {e}'
            raise Exception(error_msg)

    def get_payment_data_by_id(self, payment_id: int):
        try:
            query = { "_id": payment_id }
            payment_data = list(self.db.find(query))
            return payment_data
        
        except Exception as e:
            error_msg = f'Error fetching the payment data with id {payment_id} from the database {e}'
            raise Exception(error_msg)
        
    def add_payment_data(self, payment_data):
        try:
            payment_data['_id'] = self.id_counter.get_next_id()

            return self.db.insert_one(payment_data)
        except Exception as e:
            error_msg = f'Error adding a new payment data: {e}'
            raise Exception(error_msg)
        
    def update_payment_data(self, payment_data, payment_id: int):
        try:
            filter = {'_id': payment_id}
            data = {"$set": payment_data}
            return self.db.update_one(filter, data)
        except Exception as e:
            error_msg = f'Error updating the payment data, with id {payment_id}: {e}'
            raise Exception(error_msg)
        
    def delete_payment_data(self, payment_id: int):
        try:
            filter = {'_id': payment_id}
            deleted_payment_data = self.db.delete_one(filter)
            if deleted_payment_data.deleted_count  > 0: 
                return True
            else:
                return False

        except Exception as e:
            error_msg = f'Error deleting the payment data, with id {payment_id}: {e}'
            raise Exception(error_msg)

if __name__ == '__main__':
    payment_model = PaymentModel()

    try:
        payment_model.connect_to_database()
        payment_service = PaymentService(payment_model)

        # # getting payment data from one user
        # user_id = "12345"
        # payment_data = payment_service.get_payments_data(user_id)
        # log.debug({'payment_data': payment_data})

        # # getting payment data from id
        # payment_id = 1
        # payment_data = payment_service.get_payment_data_by_id(payment_id)
        # log.debug({'payment_data': payment_data})

        # payment_data = {
        #     "user_id": "12345",
        #     "cardholder_name": "Alejandro Vazquez Sanchez",
        #     "card_number": "5555555555555555",
        #     "expiry_date": {
        #         "month": "12",
        #         "year": "2025"
        #     },
        #     "billing_address": {
        #         "street": "Calle Oyamel",
        #         "city": "Alvaro Obregon",
        #         "state": "Ciudad de Mexico",
        #         "postal_code": "01740",
        #         "country": "Mexico"
        #     }
        # }

        # data = PaymentSchema().load(payment_data)

        # new_payment_data = payment_service.add_payment_data(data)
        # log.debug({'new_payment_data': new_payment_data})

        # updating payment data
        # id = 1
        # new_payment_data = payment_service.update_payment_data(data, id)
        # log.debug({'new_payment_data': new_payment_data})
        
        # deleting payment data
        id = 1
        done = payment_service.delete_payment_data(id)
        msg = 'Payment data deleted' if done else f'Cannot delete payment data with id {id}'
        log.debug({'msg': msg})

    except Exception as e:
        log.critical({'errors': e})
    finally:
        payment_model.close_connection()