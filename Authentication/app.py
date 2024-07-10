"""
This script initializes a Flask application for authentication purposes.

It creates an instance of the Flask application and registers routes for user authentication.
An instance of the AuthenticationService class is created to handle user authentication.
The routes related to authentication are defined in the AuthenticationRoutes blueprint, which is then registered with the Flask application.

The script attempts to connect to the database using the AuthenticationService instance.
If the connection fails, it logs a critical error.

Usage:
    Run this script to start the Flask application for user authentication.

Dependencies:
    - Flask
    - LoggerBase module for logging
    - AuthenticationService class for user authentication
    - AuthenticationRoutes blueprint for defining authentication routes
"""

from flask import Flask, send_from_directory
from Logger.LoggerBase import log
from Services.AuthenticationService import AuthenticationService
from Routes.AuthenticationRoutes import AuthenticationRoutes
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)

# Create an instance of the AuthenticationService
authentication_service = AuthenticationService()

# Create an instance of the AuthenticationRoutes to define authentication routes
authentication_routes = AuthenticationRoutes(authentication_service)

# Register the authentication routes blueprint with the Flask application
app.register_blueprint(authentication_routes)

swagger_url = '/swagger'
api_url = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(swagger_url, api_url, config={'app_name': 'Authentication'})
app.register_blueprint(swagger_ui_blueprint, url_prefix=swagger_url)

try:
    # Connect to the database
    authentication_service.connect_to_database()
except Exception as e:
    # Log a critical error if database connection fails
    log.critical(e)

if __name__ == '__main__':
    # Run the Flask application
    app.run()
