# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

# Create a database object
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load environment variables or directly set the database URI here
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/dabbawalaDB')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = '66f6f81064acb4d37d24de3d97a09496dc17ae16b5d3f9fcd12e9d5954044572f96a248215885f692842762334d072450bfb3e38852a62ee556abfe8e19cb6a308ce4b12d6a545392109215f01a97c69b27e2528c238ff8743ca51bcd9206d1143d9a846b6cfc03f955b5397177218b26344f6982738b0a01c61f93c06a569a4fefacf71161b9fa1900ecbdb97ac84962664a99a95e9a35c76e7d71e83f5f2a0de3a5f4c6a29362f587f513369a80d4eb0d7d122915798c3743111107a3108747f0ae116e04a8dd997a31d92723766fe0ee507e59dcb95b00f81015282eb07cc33db01f2d7bb66035cf99e1b8a10b168a447099469dc19566ec751b2fb478226'
    
    # Initialize JWT Manager
    

    # Initialize SQLAlchemy with the app
    db.init_app(app)
    jwt = JWTManager(app)

    # Setup Flask-Migrate
    migrate = Migrate(app, db)

    # Register routes (import the routes from routes.py)
    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp,url_prefix = "/user")
     
    from app.controllers.mess_controller import mess_bp
    app.register_blueprint(mess_bp,url_prefix = "/mess")

    return app
