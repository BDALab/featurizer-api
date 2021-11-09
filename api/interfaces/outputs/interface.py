from api.interfaces.outputs.schema import FeaturesSchema


# ------------------------------------ #
# Output features interface definition #
# ------------------------------------ #

class Features(object):
    """Class implementing the output features interface"""

    # Define the schema
    schema = FeaturesSchema()

    def __init__(self, features):
        """Initializes the Features"""
        self.features = features

    def to_response(self):
        """Dumps the features to the data to be used in the response"""
        return {"features": self.schema.dump(self)}
