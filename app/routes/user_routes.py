from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError

from app.exception_handler.custom_exception import NotFoundError
from app.exception_handler.handler import handle_exceptions
from app.inputs.user_input import UserRegisterInput, UserUpdateInput
from app.service.user_service import create_user_obj, update_user_obj, get_user_by_id, update_user_password
from logger import setup_logger

user_bp = Blueprint('user', __name__)

log = setup_logger()


@user_bp.route('/register', methods=['POST'])
@handle_exceptions
def create_user():
    log.info("Inside the create user function")
    data = request.get_json()

    user_register_input = UserRegisterInput()

    try:
        # Validate and deserialize input data
        user_data = user_register_input.load(data)
        response = create_user_obj(user_data)
        return jsonify(response), 201
    except ValidationError as err:
        # If validation fails, return errors
        return jsonify({"errors": err.messages}), 400


@user_bp.route('/update', methods=['PUT'])
@handle_exceptions
@jwt_required()
def update_user():
    log.info("Inside the update user function")
    data = request.get_json()

    user_update_input = UserUpdateInput()

    try:
        # Validate and deserialize input data
        user_data = user_update_input.load(data)
        response = update_user_obj(user_data)
        return jsonify(response), 201
    except ValidationError as err:
        # If validation fails, return errors
        return jsonify({"errors": err.messages}), 400


@user_bp.route('/updatePassword', methods=['PUT'])
@handle_exceptions
@jwt_required()
def update_password():
    log.info("Inside the update user function")
    data = request.get_json()

    user_update_input = UserUpdateInput()

    try:
        # Validate and deserialize input data
        user_data = user_update_input.load(data)
        response = update_user_password(user_data)
        return jsonify(response), 201
    except ValidationError as err:
        # If validation fails, return errors
        return jsonify({"errors": err.messages}), 400


@user_bp.route('/<user_id>', methods=['GET'])
@handle_exceptions
@jwt_required()
def get_user(user_id):
    log.info("Inside get the user")

    if user_id is None:
        return {"errors": "user id is missing in path"}, 400

    if int(user_id) < 0:
        return {"errors": "user cant be less than 0"}, 400

    user = get_user_by_id(int(user_id))

    if user is None:
        raise NotFoundError(message="User not found for the given id")

    return jsonify(user.to_dict())


@user_bp.route('/', methods=['GET'])
@handle_exceptions
@jwt_required()
def get_my_data():
    log.info("Inside get the current user")
    return jsonify(current_user.to_dict()), 200
