from api.configuration import load_configuration


# --------------------------------- #
# Configuration routines definition #
# --------------------------------- #

def configure_features_extraction_library_injection():
    """Configures the API features extraction library injection"""
    return load_configuration("injection.json")["features_extraction_library"]
