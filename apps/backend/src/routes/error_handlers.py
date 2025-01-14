from flask import jsonify

ERROR_MESSAGES = {
    400: "Bad request. Please check your input data.",
    401: "Unauthorized. Authentication credentials were missing or incorrect.",
    403: "Forbidden. You don't have permission to access this resource.",
    404: "Resource not found.",
    405: "Method not allowed for the requested URL.",
    422: "Unprocessable entity. The request was well-formed but invalid.",
    500: "Internal server error. Something went wrong on our end.",
}


def create_error_response(error_code):
    return (
        jsonify(
            {
                "success": False,
                "error": error_code,
                "message": ERROR_MESSAGES.get(error_code, "Unknown error occurred."),
            }
        ),
        error_code,
    )


def register_error_handlers(blueprint):
    for error_code in ERROR_MESSAGES.keys():
        blueprint.errorhandler(error_code)(
            lambda e, code=error_code: create_error_response(code)
        )
