import json


# -------------------------------------------------- #
# Response wrapping/unwrapping exceptions definition #
# -------------------------------------------------- #
class ResponseUnwrappingException(Exception): pass
class ResponseWrappingException(Exception): pass


# --------------------------------------- #
# Response wrapping/unwrapping definition #
# --------------------------------------- #

class ResponseWrapper(object):
    """Class implementing Response wrapper (wrapping and unwrapping responses)"""

    @staticmethod
    def unwrap_response(response):
        """Unwraps the response (deserialize from JSON-string)"""
        try:
            return json.loads(response) if isinstance(response, str) else response
        except Exception as e:
            raise ResponseUnwrappingException(e)

    @staticmethod
    def wrap_response(response):
        """Wraps the response (serialize to JSON-string)"""
        try:
            return json.dumps(response) if not isinstance(response, str) else response
        except Exception as e:
            raise ResponseWrappingException(e)


# ----------------------------- #
# HTTPError wrapping definition #
# ----------------------------- #

class HttpErrorWrapper(object):
    """Class implementing HTTPError wrapper (wrapping errors)"""

    def __init__(self, e):
        self.e = e

    def __str__(self):
        return f"{self.e.__class__.__name__}: {self.e}"
