from api.common.logging import get_application_logger
from api.featurization.library_injection.imports import *


# ------------------------------------------------- #
# Features extraction library validation definition #
# ------------------------------------------------- #

def validate_features_library(features_extraction_library_name):
    """Returns the injected features extraction library"""
    try:
        validate_importing_features_extraction_library(features_extraction_library_name)
    except Exception as e:
        get_application_logger().error(f"Injected features extraction library cannot be imported: {e}")
        exit(-1)


def get_validated_features_extractor(features_extraction_library):
    """Returns the injected features extractor"""
    try:
        return import_features_extractor(features_extraction_library)
    except Exception as e:
        get_application_logger().error(e)
        return None


def get_validated_features_extractor_exceptions(features_extraction_library):
    """Returns the injected features extractor exceptions"""
    return import_features_extractor_exceptions(features_extraction_library)
