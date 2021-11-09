import os
from pathlib import Path
from api.common.identifiers import get_identifier
from api.common.logging import get_request_logger, get_response_logger, get_application_logger, get_loggable_object
from api.configuration import application_path
from api.caching import configure_caching, DEFAULT_CACHING_TIME


# --------------------------------------- #
# Loggable API Resources class definition #
# --------------------------------------- #

class LoggableResource(object):
    """Class implementing loggable resource"""

    # Make sure the logging directory exists
    Path(os.path.join(application_path, "..", "logs")).mkdir(parents=True, exist_ok=True)

    # Loggers for requests/responses
    request_logger = get_request_logger()
    response_logger = get_response_logger()

    def __init__(self):
        self.identifier = None

    def log_request_data(self, request):
        """Logs the request data"""
        self.identifier = get_identifier()
        self.request_logger.info(get_loggable_object(request, self.identifier))

    def log_response_data(self, response):
        """Logs the response data"""
        self.response_logger.info(get_loggable_object(response, self.identifier))

    @property
    def application_logger(self):
        """Returns the application logger withing the application context"""
        return get_application_logger()


# ---------------------------------------- #
# Cacheable API Resources class definition #
# ---------------------------------------- #

class CacheableResource(object):
    """Class implementing cacheable resource"""

    # Configuration for caching
    caching_configuration = configure_caching()

    # Caching attributes
    CACHE_EXPIRATION_TIME = caching_configuration.get("expiration_time_in_seconds", DEFAULT_CACHING_TIME)
