import flask
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_api_cache import ApiCache
from http import HTTPStatus
from api.wrappers.request import RequestWrapper
from api.wrappers.response import ResponseWrapper
from api.featurization.interface import FeaturesExtractorPipeline
from api.interfaces.inputs.interface import Sample, FeaturesExtractorConfiguration, FeaturesPipeline
from api.interfaces.outputs.interface import Features
from api.resources.base import LoggableResource, CacheableResource


# ---------------------------------- #
# Featurizer API Resource definition #
# ---------------------------------- #

class FeaturizerResource(Resource, LoggableResource, CacheableResource):
    """Class implementing the featurizer API resource (controller)"""

    def __init__(self, extractor_interface=None):
        """Initializes the FeaturizerResource (controller)"""

        # Initialize the super-class
        super().__init__()

        # Set the features extractor interface
        self.extractor_interface = extractor_interface

    @jwt_required()
    @ApiCache(expired_time=CacheableResource.CACHE_EXPIRATION_TIME)
    def post(self):
        """
        Computes the features from the data for 1-M subjects.

        The method expects the JSON-serialized data in the body of the request
        that contains all information that is needed for the featurization. The
        information needed comprise: a) samples to be fed into a featurizer, b)
        featurization pipeline, and c) extractor configuration. More information
        about the structure of the data can be seen bellow.

        The featurization can be secured by the auth JWT token. If the method is
        decorated with ``@jwt_required()``, every request must be authorized by
        the JWT token that an authenticated user obtained via the ``/signup``
        and ``/login`` API calls. For more information, see:
        ``api.resources.security.py``.

        **Input data**

        Structure of the input data is the following: it is a ``dict`` object
        with these field-value pairs (example bellow):

        - ``samples`` (``dict``, mandatory)
        - ``samples.values`` (``np.array``, mandatory)
        - ``samples.labels`` (``list``, optional)
        - ``features`` (``dict``, mandatory)
        - ``features.pipeline`` (``list``, mandatory)
        - ``features.pipeline[0..., F]`` (``dict``, mandatory)
        - ``extractor_configuration`` (``dict``, optional)

        .. code-block:: python

            # Example:
            # - 10 subjects
            # - each subject has data of shape (2, 5)
            # - 3 features in the pipeline
            # - sampling frequency (fs) in extractor configuration
            {
                "samples": {
                    "labels": ["element 1", ... "element 5"],
                    "values": np.array((10, 2, 5))
                },
                "features": {
                    "pipeline": [
                        {
                            "name": "feature 1",
                            "args": {"abc": 123, "def": 456}
                        },
                        {
                            "name": "feature 2",
                            "args": {"ghi": "simple", "jkl": False}
                        },
                        {
                            "name": "feature 3",
                            "args": {}
                        },
                        ...
                    ]
                },
                "extractor_configuration": {
                    "fs": 8000
                }
            }

        It can be seen that the sample values can be multi-dimensional. The
        logic is that the last dimension of the D-dimensional sample values
        array for a particular subject stands for the number of samples in the
        array. E.g. in the case of 1-D data (N 1-D samples), it can be
        ``(1, N)`` or ``(N,)``, in the case of 2-D data (N 2-D samples), it
        is ``(2, N)``, etc.

        As the sample values are stored in a ``np.array``, they must be
        serialized before sending in the request. The featurizer API expects the
        samples to be JSON-serialized using a lightweight serialization library
        `json-tricks <https://json-tricks.readthedocs.io/en/latest/>`_. The API
        package also provides ``api.wrapper.data.DataWrapper.wrap_data``
        for serialization.

        **Output data**

        Structure of the output data is the following: it is a ``dict`` object
        with these field-value pairs (example bellow):

        - ``features`` (``dict``, mandatory)
        - ``features.values`` (``np.array``, mandatory)
        - ``features.labels`` (``list``, optional)

        .. code-block:: python

            # Example: 10 subjects, each having 5 2-D features (shape: (2, 5))
            {
                "features": {
                    "labels": ["feature 1", ... "feature 5"],
                    "values": np.array((10, 2, 5))
                }
            }

        The output feature values in the response object are JSON-serialized
        in the same way as the samples. So, to get the feature values
        ``np.array``, the deserialization must be performed after the response
        is obtained (``api.wrapper.data.DataWrapper.unwrap_data``; see the
        example bellow).

        **Workflow**

        1. Unwrap the input request
        2. Prepare and validate the data samples
        3. Prepare and validate the features pipeline/extractor configuration
        4. Prepare the features extractor
        5. Extract the features specified in the features pipeline
        6. Prepare and validate the features
        7. Wrap the output response
        8. Send the successful HTTP Response

        **Example**

        .. code-block:: python

            import numpy
            import requests
            from pprint import pprint
            from api.wrappers.data import DataWrapper

            # Prepare the samples (example: 10 subjects, each 100 1-D samples)
            samples = numpy.random.rand(10, *(1, 100))

            # Serialize the samples
            samples = DataWrapper.wrap_data(samples)

            # Prepare the featurization pipeline (example: 2 dummy features)
            features_pipeline = [
                {
                    "name": "feature 1",
                    "args": {"arg_x": 100, "arg_y": [1, 2, 3]}
                },
                {
                    "name": "feature 2",
                    "args": {"arg_z": True}
                }
            ]

            # Prepare the features extractor configuration (example: fs = 8000)
            extractor_configuration = {"fs": 8000}

            # Prepare the featurizer data
            body = {
                "samples": {
                    "values": samples
                },
                "features": {
                    "pipeline": features_pipeline
                },
                "extractor_configuration": extractor_configuration
            }

            # Prepare the authorization header (example: unreal JWT token)
            headers = {
                "Authorization": f"Bearer 123456789"
            }

            # Call the featurize endpoint (example: locally deployed API)
            response = requests.post(
                url="http://localhost:5000/featurize",
                json=body,
                headers=headers,
                verify=True,
                timeout=10)

            # Get the features
            values = response.json().get("features").get("values")
            labels = response.json().get("features").get("labels")

            # Deserialize the features
            values = DataWrapper.unwrap_data(values)

            pprint(values)
            pprint(labels)
        """

        try:

            # Featurize the input data samples with the specified features extraction pipeline
            #
            #  1. Unwrap the input request
            #  2. Prepare and validate the data samples
            #  3. Prepare and validate the features pipeline and the features extractor configuration
            #  4. Prepare the features extractor
            #  5. Extract the features specified in the features pipeline
            #  6. Prepare and validate the features
            #  7. Wrap the output response
            #  8. Send the successful HTTP Response

            # Unwrap the input request
            request = RequestWrapper.unwrap_request(flask.request)
            self.log_request_data(request)

            # Prepare and validate the data samples
            samples = Sample.from_request(request)

            # Prepare and validate the features pipeline and the features extractor configuration
            pipeline = FeaturesPipeline.from_request(request)
            settings = FeaturesExtractorConfiguration.from_request(request)

            # Prepare the features extractor
            extractor = FeaturesExtractorPipeline(self.extractor_interface, samples, settings)

            # Extract the features specified in the features pipeline
            features = extractor.extract(pipeline)

            # Prepare and validate the features
            features = Features(features).to_response()
            self.log_response_data(features)

            # Wrap the output response
            response = ResponseWrapper.wrap_response(features)

            # Send the successful HTTP Response
            return flask.Response(response=response, status=HTTPStatus.OK, mimetype="application/json")

        # Handle the error logging
        except Exception as e:
            self.application_logger.error(e)
            raise
