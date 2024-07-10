from flask import Blueprint,jsonify,request
from logger.logger_base import log

class OrderRoutes(Blueprint):
    """
    Class representing API routes for handling orders.

    Attributes:
        order_service: An instance of OrderService to handle order operations.
    """

    def __init__(self, order_service):
        """
        Initialize OrderRoutes with an OrderService instance.

        Args:
            order_service: An instance of OrderService.
        """
        super().__init__('order', __name__)
        self.order_service = order_service
        self.register_routes()

    def register_routes(self):
        """Register API routes for order operations."""
        self.route('/api/orders', methods=['GET'])(self.get_orders)
        self.route('/api/orders/<int:order_id>', methods=['GET'])(self.get_order_by_id)
        self.route('/api/newOrders', methods=['POST'])(self.create_order)
        self.route('/api/orders/<int:order_id>', methods=['DELETE'])(self.delete_order)
        self.route('/api/orders/<int:order_id>', methods=['PUT'])(self.update_order)  
        self.route('/api/orders/<int:order_id>/tracking', methods=['GET'])(self.get_tracking_info_by_id)
        self.route('/healtcheck', methods=['GET'])(self.healthcheck)

    def get_orders(self):
        """Get all orders."""
        try:
            orders = self.order_service.get_all_orders()
            return jsonify(orders), 200
        except Exception as e:
            log.exception(f'Error fetching from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500
        
    def get_order_by_id(self, order_id):
        """Get an order by its ID."""
        self.order = self.order_service.get_order_by_id(order_id)
        if self.order:
            return jsonify(self.order), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
        
    def create_order(self):
        """Create a new order."""
        try:
            order_data = request.json
            response, status_code = self.order_service.add_order(order_data)
            return jsonify(response), status_code
        except Exception as e:
            log.exception(f'Error creating order: {e}')
            return jsonify({'error': 'Failed to create order'}), 500
    
    def delete_order(self, order_id):
        """Delete an order."""
        try:
            response, status_code = self.order_service.delete_order(order_id)
            return jsonify(response), status_code
        except Exception as e:
            log.exception(f'Error deleting order: {e}')
            return jsonify({'error': 'Failed to delete order'}), 500
        
    def update_order(self, order_id):
        """Update an existing order."""
        try:
            order_data = request.json
            response, status_code = self.order_service.update_order(order_id, order_data)
            return jsonify(response), status_code
        except Exception as e:
            log.exception(f'Error updating order: {e}')
            return jsonify({'error': 'Failed to update order'}), 500
    
    def get_tracking_info_by_id(self, order_id):
        """Get tracking information for an order by its ID."""
        try:
            tracking_info, status_code = self.order_service.get_tracking_info_by_id(order_id)
            return jsonify(tracking_info), status_code
        except Exception as e:
            log.exception(f'Error fetching tracking info: {e}')
            return jsonify({'error': 'Failed to fetch tracking info'}), 500

    def healthcheck(self):
        """Health check endpoint."""
        return jsonify({'status': 'OK'}), 200
