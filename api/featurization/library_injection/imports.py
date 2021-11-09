import importlib


# --------------------------------------------------------------------- #
# Features extraction library/interface injection exceptions definition #
# --------------------------------------------------------------------- #
class FeaturesExtractionLibraryNotDefinedException(Exception): pass
class FeaturesExtractionLibraryNotInstalledException(Exception): pass
class FeaturesExtractionLibraryImportFailedException(Exception): pass
class FeaturesExtractorNotImportableException(Exception): pass


# ------------------------------------------------------- #
# Features extraction library/interface import definition #
# ------------------------------------------------------- #

def validate_importing_features_extraction_library(library_name):
    """Validate the import of the injected features extraction library"""

    # Check if the features extraction library is specified
    if not library_name:
        raise FeaturesExtractionLibraryNotDefinedException("Features extraction library not specified")

    # Try to import the library
    #
    # 1. import <library_name>
    # 2. import <library_name>.interface
    # 3. import <library_name>.interface.featurizer
    # 4. import <library_name>.interface.featurizer.exceptions
    try:
        importlib.import_module(f"{library_name}")
        importlib.import_module(f"{library_name}.interface")
        importlib.import_module(f"{library_name}.interface.featurizer")

    except (ModuleNotFoundError, ImportError):
        raise FeaturesExtractionLibraryNotInstalledException("Features extraction library not installed")
    except Exception as e:
        raise FeaturesExtractionLibraryImportFailedException(f"Features extraction library import failed: {e}")


def import_features_extractor(library_name):
    """Injects the features extractor from the library module"""
    try:

        # Get the features extractor
        interface = importlib.import_module(f"{library_name}.interface.featurizer")
        interface = getattr(interface, "FeatureExtractor")

        # Return the features extractor
        return interface

    except AttributeError:
        raise FeaturesExtractorNotImportableException("Features extractor cannot be imported")


def import_features_extractor_exceptions(library_name):
    """Injects the features extractor from the library module"""
    try:

        # Get the features extractor exceptions
        exceptions = importlib.import_module(f"{library_name}.interface.featurizer.exceptions")
        exceptions = [getattr(exceptions, e) for e in dir(exceptions) if not e.startswith("__")]
        exceptions = [e for e in exceptions if issubclass(e, Exception)]

        # Return the features extractor exceptions
        return exceptions

    except AttributeError:
        return []
