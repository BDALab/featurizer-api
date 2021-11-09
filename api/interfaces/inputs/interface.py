from api.interfaces.inputs.schema import SampleSchema, FeaturesPipelineSchema, FeaturesExtractorConfigurationSchema


# --------------------------------- #
# Input sample interface definition #
# --------------------------------- #

class Sample(object):
    """Class implementing the input samples interface"""

    # Define the schema
    schema = SampleSchema()

    def __init__(self, values, labels):
        """Initializes the Sample"""
        self.values = values
        self.labels = labels

    def __repr__(self):
        return str({"values": self.values, "labels": self.labels})

    def __str__(self):
        return repr(self)

    @classmethod
    def from_request(cls, request):
        """
        Creates the Sample instance utilizing the schema.

        :param request: dict with the data sample values and labels
        :type request: dict
        :return: class instance
        :rtype: api.interfaces.inputs.Sample
        """
        return cls(**cls.schema.load(request))


# ----------------------------------------------------------- #
# Input features extractor configuration interface definition #
# ----------------------------------------------------------- #

class FeaturesExtractorConfiguration(object):
    """Class implementing the input extractor configuration interface"""

    # Define the schema
    schema = FeaturesExtractorConfigurationSchema()

    def __init__(self, extractor_configuration):
        """Initializes the FeaturesExtractorConfiguration"""
        self.extractor_configuration = extractor_configuration if extractor_configuration else {}

    def __repr__(self):
        return str({"configuration": self.extractor_configuration})

    def __str__(self):
        return repr(self)

    @classmethod
    def from_request(cls, request):
        """
        Creates the FeaturesExtractorConfiguration instance.

        :param request: dict with the features pipeline
        :type request: dict or str
        :return: class instance
        :rtype: api.interfaces.inputs.FeaturesExtractorConfiguration
        """
        return cls(**cls.schema.load(request))


# -------------------------------------------- #
# Input features pipeline interface definition #
# -------------------------------------------- #

class FeaturesPipeline(object):
    """Class implementing the input features pipeline interface"""

    # Define the schema
    schema = FeaturesPipelineSchema()

    def __init__(self, pipeline):
        """Initializes the FeaturesPipeline"""
        self.pipeline = pipeline

    def __repr__(self):
        return str({"pipeline": self.pipeline})

    def __str__(self):
        return repr(self)

    def __getitem__(self, index):
        return self.pipeline[index]

    def __setitem__(self, index, value):
        self.pipeline[index] = value

    @classmethod
    def from_request(cls, request):
        """
        Creates the FeaturesPipeline instance.

        :param request: dict with the features pipeline
        :type request: dict or str
        :return: class instance
        :rtype: api.interfaces.inputs.FeaturesPipeline
        """
        return cls(**cls.schema.load(request))
