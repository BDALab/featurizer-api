import flask_restful


# ----------------------------- #
# Extended API class definition #
# ----------------------------- #

class Api(flask_restful.Api):
    """Class extending the capabilities of the Flask-Restful API class"""

    def error_router(self, original_handler, e):
        """Overrides error_router to custom errors/ webargs parsing errors"""

        # -----
        # Info:
        #
        # If the provided input error can be handled by the flask_restful's Api
        # error handler, it is done that way, otherwise, the error is handled
        # by Flask (it is propagated to the Flask's error handler).
        #
        # To support the errors given by the webargs library, the error handler
        # of the flask_restful also checks for "UnprocessableEntity" error.

        # Handle the error by the flask_restful
        if self._has_fr_route() and type(e).__name__.split(".")[-1] in ["UnprocessableEntity"]:
            try:
                return self.handle_error(e)
            except Exception:
                pass

        # Fall through to original error handler
        return original_handler(e)
