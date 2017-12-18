from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
    Function that gets called when user calls the /auth endpoint
    with their username and password
    :param username: user's username in str format
    :param password: user's un-encrypted password
    :return: A UserModel bject when authentication was successful, None if not.
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def indetity(payload):
    """
    function that gets called when user is authenticated and Flask-JWT
    verified their authorization header is correct
    :param payload: A dictionary with 'identity' key which is user id.
    :return: A UserModel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
