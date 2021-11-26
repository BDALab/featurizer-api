import os
from pathlib import Path
from flask_bcrypt import Bcrypt
from api.configuration import application_path, load_configuration
from api.authentication.database import initialize_database


# ------------------------------------------------ #
# Authentication configuration routines definition #
# ------------------------------------------------ #

def configure_authentication(app):
    """Configures the authentication"""

    # Initialize the encryption object
    Bcrypt(app)

    # Configure the authentication database
    for key, value in load_configuration("authentication.json").get("database", {}).items():
        app.config[key] = value

    # Get the database path
    path = app.config["SQLALCHEMY_DATABASE_URI"].lstrip("sqlite:///").split("/")[:-1]

    # Prepare the database path and make sure the database directory exists
    Path(os.path.join(application_path, "..", *path)).mkdir(parents=True, exist_ok=True)

    # Initialize the authentication database
    initialize_database(app)
