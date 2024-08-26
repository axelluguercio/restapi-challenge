from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from prometheus_client import start_http_server, Summary
import os

# Init extensions
db = SQLAlchemy()
migrate = Migrate()
metrics = Summary('api_requests', 'Summary of API requests')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
    )   
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init db
    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints
    from .routes import main
    app.register_blueprint(main)

    # Setup metric server
    start_http_server(8001)

    return app