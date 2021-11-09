from api.common.logging import get_application_logger
from api.featurization.library_injection.validation import (
    validate_features_library,
    get_validated_features_extractor,
    get_validated_features_extractor_exceptions
)


# --------------------------------------- #
# Features extractor injection definition #
# --------------------------------------- #

def inject_features_extractor(features_extractor_library_name):
    """Injects the feature extractor from the external library"""

    # Import the features extractor
    features_extraction_interface = get_validated_features_extractor(features_extractor_library_name)
    if not features_extraction_interface:
        get_application_logger().error(f"Injected features extractor cannot be imported")
        exit(-1)

    # Return the injected features extractor
    return features_extraction_interface


def inject_features_extractor_exceptions(features_extractor_library_name):
    """Injects the feature extractor exceptions from the external library"""
    return get_validated_features_extractor_exceptions(features_extractor_library_name)
