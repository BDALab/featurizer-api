import os
import json


# ---------------------------- #
# Package structure definition #
# ---------------------------- #

# Prepare the configuration path
configuration_path = os.path.dirname(os.path.realpath(__file__))

# Prepare the application path
application_path = os.path.join(configuration_path, "..")


# -------------------------------- #
# Configuration helpers definition #
# -------------------------------- #

def load_configuration(configuration_filename):
    """Loads the configuration from the specified configuration file name"""

    # Prepare the api configuration file path
    path = os.path.join(configuration_path, configuration_filename)

    # Read the configuration
    if path and os.path.isfile(path) and os.access(path, os.R_OK):
        with open(path, "r") as f:
            return json.load(f)
