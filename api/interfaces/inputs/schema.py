import marshmallow
from api.interfaces.inputs.utilities import SamplesValuesValidator, SamplesLabelsValidator
from api.wrappers.data import *


# ---------------------------------------- #
# Input sample interface schema definition #
# ---------------------------------------- #

class SampleSchema(marshmallow.Schema):
    """Class defining the schema for the sample input interface"""

    # Define the meta attributes
    class Meta:
        unknown = marshmallow.EXCLUDE

    # Define the schema attributes
    values = marshmallow.fields.Str(required=True)
    labels = marshmallow.fields.List(marshmallow.fields.String, missing=[])

    @marshmallow.pre_load
    def _pre_load(self, data, **kwargs):
        """Handles the pre-loading data preparation and validation"""

        # Handle the sample field
        if not data.get("samples"):
            raise marshmallow.ValidationError("Missing data for required field.", "samples")
        if not isinstance(data.get("samples"), dict):
            raise marshmallow.ValidationError("Not a valid dict.", "samples")

        # Return the output data
        return data.get("samples")

    @marshmallow.post_load
    def _post_load(self, data, **kwargs):
        """Handles the post-loading data preparation and validation"""

        # Get the attributes
        values = DataWrapper.unwrap_data(data["values"])
        labels = data["labels"] or []

        # Handle the sample values/labels
        values = SamplesValuesValidator.validate(values)
        labels = SamplesLabelsValidator.validate(labels, values)

        # Return the output data
        return {"values": values, "labels": labels}


# ------------------------------------------------- #
# Feature extractor configuration schema definition #
# ------------------------------------------------- #

class FeaturesExtractorConfigurationSchema(marshmallow.Schema):
    """Class defining the schema for the features extractor configuration"""

    # Define the meta attributes
    class Meta:
        unknown = marshmallow.EXCLUDE

    # Define the schema attributes
    extractor_configuration = marshmallow.fields.Dict(missing={})


# --------------------------------------------------- #
# Input features pipeline interface schema definition #
# --------------------------------------------------- #

class FeaturesPipelineElementSchema(marshmallow.Schema):
    """Class defining the schema for the features pipeline input element"""

    # Define the meta attributes
    class Meta:
        unknown = marshmallow.EXCLUDE

    # Define the schema attributes
    name = marshmallow.fields.Str(required=True)
    args = marshmallow.fields.Dict(missing={})


class FeaturesPipelineSchema(marshmallow.Schema):
    """Class defining the schema for the features pipeline input interface"""

    # Define the meta attributes
    class Meta:
        unknown = marshmallow.EXCLUDE

    # Define the schema attributes
    pipeline = marshmallow.fields.Nested(FeaturesPipelineElementSchema, many=True)

    @marshmallow.pre_load
    def _pre_load(self, data, **kwargs):
        """Handles the pre-loading data preparation and validation"""

        # Handle the sample field
        if not data.get("features"):
            raise marshmallow.ValidationError("Missing data for required field.", "features")
        if not isinstance(data.get("features"), dict):
            raise marshmallow.ValidationError("Not a valid dict.", "features")

        # Return the output data
        return data.get("features")

    @marshmallow.post_load
    def _post_load(self, data, **kwargs):
        """Handles the post-loading data preparation and validation"""

        # Handle the feature values
        if not data.get("pipeline") or len(data["pipeline"]) == 0:
            raise marshmallow.ValidationError("No features to be computed (empty pipeline)", "features.pipeline")

        # Return the output data
        return data
