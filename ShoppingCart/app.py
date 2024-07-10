from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from logger.LoggerBase import log
from models.CartModel import CartModel
from services.CartService import CartService
from routes.CartRoutes import CartRoutes

app = Flask(__name__)

car_model = CartModel()
car_service = CartService(car_model)
car_routes = CartRoutes(car_service)
app.register_blueprint(car_routes)

# swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

# register swagger bp
swagger_ui_blueprint = get_swaggerui_blueprint(
    base_url=SWAGGER_URL,
    api_url=API_URL,
    config={
        'app_name': 'Microservice Payment API'
    }
)

app.register_blueprint(swagger_ui_blueprint)

try:
    #nos conectamos a la base de datos
    car_model.connect_to_database()
except Exception as e:
    log.critical(e)

if __name__ == '__main__':
    app.run(debug=True)
