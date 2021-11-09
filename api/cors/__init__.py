from flask_cors import CORS
from api.configuration import load_configuration


# -------------------------------------- #
# CORS configuration routines definition #
# -------------------------------------- #

def configure_cors(app):
    """Configures the cross-object resource sharing"""

    # Configure the CORS
    origins = load_configuration("cors.json").get("origins")

    # Initialize the CORS object
    CORS(app, origins=origins)
