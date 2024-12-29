import json

from flask import jsonify

from app.service.user_service import get_user_by_email


def user_lookup_callback(_jwt_headers, jwt_data):
    identity = json.loads(jwt_data["sub"])

    if identity.get('email', None) is None:
        return None

    return get_user_by_email(identity.get('email'))


def make_additional_claims(identity):
    if identity == "janedoe123":
        return {"is_staff": True}
    return {"is_staff": False}


# jwt error handlers

def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "Token has expired", "error": "token_expired"}), 401


def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed", "error": "invalid_token"}
        ),
        401,
    )


def missing_token_callback(error):
    return (
        jsonify(
            {
                "message": "Request doesnt contain valid token",
                "error": "authorization_header",
            }
        ),
        401,
    )
