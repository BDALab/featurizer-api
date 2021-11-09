from flask_sqlalchemy import SQLAlchemy


# ----------------------------------------- #
# Authentication database object definition #
# ----------------------------------------- #
db = SQLAlchemy()


# -------------------------------------- #
# Authentication database initialization #
# -------------------------------------- #

def initialize_database(app):
    """
    Prepares and registers the authentication database supported by the API.

    :param app: app instance
    :type app: flask.Flask
    :return: None
    :rtype: None type
    """

    # Register the initialize the authentication database object to the application
    db.init_app(app)

    # Create the tables if needed
    with app.app_context():
        db.create_all()
