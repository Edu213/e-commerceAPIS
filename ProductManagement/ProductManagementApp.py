"""
This module initialize a Flask application and integrate product related components

It initialize a Flask app, connect to the databse using ProductModel, 
initialize ProductServices for product related operations,
and registers product routes using ProductRoutes
"""

from flask import Flask 
from Models.ProductModel import ProductModel
from Services.ProductServices import ProductServices
from Routes.ProductRoutes import ProductRoutes
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/swagger' #URL to access the documentation
API_URL = '/static/swagger.json' #Swagger JSON specification URL

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Product Management API" #Specify the name of the API
    }
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

#Initialize database connection
db_connector = ProductModel()
db_connector.connect_to_database()

#Initialize product services
product_service = ProductServices(db_connector)

#Initialize product routes
product_blueprint = ProductRoutes(product_service)
app.register_blueprint(product_blueprint)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        #Close database connection whenm the application exits
        db_connector.close_connection()