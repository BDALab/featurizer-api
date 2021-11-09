from api.featurization.library_injection.imports import *


# ------------------------------------------------- #
# Features extraction library validation definition #
# ------------------------------------------------- #

def validate_features_library(features_extraction_library_name):
    """Returns the injected features extraction library"""
    validate_importing_features_extraction_library(features_extraction_library_name)


def get_validated_features_extractor(features_extraction_library):
    """Returns the injected features extractor"""
    return import_features_extractor(features_extraction_library)


def get_validated_features_extractor_exceptions(features_extraction_library):
    """Returns the injected features extractor exceptions"""
    return import_features_extractor_exceptions(features_extraction_library)
