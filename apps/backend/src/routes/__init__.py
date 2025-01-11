from .actors import actors_bp
from .movies import movies_bp

# Register blueprints with API prefix
actors_bp.url_prefix = "/api/v1"
movies_bp.url_prefix = "/api/v1"

__all__ = ["actors_bp", "movies_bp"]
