import os
import time
import copy
import flask
import logging
import importlib
from pathlib import Path
from flask import has_request_context, request
from flask.logging import default_handler
from api.configuration import load_configuration, application_path


# ------------------------- #
# Logger getting definition #
# ------------------------- #

def get_logger(name, propagate=False):
    """
    Gets the basic logger with the specified name and the propagation rule.

    :param name: name of the logger
    :type name: str
    :param propagate: logger propagation, defaults to False
    :type propagate: bool, optional
    :return: Logger instance
    :rtype: <object>
    """

    # Get the logger
    logger = logging.getLogger(name)

    # Set the propagation rule
    logger.propagate = propagate

    # Return the logger
    return logger


# -------------------------------- #
# Logging configuration definition #
# -------------------------------- #

def configure_logging(app):
    """Configures the API logging"""

    # Prepare the logs path and make sure the logs directory exists
    Path(os.path.join(application_path, "..", "logs")).mkdir(parents=True, exist_ok=True)

    # Register the application logger
    set_application_logger(app)


# --------------------------- #
# Logging routines definition #
# --------------------------- #

def set_application_logger(app):
    """Sets the application logger"""

    # Load the configuration
    config = load_configuration("logging.json")["werkzeug"]
    logger = logging.getLogger("werkzeug")

    # Update the filename of the logging directory to reflect the full path
    if config.get("kwargs", {}).get("filename"):
        config["kwargs"]["filename"] = time.strftime(os.path.join("logs", f"%Y_%m_%d_{config['kwargs']['filename']}"))

    # Prepare the logging module and logger class name
    logger_path = config["class"].split(".")
    logger_module, logger_class = ".".join(logger_path[:-1]), logger_path[-1]

    # Prepare the logging class
    logger_class = getattr(importlib.import_module(logger_module), logger_class)

    # Prepare the handler
    handler = logger_class(**config["kwargs"])

    # Set the level and the formatter
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    logger.addHandler(handler)

    # Register the handler
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(handler)


def get_application_logger(app=None):
    """Gets the application logger"""
    return (app if app else flask.current_app).logger


def get_request_logger():
    """Gets the request logger"""

    class RequestFormatter(logging.Formatter):
        """Class extending the default formatter"""

        def format(self, record):
            """Formats the input record"""
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr
            else:
                record.url = None
                record.remote_addr = None
            return super().format(record)

    # Load the configuration
    config = load_configuration("logging.json")["request"]
    logger = logging.getLogger("request_logger")
    logger.setLevel(logging.DEBUG)

    # Update the filename of the logging directory to reflect the full path
    if config.get("kwargs", {}).get("filename"):
        config["kwargs"]["filename"] = time.strftime(
            os.path.join("logs", f"%Y_%m_%d_{config['kwargs']['filename']}"))

    # Prepare the logging module and logger class name
    logger_path = config["class"].split(".")
    logger_module, logger_class = ".".join(logger_path[:-1]), logger_path[-1]

    # Prepare the logging class
    logger_class = getattr(importlib.import_module(logger_module), logger_class)

    # Prepare the handler
    handler = logger_class(**config["kwargs"])

    # Configure the formatter
    formatter = RequestFormatter("[%(asctime)s] %(remote_addr)s requested %(url)s in %(module)s: %(message)s")
    handler.setFormatter(formatter)

    # Register the logger
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Return the logger
    return logger


def get_response_logger():
    """Gets the response logger"""

    # Load the configuration
    config = load_configuration("logging.json")["response"]
    logger = logging.getLogger("response_logger")
    logger.setLevel(logging.DEBUG)

    # Update the filename of the logging directory to reflect the full path
    if config.get("kwargs", {}).get("filename"):
        config["kwargs"]["filename"] = time.strftime(
            os.path.join("logs", f"%Y_%m_%d_{config['kwargs']['filename']}"))

    # Prepare the logging module and logger class name
    logger_path = config["class"].split(".")
    logger_module, logger_class = ".".join(logger_path[:-1]), logger_path[-1]

    # Prepare the logging class
    logger_class = getattr(importlib.import_module(logger_module), logger_class)

    # Prepare the handler
    handler = logger_class(**config["kwargs"])

    # Configure the formatter
    formatter = logging.Formatter("%(asctime)s, %(message)s")
    handler.setFormatter(formatter)

    # Register the logger
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Return the logger
    return logger


def get_loggable_object(instance, identifier):
    """Returns the loggable request/response objects"""

    # Make a copy of the instance
    loggable = copy.deepcopy(instance)

    # Add the identifier
    loggable.update({"identifier": identifier})

    # Return the loggable object
    return loggable
