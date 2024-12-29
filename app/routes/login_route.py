from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.exception_handler.handler import handle_exceptions
from app.inputs.login_input import LoginInput
from app.service.login_service import generate_token
from logger import setup_logger

login_bp = Blueprint('login', __name__)

log = setup_logger()


@login_bp.route('/', methods=['POST'])
@handle_exceptions
def login():
    payload = request.get_json()

    login_input = LoginInput()

    try:
        # Validate and deserialize input data
        user_data = login_input.load(payload)
        response = generate_token(user_data)
        return jsonify(response), 200
    except ValidationError as err:
        # If validation fails, return errors
        return jsonify({"errors": err.messages}), 401
