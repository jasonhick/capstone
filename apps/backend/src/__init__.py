from flask import Flask, render_template
from flask_cors import CORS

from .config import Config
from .database import db, init_db
from .routes import actors_bp, movies_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False  # This disables the automatic redirect

    # Enable CORS
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://127.0.0.1:3000"],
                "methods": ["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    # Initialize database and models (this will also init the app)
    init_db(app)

    # Register blueprints
    app.register_blueprint(actors_bp)
    app.register_blueprint(movies_bp)

    return app


# Create the app instance
app = create_app()

__all__ = ["create_app"]
