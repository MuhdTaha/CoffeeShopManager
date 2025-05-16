from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    @app.route('/')
    def index():
        return "Hello from CoffeeShop!"
    
    @app.route('/api/')
    def api_home():
        return "Hello from Flask API"
    
    from app.routes import auth, orders, test
    app.register_blueprint(auth.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(test.bp)

    return app