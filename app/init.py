from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os

from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) 

    #Ensure logs file exists
    os.makedirs("logs", exist_ok=True)

    #Logging setup
    file_handler = RotatingFileHandler(
        app.config["LOG_FILE"], maxBytes= 10240, backupCount=5
        )
    
    file_handler.setLevel(app.config["LOG_LEVEL"])

    formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
    )
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    app.logger.info("App started")

    #Registering route file
    from .routes import main_bp
    app.register_blueprint(main_bp)

    #Registering error_handler
    from .error import error_handlers
    error_handlers(app)

    return app
