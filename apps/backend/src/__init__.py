from flask import Flask

from .config import Config
from .database import db, init_db
from .routes import actors_bp, movies_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False  # This disables the automatic redirect

    # Initialize extensions
    db.init_app(app)

    # Initialize database and models
    init_db(app)

    # Register blueprints
    app.register_blueprint(actors_bp)
    app.register_blueprint(movies_bp)

    return app


# Create the app instance
app = create_app()

__all__ = ["create_app"]
