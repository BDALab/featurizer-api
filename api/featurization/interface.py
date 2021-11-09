# ------------------------------------------------- #
# Features extraction pipeline interface definition #
# ------------------------------------------------- #

class FeaturesExtractorPipeline(object):
    """Class implementing the features extractor pipeline interface"""

    def __init__(self, extractor, sample, config):
        """
        Initializes the FeaturesExtractorPipeline (using injected extractor).

        :param extractor: feature extractor interface class
        :type extractor: <injected>.interface.featurizer.HandwritingFeatures
        :param sample: sample data to extract the features from
        :type sample: api.interfaces.inputs.Sample
        :param config: feature extractor configuration
        :type config: api.interfaces.inputs.FeaturesExtractorConfiguration
        """
        self.extractor = extractor(sample.values, sample.labels, **config.extractor_configuration)

    def __repr__(self):
        return str({"extractor": self.extractor})

    def __str__(self):
        return repr(self)

    def __call__(self, pipeline):
        return self.extract(pipeline)

    def extract(self, pipeline):
        """
        Extracts the features from the features extraction pipeline.

        :param pipeline: pipeline with the feature names and kwargs
        :type pipeline: api.interfaces.inputs.FeaturesPipeline
        :return: extracted features and feature labels
        :rtype: dict
        """

        # Extract the features via the injected features extractor
        extracted = self.extractor.extract(pipeline.pipeline)

        # Return the extracted feature values and labels
        return {
            "values": extracted["features"],
            "labels": extracted["labels"]
        }
