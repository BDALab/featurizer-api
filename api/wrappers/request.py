import json


# ------------------------------------------------- #
# Request wrapping/unwrapping exceptions definition #
# ------------------------------------------------- #
class RequestUnwrappingException(Exception): pass
class RequestWrappingException(Exception): pass


# -------------------------------------- #
# Request wrapping/unwrapping definition #
# -------------------------------------- #

class RequestWrapper(object):
    """Class implementing Request wrapper (wrapping and unwrapping requests)"""

    @staticmethod
    def unwrap_request(request):
        """Unwraps the request (deserialize from JSON-string)"""
        try:
            return request.args if request.method == "GET" else (request.get_json() or json.loads(request.data))
        except Exception as e:
            raise RequestUnwrappingException(e)

    @staticmethod
    def wrap_request(request):
        """Wraps the request (serialize to JSON-string)"""
        try:
            return json.dumps(request) if not isinstance(request, str) else request
        except Exception as e:
            raise RequestWrappingException(e)
