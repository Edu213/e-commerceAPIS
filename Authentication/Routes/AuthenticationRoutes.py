"""
This script defines Flask routes for user authentication including user registration and login.

It utilizes Flask Blueprint to organize routes related to authentication.
The AuthenticationRoutes blueprint includes routes for user registration and login.

The register_user route handles user registration by validating incoming JSON data using the AuthenticationSchema,
registering the user in the database using the AuthenticationService, and returning the user ID or an error message.

The login_user route handles user login by verifying the email and password against the database using the AuthenticationService,
and returning the user ID upon successful login or an error message if authentication fails.

Usage:
    Import this script and add the AuthenticationRoutes blueprint to your Flask application.

Dependencies:
    - Flask
    - Blueprint, jsonify, request from Flask
    - LoggerBase module for logging
    - AuthenticationService class for user authentication
    - AuthenticationSchema for validating authentication data
"""

from flask import Blueprint, jsonify, request
from Logger.LoggerBase import log
from Services.AuthenticationService import AuthenticationService
from Schemes.AuthenticationSchema import AuthenticationSchema
from marshmallow import ValidationError

class AuthenticationRoutes(Blueprint):
    def __init__(self, authentication_service: AuthenticationService):
        """
        Initializes the AuthenticationRoutes blueprint with the specified AuthenticationService instance.

        Args:
            authentication_service (AuthenticationService): An instance of the AuthenticationService class.
        """
        super().__init__('authentication', __name__)
        self.authentication_service = authentication_service
        self.register_routes()
        
    def register_routes(self):
        """
        Registers routes for user registration, login, healthcheck.
        """
        self.route('/api/register', methods=['POST'])(self.register_user)
        self.route('/api/login', methods=['POST'])(self.login_user)
        self.route('/api/delete_user', methods=['DELETE'])(self.delete_user)
        
        self.route('/health', methods=['GET'])(self.health_check)
        
    def register_user(self):
        """
        Handles user registration.

        Validates incoming JSON data using the AuthenticationSchema, registers the user in the database,
        and returns the user ID or an error message.

        Returns:
            JSON response: User ID or error message.
        """
        req_body = request.get_json() 

        if not req_body:
            return jsonify({'error': 'Invalid data'})
        
        try:
            data = AuthenticationSchema().load(req_body)
            user_id = self.authentication_service.register_user(data)
            
            if user_id is None:
                msg = "Cannot register the user in the database"
                log.critical(msg)
                return jsonify('error:', msg)
            
            return jsonify({'user_id': user_id}), 201

        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        
        except Exception as error_msg: 
            log.critical(error_msg)
            return jsonify({'error': str(error_msg)}), 500
        
    def login_user(self):
        """
        Handles user login.

        Verifies the email and password against the database using the AuthenticationService,
        and returns the user ID upon successful login or an error message if authentication fails.

        Returns:
            JSON response: User ID or error message.
        """
        req_body = request.get_json()

        if not req_body:
            return jsonify({'error': 'Invalid data'})

        try:
            email = req_body.get('email')
            password = req_body.get('password')
            user_id = self.authentication_service.login_user(email, password)

            if user_id:
                return jsonify({'user_id': user_id}), 200
            else:
                return jsonify({'error': 'Invalid credentials'}), 401

        except Exception as error_msg:
            log.critical(error_msg)
            return jsonify({'error': str(error_msg)}), 500
        
    def delete_user(self):
        """
        Handles user deletion.

        Deletes a user based on email and password, with confirmation.

        Returns:
            JSON response: Message indicating the result of the deletion.
        """
        req_body = request.get_json()

        if not req_body:
            return jsonify({'error': 'Invalid data'})

        try:
            email = req_body.get('email')
            password = req_body.get('password')
            user_id = req_body.get('user_id')
            confirm = req_body.get('confirm')

            result = self.authentication_service.delete_user(email, password, user_id, confirm)

            return jsonify({'message': result}), 200
        except Exception as error_msg:
            log.critical(error_msg)
            return jsonify({'error': str(error_msg)}), 500
        
    def health_check(self):
        try:
            return jsonify({'status': 'ok'}), 200
        
        except Exception as error_msg:
            log.critical(error_msg)
            return jsonify({'error': str(error_msg)}), 500
