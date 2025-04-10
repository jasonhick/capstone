from flask import jsonify
from werkzeug.exceptions import HTTPException

from ..auth.auth import AuthError
from .logging import get_logger

logger = get_logger()

# Standard error messages
ERROR_MESSAGES = {
    400: "Bad request. Please check your input data.",
    401: "Unauthorised. Authentication credentials were missing or incorrect.",
    403: "Forbidden. You don't have permission to access this resource.",
    404: "Resource not found.",
    405: "Method not allowed for the requested URL.",
    422: "Unprocessable entity. The request was well-formed but invalid.",
    500: "Internal server error. Something went wrong on our end.",
}


class APIError(Exception):
    """Base class for API errors"""

    def __init__(self, message=None, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or {})
        rv["error"] = self.message or ERROR_MESSAGES.get(
            self.status_code, "An error occurred"
        )
        rv["status_code"] = self.status_code
        return rv


def register_error_handlers(app_or_blueprint):
    """Register error handlers for a Flask app or blueprint"""

    @app_or_blueprint.errorhandler(APIError)
    def handle_api_error(error):
        logger.error(f"API Error: {error.message} - Status: {error.status_code}")
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app_or_blueprint.errorhandler(HTTPException)
    def handle_http_exception(error):
        logger.error(f"HTTP Exception: {error.description} - Status: {error.code}")
        response = jsonify(
            {
                "error": error.description
                or ERROR_MESSAGES.get(error.code, "An error occurred"),
                "status_code": error.code,
            }
        )
        response.status_code = error.code
        return response

    @app_or_blueprint.errorhandler(Exception)
    def handle_generic_exception(error):
        logger.exception("Unhandled exception occurred")
        response = jsonify(
            {
                "error": ERROR_MESSAGES.get(500, "An unexpected error occurred"),
                "status_code": 500,
            }
        )
        response.status_code = 500
        return response

    @app_or_blueprint.errorhandler(AuthError)
    def handle_auth_error(error):
        logger.error(
            f"Auth Error: {error.error.get('description')} - Status: {error.status_code}"
        )
        response = jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": error.error.get("description", "Authentication error"),
            }
        )
        response.status_code = error.status_code
        return response


def handle_exception(func):
    """Decorator to handle exceptions in route handlers"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIError as e:
            logger.error(f"API Error in {func.__name__}: {e.message}")
            raise
        except HTTPException as e:
            logger.error(f"HTTP Exception in {func.__name__}: {e.description}")
            raise
        except AuthError as e:
            logger.error(f"Auth Error in {func.__name__}: {e.error.get('description')}")
            raise
        except Exception as e:
            logger.exception(f"Unhandled exception in {func.__name__}: {str(e)}")
            raise APIError(message=ERROR_MESSAGES.get(500), status_code=500)

    # Preserve the original function's metadata
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__

    return wrapper
