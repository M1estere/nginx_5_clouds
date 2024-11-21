from app.constants import ERROR_500_TEXT
from app.models import User


def make_user_id_cache_key(*args, **kwargs):
    """User id cache key"""
    user_id = kwargs['user_id']
    return f'user_data::{user_id}'


def internal_error_response(err):
    """
    Returns error response
    :param err: Exception
    :return: dict
    """
    return {
        'message': ERROR_500_TEXT,
        'error': str(err)
    }, 500


def is_user_exist(email):
    """
    Check if user with email exist in database
    :param email:
    :return:
    """
    user_with_email = User.query.filter_by(email=email).first()
    return user_with_email is not None
