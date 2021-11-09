from functools import wraps
from datetime import datetime


# -------------------- #
# Utilities definition #
# -------------------- #

def measure_runtime(method):
    """
    Decorator that measures the runtime of the <method>.

    :param method: method to decorate
    :type method: callable
    :return: decorated method
    :rtype: <method>
    """

    @wraps(method)
    def measure(*args, **kwargs):
        s = datetime.now()
        r = method(*args, **kwargs)
        f = datetime.now()
        d = (f - s)
        if d.microseconds > 0.0000:
            print(f"Execution of <{method.__name__}> finished (runtime): {d}")
        return r
    return measure
