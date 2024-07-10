from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from Logger.Logger import log
from Models.PaymentModel import PaymentModel
from Routes.PaymentRoutes import PaymentRoutes
from Services.PaymentService import PaymentService

app = Flask(__name__)

payment_model = PaymentModel()

try:
    payment_model.connect_to_database()
except Exception as e:
    log.critical(e)

payment_service = PaymentService(payment_model)
payment_routes = PaymentRoutes(payment_service)
app.register_blueprint(payment_routes)

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

if __name__ == '__main__':
    app.run()