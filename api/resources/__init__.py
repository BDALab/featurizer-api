from api.resources.security import SignupResource, LoginResource, RefreshAccessTokenResource
from api.resources.featurizer import FeaturizerResource


# ------------------------------------------- #
# Featurizer API Resources helpers definition #
# ------------------------------------------- #

def add_featurizer_resource(api, extractor):
    """Register featurizer resource"""
    api.add_resource(FeaturizerResource, "/featurize", resource_class_kwargs={"extractor_interface": extractor})


def add_signup_resource(api):
    """Registers signup resource"""
    api.add_resource(SignupResource, "/signup")


def add_login_resource(api):
    """Registers login resource"""
    api.add_resource(LoginResource, "/login")


def add_refresh_resource(api):
    """Registers refresh resource"""
    api.add_resource(RefreshAccessTokenResource, "/refresh")


# ------------------------------------- #
# Featurizer API Resources registration #
# ------------------------------------- #

def configure_routes(api, feature_extractor_interface):
    """
    Prepares and registers the resources supported by the featurizer API.

    :param api: api instance
    :type api: flask_restful.API
    :param feature_extractor_interface: features extraction interface
    :type feature_extractor_interface: object instance
    :return: None
    :rtype: None type
    """

    # Register the resources
    #
    #  1. add and register the FeaturizerResource
    #  2. add and register the SignupResource
    #  3. add and register the LoginResource
    #  4. add and register the RefreshAccessTokenResource
    add_featurizer_resource(api, extractor=feature_extractor_interface)
    add_signup_resource(api)
    add_login_resource(api)
    add_refresh_resource(api)
