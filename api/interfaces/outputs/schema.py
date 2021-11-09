import numpy
import marshmallow
from api.interfaces.outputs.utilities import FeatureValuesValidator, FeatureLabelsValidator
from api.wrappers.data import *


# ------------------------------------------- #
# Output features interface schema definition #
# ------------------------------------------- #

class FeaturesSchema(marshmallow.Schema):
    """Class defining the schema for the features input interface"""

    # Define the meta attributes
    class Meta:
        unknown = marshmallow.EXCLUDE

    # Define the schema attributes
    values = marshmallow.fields.Str(required=True)
    labels = marshmallow.fields.List(marshmallow.fields.String, missing=[])

    @marshmallow.pre_dump
    def _pre_dump(self, instance, **kwargs):
        """Handles the pre-dumping data preparation and validation"""

        # Validate the features
        if not isinstance(instance.features.get("values"), numpy.ndarray):
            raise marshmallow.ValidationError("Not a valid numpy.array.", "features.values")

        # Get the attributes
        values = instance.features["values"]
        labels = instance.features["labels"]

        # Handle the feature values/labels
        instance.features["values"] = DataWrapper.wrap_data(FeatureValuesValidator.validate(values))
        instance.features["labels"] = FeatureLabelsValidator.validate(labels, values)

        # Return the output data
        return instance.features
