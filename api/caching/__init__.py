from api.configuration import load_configuration


# ------------------------------------- #
# Default caching attributes definition #
# ------------------------------------- #
DEFAULT_CACHING_TIME = 60


# ----------------------------------------- #
# Caching configuration routines definition #
# ----------------------------------------- #

def configure_caching():
    """Configures the response caching"""
    return {key: value for key, value in load_configuration("caching.json").get("cache", {}).items()}
