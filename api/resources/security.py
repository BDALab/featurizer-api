from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from http import HTTPStatus
from webargs import validate
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs
from api.authentication.database.models import User


# --------------------------------- #
# Security API Resources definition #
# --------------------------------- #

class BaseUserResource(Resource):
    """Base class for the user authentication and authorization resources"""

    # User model class definition
    model = User

    # Password validator definition
    password_validator = validate.Regexp(
        regex="^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*).{7,50}$",
        error="Password must meet: a) contain at least 1 letter and at least 1 number, b) between 6-50 characters"
    )

    # Sign-up form validator definition
    sign_up_form_validation = {
        "username": fields.Str(required=True, location="json"),
        "password": fields.Str(required=True, location="json", validate=password_validator)
    }

    # Sign-in form validator definition
    sign_in_form_validation = {
        "username": fields.Str(required=True, location="json"),
        "password": fields.Str(required=True, location="json")
    }


class SignupResource(BaseUserResource):
    """Class implementing sign-up API resource"""

    @use_kwargs(BaseUserResource.sign_up_form_validation)
    def post(self, username, password):
        """
        Signs-up a new user.

        :param username: name of the new user
        :type username: str
        :param password: password of the user (see: validation requirements)
        :type password: str
        :return: sign-up response data (username)
        :rtype: dict

        **Example**

        .. code-block:: python

            import requests

            # Prepare the sign-up data (example: new user)
            body = {
                "username": "user123",
                "password": "pAsSw0rd987!"
            }

            # Call the sign-up endpoint (example: locally deployed API)
            response = requests.post(
                "http://localhost:5000/signup",
                json=body)

            # Check if the user was created
            if response.ok:
                print(f"User {response.json().get('username')} created")
        """

        # Check if the user already exists
        if self.model.get_by_username(username):
            return {"message": "Username already exist"}, HTTPStatus.BAD_REQUEST

        # Create the new user
        user = self.model(username=username, password=password)
        user.hash_password()
        user.save()

        # Return the response
        return {"username": str(user.username)}, HTTPStatus.CREATED


class LoginResource(BaseUserResource):
    """Class implementing log-in API resource"""

    @use_kwargs(BaseUserResource.sign_in_form_validation)
    def post(self, username, password):
        """
        Logs-in an existing user.

        :param username: name of the existing user
        :type username: str
        :param password: password of the user
        :type password: str
        :return: log-in response data (username, access token, refresh token)
        :rtype: dict

        **Example**

        .. code-block:: python

            import requests

            # Prepare the log-in data (example: existing user)
            body = {
                "username": "user123",
                "password": "pAsSw0rd987!"
            }

            # Call the log-in endpoint (example: locally deployed API)
            response = requests.post(
                "http://localhost:5000/login",
                json=body)

            # Get the access and refresh tokens from the response
            if response.ok:
                access_token = response.json().get("access_token")
                refresh_token = response.json().get("refresh_token")
        """

        # Authenticate the user from the database
        user = User.authenticate(username=username, password=password)
        if not user:
            return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED

        # Create the token: a) access token, b) refresh token
        data = {
            "username": user.username,
            "access_token": create_access_token(identity=str(user.id), fresh=True),
            "refresh_token": create_refresh_token(identity=str(user.id))
        }

        # Return the response with the token
        return data, HTTPStatus.OK


class RefreshAccessTokenResource(Resource):
    """Class implementing refreshing of the access token API resource"""

    @jwt_required(refresh=True)
    def post(self):
        """
        Refreshes the access token.

        :return: refresh response data (refreshed access token)
        :rtype: dict

        **Example**

        .. code-block:: python

            import requests

            # Prepare the refresh headers
            headers = {
                "Authorization": f"Bearer <refresh_token>"
            }

            # Call the refresh endpoint (example: locally deployed API)
            response = requests.post(
                "http://localhost:5000/refresh",
                headers=headers)

            # Get the refreshed access token
            if response.ok:
                access_token = response.json().get("access_token")
        """

        # Get the user from the token
        current_user = get_jwt_identity()
        if not current_user:
            return {"message": "Invalid user"}, HTTPStatus.UNAUTHORIZED

        # Refresh the token
        token = create_access_token(identity=current_user, fresh=False)

        # Return the response with the fresh token
        return {"access_token": token}, HTTPStatus.OK
