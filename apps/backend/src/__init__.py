from flask import Flask, render_template
from flask_cors import CORS

from .common import get_logger
from .common.error_handlers import register_error_handlers
from .config import Config
from .database import db, init_db
from .routes import actors_bp, movies_bp

# Get logger
logger = get_logger()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False  # This disables the automatic redirect

    # Enable CORS
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://127.0.0.1:4200", "http://localhost:4200"],
                "methods": ["GET", "PUT", "POST", "PATCH", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    # Initialize database and models (this will also init the app)
    init_db(app)

    # Register blueprints
    app.register_blueprint(actors_bp)
    app.register_blueprint(movies_bp)

    # Register error handlers
    register_error_handlers(app)

    logger.info("Application initialized successfully")

    return app


# Create the app instance
app = create_app()

__all__ = ["create_app"]
