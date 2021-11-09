# Featurizer API

![GitHub last commit](https://img.shields.io/github/last-commit/BDALab/featurizer-api)
![GitHub issues](https://img.shields.io/github/issues/BDALab/featurizer-api)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/BDALab/featurizer-api)
![GitHub top language](https://img.shields.io/github/languages/top/BDALab/featurizer-api)
![GitHub](https://img.shields.io/github/license/BDALab/featurizer-api)

**Server side application**:

This package provides a modern RESTFull featurizer API created using Python programming language and [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) library. It is designed to be used for various feature extraction libraries due to its feature injection capabilities (instructions are provided in the [Configuration](#Configuration) section) and flexible input/output data definition (multi-dimensional samples/features, multiple subjects, etc.). On top of that, the featurizer API provides endpoints for user authentication and JWT-based request authorization, it supports handling of cross-origin resource sharing, request-response caching, advanced logging, etc. It comes also with the basic support for containerization via Docker (Dockerfile and docker-compose).

**Client side application**:

To make the use of the Featurizer API as easy as possible, there is a [PyPi-installable](https://pypi.org/project/featurizer-api-client/) lightweight client side application named [Featurizer API client](https://github.com/BDALab/featurizer-api-client/) that provides method-based calls to all endpoints accessible on the API. For more information about the Featurizer API client, please read the official [readme](https://github.com/BDALab/featurizer-api-client#readme) and [documentation](https://github.com/BDALab/featurizer-api-client/tree/master/docs).

**Endpoints**:
1. featurization endpoints (`api/resources/featurizer`)
    1. `/featurize` - calls `.extract` on the specified features-extractor (featurizer interface). This endpoint is designed to be used to compute the features specified in the features-extraction pipeline.
2. security endpoints (`api/resources/security`)
    1. `/signup` - signs-up a new user.
    2. `/login` - logs-in an existing user (obtains access and refresh JWT tokens).
    3. `/refresh` - refreshes an expired access token (obtains refreshed FWT access token).

_The full programming sphinx-generated docs can be seen in `docs/`_.

**Contents**:
1. [Installation](#Installation)
2. [Configuration](#Configuration)
3. [Featurization](#Featurization)
4. [Injection](#Injection)
5. [Workflow](#Workflow)
6. [Data](#Data)
7. [Examples](#Examples)
8. [License](#License)
9. [Contributors](#Contributors)

---

## Installation

```
# Clone the repository
git clone https://github.com/BDALab/featurizer-api.git

# Install packaging utils
pip install --upgrade pip
pip install --upgrade virtualenv

# Change directory
cd featurizer-api

# Activate virtual environment
# Linux
# Windows

# Linux
virtualenv .venv
source .venv/bin/activate

# Windows
virtualenv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Create .env file with the JWT secret key (see the configuration section bellow)
```

## Configuration

The package provides various configuration files stored at `api/configuration`. More specifically, the following configuration is provided:
1. authentication (`api/configuration/authentication.json`): it supports the configuration of the database of users. In this version, the `sqlite` database is used for simplicity. The main configuration is the URI for the `*.db` file (pre-set to `api/authentication/database/database/database.db`). An empty database file is created automatically.
2. authorization (`api/configuration/authorization.json`): it supports the configuration of the request authorization. In this version, the JWT authorization is supported. The main configuration is the name of the `.env` file that stores the JWT secret key. For security reasons, the `.env` file is not part of this repository, i.e. **before using the API, it is necessary to create the .env file** at `api`-level, i.e. `api/.env` **and set the JWT_SECRET_KEY** field (e.g. `JWT_SECRET_KEY: "wfTHu38GpF5y60djwKC0EkFj586jdyZR"`).
3. cors (`api/configuration/cors.json`): it supports the configuration of the cross-origin resource sharing. In this version, no sources are added to the `origins`, (to be updated per deployment).
4. caching (`api/configuration/caching.json`): it supports the configuration of API request-response caching. In this version, the simple in-memory caching with the TTL of 60 seconds is used.
5. logging (`api/configuration/logging.json`): it supports the configuration of the logging. The package provides logging on three levels: (a) request, (b) response, (c) werkzeug. The log files are created in the `logs` directory located at the featurizer's root directory.
6. featurization (`api/configuration/injection.json`): it supports the configuration of the features-extraction library injection. The main configuration is the name of the library to be injected. **By design, the features-extraction library is not part of the `requirements.txt` and must be installed separately**. The injection of the feature extractor as well as the requirements on the features-extraction library and the process of featurization are summarized in the [Featurization](#Featurization) and [Injection](#Injection) sections.

## Featurization

The featurizer API provides featurization interface class `FeaturesExtractorPipeline` located at `api/featurization/interface` that accepts a specific injected feature extractor class and the extractor's configuration. It also provides the `extract` method accepting data to be featurized and the pipeline of features to be extracted. To featurize the data, it calls the `extract` method on the initialized and configured feature extractor instance. The definition of the featurization interface class can be seen bellow.

```python
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
```

The features-extraction library must implement the `FeatureExtractor` class serving as an interface between the featurizer API and the features-extraction library. The interface must be placed at `<library>/interface/featurizer`. As shown above, the feature extractor must accept `**extractor_configuration` in its `__init__` method to enable passing the configuration (the configuration is optional on the library level, but the interface must be consistent). An example template of the feature extractor interface is shown bellow.

```python
class FeatureExtractor(object):
    """
    Class implementing the features extractor interface for the Featurizer API.

    For more information about featurizer, see the following repositories:
    1. [server side](#github.com/BDALab/featurizer-api)
    1. [client side](#github.com/BDALab/featurizer-api-client)

    For more information about the attributes, see: ``extract(...)``
    """

    def __init__(self, values, labels=None, **configuration):
        """
        Initializes the FeatureExtractor featurizer API interface.

        :param values: data values to extract the features from
        :type values: numpy.ndarray
        :param labels: data labels for data samples, defaults to None
        :type labels: list, optional
        :param configuration: common extractor configuration
        :type configuration: **kwargs, optional
        """

        # Set the data values/labels
        self.values = values
        self.labels = labels if labels else []

        # Set the extractor configuration
        self.configuration = configuration if configuration else {}

    def extract(self, pipeline):
        """
        Interface method: extract the features.

        **Data**

        1. data is of type: ``numpy.ndarray``.
        2. data is mandatory.
        3. data shape: In general, data to have the shape (M, ..., D). Where M
           stands for subjects (i.e. subjects are in the first dimension), and
           D stands for D data samples (of shape ...).
            1. in the case of data having the following shape: (D, ), the API
               assumes it is a vector of D data sample points for one subject.
               It transforms the data to a row vector: (1, D) to add the
               dimension for the subject.
            2: in the case of data having the following shape: (M, ..., D),
               the API does not transform the data, but it assumes there are
               M subjects abd D data samples, each having (...) dimensionality,
               e.g. if data has the shape (M, 3, 10) it means that there are
               M subjects and each of the subjects has 10 data samples (each
               being three dimensional).

        **Labels**

        1. labels are of type: ``list``.
        2. labels are optional.
        3. labels are of length D (for each data sample, there is one label)

        **Configuration**

        1. configuration are of type: ``dict``.
        2. configuration is optional.
        3. configuration provides common kwargs for feature extraction

        **Pipeline**

        1. pipeline is of type: ``list``.
        2. pipeline is mandatory.
        3. each element in the pipeline is of type: ``dict``.
        4. each element in the pipeline has the following keys: a) ``name``
           to hold the name of the feature to be computed, and b) ``args``
           to hold the arguments (kwargs) for the specific feature extraction
           method that is going to be used (it is of type: ``dict``).

        **Output**

        The extracted features follow the same shape convention as the input
        data: the subjects are in the first dimension, and the features are
        in the last dimension (each feature having shape ...).

        :param pipeline: pipeline of the features to be extracted
        :type pipeline: list
        :return: extracted features and labels
        :rtype: dict {"features": ..., "labels": ...}
        """

        # TODO: computation (implement the feature extraction)
        values, labels = None, None

        # Return the extracted features and feature labels
        return {
            "features": values,
            "labels": labels
        }
```

## Injection

To inject the features-extraction library and to get the feature extractor, the featurizer API uses two functions: (a) `import_features_extractor` (abbr. _inject extractor_ function), and (b) `import_features_extractor_exceptions` (abbr. _inject exceptions_ function), both located at `api/featurization/library_injection/imports`. First, it uses the _inject extractor_ function to get the feature extractor class `FeatureExtractor` from `<library_name>.interface.featurizer` and then it uses the _inject exceptions_ function to get the feature extractor-specific exceptions from `<library_name>.interface.featurizer.exceptions` to be handled as client-side errors. The `<library_name>` **must be specified** at `api/configuration/injection.json` and it **must be installed manually before the API can be used**.

## Workflow

In order for a user to use the API, the following steps are required:
1. a new user must be created via the `/signup` endpoint
2. the existing user must log-in to get the access and refresh tokens via the `login` endpoint
3. calls to the `/featurize` endpoint can be made 
4. if the access token expires, a new one must be obtained via the `/refresh` endpoint

For specific examples for each step of the workflow, see the [Examples](#Examples) section.

## Data

### Input data

Structure of the input data is the following: it is a ``dict`` object with these field-value pairs (example bellow):
- ``samples`` (``dict``, mandatory; _placeholder for the sample values/labels_)
- ``samples.values`` (``numpy.array``, mandatory; _sample values_)
- ``samples.labels`` (``list``, optional; _sample labels_)
- ``features`` (``dict``, mandatory; _placeholder for the features-extraction pipeline_)
- ``features.pipeline`` (``list``, mandatory; _features-extraction pipeline_)
- ``features.pipeline[0..., F]`` (``dict``, mandatory; _single feature configuration_)
- ``extractor_configuration`` (``dict``, optional; _features-extractor configuration_)

**Shape**:

Shape of the sample values: (first dimension, (inner dimensions), last dimension)

- the first dimension is dedicated to subjects
- the inner dimensions are dedicated to the dimensionality of the samples
- the last dimension is dedicated to samples

Important requirement that must be met is to provide the features-extractor with the data it can process (shape, format, etc.).

```
# Example:
# - M subjects, D samples of (... dimensions)
# - N features in the pipeline
# - sampling frequency (fs) in the extractor configuration
{
    "samples": {
        "labels": ["element 1", ... "element D"],
        "values": np.array((M, ..., D))
    },
    "features": {
        "pipeline": [
            {
                "name": "feature 1",
                "args": {"abc": 123, "def": 456}
            },
            ...
            {
                "name": "feature N",
                "args": {}
            },
            ...
        ]
    },
    "extractor_configuration": {"fs": 8000}
}
```

**Examples**:

- 100 subjects, each having 30 1-D samples (shape `(1,)` or shape `(1, 1)`): `shape = (100, 1, 30)`
- 250 subjects, each having 20 2-D samples (shape `(2,)` or shape `(1, 2)`): `shape = (250, 2, 20)`
- 500 subjects, each having 10 samples with the shape of `(3, 4)`: `shape = (500, 3, 4, 10)`

### Output data

Structure of the output data is the following: it is a ``dict`` object with these field-value pairs (example bellow):
- ``features`` (``dict``, mandatory; _placeholder for the feature values/labels_)
- ``features.values`` (``numpy.array``, mandatory; _feature values_)
- ``features.labels`` (``list``, optional; _feature labels_)

**Shape**:

Shape of the feature values: (first dimension, (inner dimensions), last dimension)

- the first dimension is dedicated to subjects
- the inner dimensions are dedicated to the dimensionality of the features
- the last dimension is dedicated to features

```
# Dimensions: M subjects, N features of (... dimensions)
{
    "features": {
        "labels": ["feature 1", ... "feature N"],
        "values": array of shape (M, ..., N)
    }
}
```

**Examples**:

- 100 subjects, each having 30 1-D samples (shape `(1,)` or shape `(1, 1)`), samples shape: `(100, 1, 30)`; 1000 1-D features, features shape `(100, 1, 1000)`
- 250 subjects, each having 20 2-D samples (shape `(2,)` or shape `(1, 2)`), samples shape: `(250, 2, 20)`; 100 2-D features, features shape: `(250, 2, 100)`
- 500 subjects, each having 100 samples with the shape of `(3, 4)`, samples shape: `(500, 3, 4, 100)`); 50 features with the shape of `(5, 10, 15)`, features shape: `(500, 5, 10, 15, 50)`

### Serialization/deserialization

As the sample/feature values are stored as a ``numpy.array``, they must be JSON-serialized/deserialized. For this purpose, the package provides the ``api.wrapper.data.DataWrapper`` class.

## Examples

### User sign-up

```python
import requests

# Prepare the sign-up data (new user to be created)
body = {
    "username": "user123",
    "password": "pAsSw0rd987!"
}

# Call the sign-up endpoint (locally deployed API)
response = requests.post(
    "http://localhost:5000/signup",
    json=body)
```

### User log-in

```python
import requests

# Prepare the log-in data (already created user)
body = {
    "username": "user123",
    "password": "pAsSw0rd987!"
}

# Call the log-in endpoint (locally deployed API)
response = requests.post(
    "http://localhost:5000/login",
    json=body)

# Get the access and refresh tokens from the response
if response.ok:
    access_token = response.json().get("access_token")
    refresh_token = response.json().get("refresh_token")
```

### Featurization

```python
import numpy
import requests
from pprint import pprint
from api.wrappers.data import DataWrapper

# Set the number of subjects (10)
num_subjects = 10

# Set the shape of the samples for each subject (1, 100): 1-D sample vector with 100 samples
samples_shape = (1, 100)

# Prepare the sample values/labels (labels are optional)
values = numpy.random.rand(num_subjects, *samples_shape)
labels = [f"sample {i}" for i in range(samples_shape[-1])]

# Serialize the sample values
values = DataWrapper.wrap_data(values)

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
        "labels": values,
        "values": labels
    },
    "features": {
        "pipeline": features_pipeline
    },
    "extractor_configuration": extractor_configuration
}

# Prepare the authorization header (take the access_token obtained via /login endpoint)
headers = {
    "Authorization": f"Bearer <access_token>"
}

# Call the featurize endpoint (locally deployed API; endpoints: /featurize)
response = requests.post(
    url="http://localhost:5000/featurize",
    json=body,
    headers=headers,
    verify=True,
    timeout=10)

if response.ok:

    # Get the features
    values = response.json().get("features").get("values")
    labels = response.json().get("features").get("labels")
    
    # Deserialize the features
    values = DataWrapper.unwrap_data(values)
    
    pprint(values)
    pprint(labels)
```

### Expired access token refresh

```python
import requests

# Prepare the refresh headers (take the refresh_token obtained via /login endpoint)
headers = {
    "Authorization": f"Bearer <refresh_token>"
}

# Call the refresh endpoint (locally deployed API)
response = requests.post(
    "http://localhost:5000/refresh",
    headers=headers)

# Get the refreshed access token
if response.ok:
    access_token = response.json().get("access_token")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

This package is developed by the members of [Brain Diseases Analysis Laboratory](http://bdalab.utko.feec.vutbr.cz/). For more information, please contact the head of the laboratory Jiri Mekyska <mekyska@vut.cz> or the main developer: Zoltan Galaz <galaz@vut.cz>.