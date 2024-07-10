from flask import Blueprint, jsonify, request
from Logger.Logger import log
from Services.PaymentService import PaymentService
from Schemas.PaymentSchema import PaymentSchema
from marshmallow import ValidationError

class PaymentRoutes(Blueprint):
    def __init__(self,payment_service: PaymentService):
        super().__init__('payments', __name__)
        self.payment_service = payment_service
        self.register_routes()

    def register_routes(self):
        self.route('/api/payments', methods=['GET'])(self.get_payments)
        self.route('/api/payments/<int:payment_id>', methods=['GET'])(self.get_payment_by_id)
        self.route('/api/payments', methods=['POST'])(self.add_payment)
        self.route('/api/payments/<int:payment_id>', methods=['PUT'])(self.update_payment)
        self.route('/api/payments/<int:payment_id>', methods=['DELETE'])(self.delete_payment)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    def get_payments(self):
        try:
            user_id = request.args.get('user_id')

            if user_id == None:
                return jsonify({'error': 'User id not provided'}), 400

            payments = self.payment_service.get_payments_data(user_id)
            return jsonify(payments)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_payment_by_id(self, payment_id):
        try:
            payment_data = self.payment_service.get_payment_data_by_id(payment_id)

            if payment_data == None:
                return jsonify({'error': f'Cannot found payment with id: {payment_id}'}), 404
            
            return jsonify({'payment_data': payment_data}), 201
        
        except Exception as error:
            return jsonify({'error': str(error)}), 500
    
    def add_payment(self):
        try:
            req_body = request.get_json()

            if not req_body:
                return jsonify({'error': 'Invalid data'}), 400
            
            data = PaymentSchema().load(req_body)
            new_payment = self.payment_service.add_payment_data(data)
            
            if new_payment == None:
                msg = "Cannot add the payment in the datebase"
                return jsonify('error:', msg), 404
            
            return jsonify({'message': 'Payment added successfully'}), 201

        except ValidationError as e:
            # 400 -> bad request
            return jsonify({'error': e.messages}), 400
        
        except Exception as error:
            error_msg = str(error)
            return jsonify({'error': error_msg}), 500

    def update_payment(self, payment_id: int):
        try:
            req_body = request.get_json()

            if not req_body:
                return jsonify({'error': 'Invalid data'}), 400
            data = PaymentSchema().load(req_body)
            updated_payment = self.payment_service.update_payment_data(data, payment_id)
            
            if updated_payment == None:
                msg = f"Payment with id {payment_id} not found", 404
                return jsonify('error:', msg)
            
            return jsonify({'message': 'Payment updated succesfully'}), 201

        except ValidationError as e:
            # 400 -> bad request
            return jsonify({'error': e.messages}), 400
        
        except Exception as error: 
            error_msg = str(error)
            return jsonify({'error': error_msg}), 500

    def delete_payment(self, payment_id: int):
        try:
            done = self.payment_service.delete_payment_data(payment_id)

            if done:
                return jsonify({'message': 'Payment deleted successfully'}), 201
            else:
                return jsonify({'error': f'Payment with id {payment_id} not found'}), 404
        
        except Exception as error:
            error_msg = str(error)
            return jsonify({'error': error_msg}), 500
        
    def healthcheck(self):
        return jsonify({'status': 'up'}), 200
