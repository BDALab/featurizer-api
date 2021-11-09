from flask import jsonify, make_response
from werkzeug import exceptions
from marshmallow import ValidationError


# ------------------------------------------ #
# Specifically handled exceptions definition #
# ------------------------------------------ #
from api.wrappers.request import RequestWrappingException, RequestUnwrappingException
from api.wrappers.response import ResponseWrappingException, ResponseUnwrappingException
from api.wrappers.data import DataUnwrappingException, DataWrappingException


# -------------------------------------------------- #
# Specifically handled client side errors definition #
# -------------------------------------------------- #
errors_client_side = (
    ValidationError,
    RequestWrappingException,
    RequestUnwrappingException,
    ResponseWrappingException,
    ResponseUnwrappingException,
    DataWrappingException,
    DataUnwrappingException,
)


# ---------------------------------- #
# Error handling routines definition #
# ---------------------------------- #

def generate_error(error, status_code, message=None):
    """
    Generates an error message formatted for the error handlers.

    :param error: error object
    :type error: object
    :param status_code: HTTP status code
    :type status_code: int
    :param message: message, defaults to None
    :type message: str, optional
    :return: jsonified response
    :rtype: Response
    """
    return make_response(jsonify({"message": f"{str(error) or message}"}), status_code)


def handle_400_errors(error):
    """Handles 400 errors in resources"""
    return generate_error(error, 400)


def handle_404_errors(error):
    """Handles 404 errors in resources"""
    return generate_error(error, 404)


def handle_server_errors(error):
    """Handles all internal server errors"""
    return generate_error(error, 500, message="Internal server error: we are working to resolve the issue")


def register_errors_from_third_parties(app, third_party_errors=None):
    """Registers the client-side errors from third parties"""
    if third_party_errors:
        for error in third_party_errors:
            app.register_error_handler(error, handle_400_errors)


def register_errors(app):
    """Registers the application errors"""

    # Register the 400 and 404 errors, and internal server errors
    app.register_error_handler(exceptions.BadRequest, handle_400_errors)
    app.register_error_handler(exceptions.NotFound, handle_404_errors)
    app.register_error_handler(exceptions.InternalServerError, handle_server_errors)

    # Register the specifically handled client-side errors
    for error in errors_client_side:
        app.register_error_handler(error, handle_400_errors)

    @app.errorhandler(422)
    def handle_error(err):
        """Registers handling of 422 errors (handles webargs exceptions)"""

        # Prepare the headers and the error message
        headers = err.data.get("headers", None)
        message = err.data.get("messages", ["Invalid request."])

        # Return the jsonified data
        if headers:
            return jsonify({"errors": message}), err.code, headers
        else:
            return jsonify({"errors": message}), err.code
