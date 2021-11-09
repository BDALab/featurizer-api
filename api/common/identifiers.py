import uuid


# ------------------------------ #
# Identifier routines definition #
# ------------------------------ #

def get_identifier():
    """Return a unique identifier"""
    return uuid.uuid4().hex
