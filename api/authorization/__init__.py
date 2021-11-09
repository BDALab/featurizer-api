import os
from dotenv import load_dotenv, find_dotenv
from flask_jwt_extended import JWTManager
from api.configuration import load_configuration, application_path


# ----------------------------------------------- #
# Authorization configuration routines definition #
# ----------------------------------------------- #

def configure_authorization(app):
    """Configures the authorization"""

    # Initialize the authorization object
    JWTManager(app)

    # Load the configuration
    authorization_config = load_configuration("authorization.json").get("env", {}).get("env_file_location")

    # load the hidden authorization configuration as environment variables
    try:
        load_dotenv(find_dotenv(os.path.join(application_path, authorization_config), raise_error_if_not_found=True))
    except OSError:
        raise OSError(f"Cannot find .env file with JWT_SECRET_KEY specified in the configuration")

    # Configure the API authorization
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Configure the error message key
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
