import sys
import subprocess
import importlib
from api.configuration import load_configuration


# ----------------------------------------------------------------------------------- #
# Features extraction library/interface injection configuration exceptions definition #
# ----------------------------------------------------------------------------------- #
class FeaturesExtractionLibraryInjectionTypeNotDefinedException(Exception): pass
class FeaturesExtractionLibraryInjectionTypeNotSupportedException(Exception): pass
class FeaturesExtractionLibraryLocalInjectionException(Exception): pass
class FeaturesExtractionPipInjectionException(Exception): pass
class FeaturesExtractionPipInstallationException(Exception): pass


# --------------------------------- #
# Configuration routines definition #
# --------------------------------- #

def configure_features_extraction_library_injection():
    """Configures the API features extraction library injection"""

    # Load the features extractor configuration
    configuration = load_configuration("injection.json")["features_extraction_library"]

    # Get the injection type
    injection_type = configuration.get("injection_type")
    if not injection_type:
        raise FeaturesExtractionLibraryInjectionTypeNotDefinedException(f"Injection type undefined")
    if injection_type not in configuration.get("injection_types"):
        raise FeaturesExtractionLibraryInjectionTypeNotSupportedException(f"Injection type unsupported")

    # Get the injection type-specific configuration
    injection_configuration = configuration.get("injection").get(injection_type)

    # Get the features extraction installation and import names
    install_name = injection_configuration.get("installation_name")
    import_name = injection_configuration.get("import_name")
    if injection_type == "pip":
        if not all((install_name, import_name)):
            raise FeaturesExtractionPipInjectionException(f"Missing installation/import name")
    else:
        if not import_name:
            raise FeaturesExtractionLibraryLocalInjectionException(f"Missing import name")

    # Install the features extraction library
    if injection_type == "pip":
        try:
            install_features_extraction_library(install_name)
        except Exception as e:
            raise FeaturesExtractionPipInstallationException(f"Features extraction library installation failed: {e}")

    # Return the features extraction library import name
    return import_name


# -------------------------------- #
# Installation routines definition #
# -------------------------------- #

def install_features_extraction_library(library_name):
    """Installs the features extraction library (if pip-installable)"""
    try:
        importlib.import_module(library_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
