from flask import Flask
from api.common.base import Api
from api.common.errors import register_errors, register_errors_from_third_parties
from api.common.logging import configure_logging
from api.cors import configure_cors
from api.resources import configure_routes
from api.authentication import configure_authentication
from api.authorization import configure_authorization
from api.featurization import configure_features_extraction_library_injection
from api.featurization.library_injection import (
    validate_features_library,
    inject_features_extractor,
    inject_features_extractor_exceptions
)


def prepare_app(app_name):
    """Prepares the application"""

    # Initialize the Flask object
    app = Flask(app_name)

    # Initialize the cross origin resource sharing object
    configure_cors(app)

    # Configure the logging and error-handling
    configure_logging(app)
    register_errors(app)

    # Configure the authentication and authorization
    configure_authentication(app)
    configure_authorization(app)

    # Prepare the API
    prepare_api(app)

    # Return the app
    return app


def prepare_api(app):
    """Prepares the API"""

    # Initialize the Flask-RestFul object
    api = Api(app)

    # Get the features extractor library
    injected_library_name = configure_features_extraction_library_injection()

    # Validate the ability to import the features extractor library
    validate_features_library(injected_library_name)

    # Get the injected features extractor and exceptions
    feature_extractor_interface = inject_features_extractor(injected_library_name)
    feature_extractor_exceptions = inject_features_extractor_exceptions(injected_library_name)

    # Register the injected features extractor exceptions as client-side errors
    if feature_extractor_exceptions:
        register_errors_from_third_parties(app, feature_extractor_exceptions)

    # Register the routes
    configure_routes(api, feature_extractor_interface)
