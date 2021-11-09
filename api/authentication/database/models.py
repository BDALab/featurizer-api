from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.authentication.database import db


# ------------------------------------------ #
# Authentication database mapping definition #
# ------------------------------------------ #

class BaseModel(db.Model):
    """Base model for authentication user model"""

    # Set the class to be abstract
    __abstract__ = True

    # Common fields
    #
    #  1. id, mandatory, primary key
    #  2. created_on, mandatory
    #  3. updated_on, mandatory
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def save(self):
        """Saves an instance of the model from the database"""
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        except SQLAlchemyError:
            db.session.rollback()

    def update(self):
        """Updates an instance of the model from the database"""
        return db.session.commit()

    def delete(self):
        """Deletes an instance of the model from the database"""
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()


class User(BaseModel):
    """Class implementing authentication user model"""

    # User fields
    #
    #  1. username, mandatory
    #  2. password, mandatory
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    @classmethod
    def get_by_username(cls, username):
        """Returns a user instance given the username"""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_identifier(cls, uid):
        """Returns a user instance given the identifier"""
        return cls.query.filter_by(id=uid).first()

    def hash_password(self):
        """Generates the password hash"""
        self.password = generate_password_hash(str(self.password)).decode("utf8")

    def check_password(self, password):
        """Checks if the password hashes are equal"""
        return check_password_hash(str(self.password), password)

    @classmethod
    def authenticate(cls, **kwargs):
        """Authenticates a user given the provided arguments"""

        # Parse the mandatory user fields
        username = kwargs.get("username")
        password = kwargs.get("password")
        if not username or not password:
            return None

        # Get the user and authenticate the provided passwords
        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        # Return the user instance
        return user
