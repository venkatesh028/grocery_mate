from flask_jwt_extended.exceptions import NoAuthorizationError

from app.exception_handler.custom_exception import AppError
from logger import setup_logger

from functools import wraps
from flask import jsonify

log = setup_logger()


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppError as e:
            response = {
                "error": e.message,
                "status": e.status_code
            }
            return jsonify(response), e.status_code
        except NoAuthorizationError as noe:
            response = {
                "error": str(noe),
                "status": 401
            }
            return jsonify(response), 401
        except Exception as e:
            # Handle other exceptions if necessary
            response = {
                'error': 'Internal Server Error',
                'message': str(e)
            }
            return jsonify(response), 500

    return wrapper
