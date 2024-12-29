import json
from datetime import timedelta

from flask_jwt_extended import create_access_token

from app.exception_handler.custom_exception import InvalidCredential
from app.service.user_service import get_user_by_email_password


def generate_token(payload: dict):
    user = get_user_by_email_password(payload.get('email'), payload.get('password'))

    if not user:
        raise InvalidCredential(message="Invalid User Credentials")

    access_token = create_access_token(
        identity=json.dumps({"name": user.first_name, "email": user.email}),
        expires_delta=timedelta(days=10)
    )

    return {"access_token": access_token}
