from flask import Flask
from models.OrderModels import OrderModel
from services.OrderServices import OrderService
from routes.OrderRoutes import OrderRoutes
from flask_swagger_ui import get_swaggerui_blueprint

app=Flask(__name__)


SWAGGER_URL='/swagger'
API_URL='/static/swagger.json'
swagger_ui_blueprint=get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':'Orders API'
    }
)

db_connector=OrderModel()
db_connector.connect_to_database()

order_service=OrderService(db_connector)

order_blueprint=OrderRoutes(order_service)
app.register_blueprint(order_blueprint)
app.register_blueprint(swagger_ui_blueprint)

if __name__=='__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(e)