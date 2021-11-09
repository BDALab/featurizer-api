import json_tricks


# ---------------------------------------------- #
# Data wrapping/unwrapping exceptions definition #
# ---------------------------------------------- #
class DataUnwrappingException(Exception): pass
class DataWrappingException(Exception): pass


# ----------------------------------- #
# Data wrapping/unwrapping definition #
# ----------------------------------- #

class DataWrapper(object):
    """Class implementing data wrapper (wrapping and unwrapping data)"""

    @staticmethod
    def unwrap_data(data):
        """Unwraps the data (deserialize from JSON-string to numpy.ndarray)"""
        try:
            return json_tricks.loads(data) if isinstance(data, str) else data
        except Exception as e:
            raise DataUnwrappingException(e)

    @staticmethod
    def wrap_data(data):
        """Wraps the data (serialize numpy.ndarray to JSON-string)"""
        try:
            return json_tricks.dumps(data, allow_nan=True) if not isinstance(data, str) else data
        except Exception as e:
            raise DataWrappingException(e)
