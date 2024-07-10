from logger.logger_base import log
from flask import jsonify
from schemes.OrderSchemas import OrderSchema

class OrderService:
    """
    Service to handle operations related to orders.

    Attributes:
        db_connector: Database connector used by the service.
        order_schemas: Instance of the order validation and serialization schema.
    """
    
    def __init__(self, db_connector):
        """Initialize OrderService with a database connector."""
        self.db_connector = db_connector
        self.order_schemas = OrderSchema()
        
    def get_all_orders(self):
        """Retrieve all orders from the database."""
        try:
            self.orders = list(self.db_connector.db.orders.find())
            return self.orders
        except Exception as e:
            log_message = f'Error fetching all orders from the database: {e}'
            log.critical(log_message)
            return jsonify({'error': log_message}), 500
        
    def get_order_by_id(self, order_id):
        """Retrieve an order by its ID from the database."""
        try:
            self.order = self.db_connector.db.orders.find_one({'_id': order_id})
            return self.order
        except Exception as e:
            log_message = f'Error fetching order: {e}'
            log.critical(log_message)
            return jsonify({'error': log_message}), 500
    
    def add_order(self, order_data):
        """Add a new order to the database."""
        try:
            # Validate order data using schema
            validated_data = self.order_schemas.load(order_data)
            # Insert validated data into the database
            result = self.db_connector.db.orders.insert_one(validated_data)
            if result.inserted_id:
                return {'message': 'Order added successfully', 'order_id': str(result.inserted_id)}, 201
            else:
                return {'error': 'Failed to add order'}, 500
        except Exception as e:
            log_message = f'Error adding order: {e}'
            log.critical(log_message)
            return {'error': log_message}, 500
    
    def delete_order(self, order_id):
        """Delete an order from the database by its ID."""
        try:
            order = self.db_connector.db.orders.find_one({'_id': order_id})
            if order:
                self.db_connector.db.orders.delete_one({'_id': order_id})
                return {'message': 'Order deleted successfully'}, 200
            else:
                return {'error': 'Order not found'}, 404
        except Exception as e:
            log_message = f'Error deleting order: {e}'
            log.critical(log_message)
            return {'error': log_message}, 500

    def update_order(self, order_id, order_data):
        """Update an existing order in the database."""
        try:
            # Validate order data using schema
            validated_data = self.order_schemas.load(order_data)
            
            # Check if the order exists
            existing_order = self.db_connector.db.orders.find_one({'_id': order_id})
            if not existing_order:
                return {'error': 'Order not found'}, 404
            
            # Update the order in the database
            self.db_connector.db.orders.update_one({'_id': order_id}, {'$set': validated_data})
            
            return {'message': 'Order updated successfully'}, 200
        except Exception as e:
            log_message = f'Error updating order: {e}'
            log.critical(log_message)
            return {'error': log_message}, 500
        
    def get_tracking_info_by_id(self, order_id):
        """Retrieve tracking information for an order by its ID."""
        try:
            order = self.db_connector.db.orders.find_one({'_id': order_id})
            if order:
                tracking_info = order.get('tracking_info')
                if tracking_info:
                    return tracking_info, 200
                else:
                    return {'error': 'Tracking info not found for this order'}, 404
            else:
                return {'error': 'Order not found'}, 404
        except Exception as e:
            log_message = f'Error fetching tracking info: {e}'
            log.critical(log_message)
            return {'error': log_message}, 500
