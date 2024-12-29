from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.exception_handler.handler import handle_exceptions
from app.inputs.product_input import ProductInput, ProductUpdate
from app.service.product_service import create_product_obj, update_product_obj, mark_as_sold, upload_to_s3, \
    get_all_product, get_all_my_product
from logger import setup_logger

product_bp = Blueprint('product', __name__)

log = setup_logger()


@product_bp.route('/', methods=['POST'])
@handle_exceptions
@jwt_required()
def create_product():
    data = request.get_json()

    product_input = ProductInput()

    try:
        # Validate and deserialize input data
        user_data = product_input.load(data)
        response = create_product_obj(user_data)
        return jsonify(response), 201
    except ValidationError as err:
        # If validation fails, return errors
        return jsonify({"errors": err.messages}), 400


@product_bp.route('/update', methods=['PUT'])
@handle_exceptions
@jwt_required()
def update_product():
    data = request.get_json()

    product_input = ProductUpdate()

    try:
        # Validate and deserialize input data
        user_data = product_input.load(data)
        response = update_product_obj(user_data)
        return jsonify(response), 200
    except ValidationError as err:
        # If validation fails, return errors
        return jsonify({"errors": err.messages}), 400


@product_bp.route('/sold/<product_id>', methods=['PUT'])
@handle_exceptions
@jwt_required()
def update_sold_status(product_id):
    mark_as_sold(product_id)
    return jsonify({"message": "Updated the sold status"}), 200


@product_bp.route('/image/<product_id>', methods=['POST'])
@handle_exceptions
@jwt_required()
def upload_product_image(product_id):
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    return upload_to_s3(file, product_id), 200


@product_bp.route('/all', methods=['GET'])
@handle_exceptions
@jwt_required()
def get_all_products():
    return get_all_product()


@product_bp.route('/myproducts', methods=['GET'])
@handle_exceptions
@jwt_required()
def get_all_my_products():
    return get_all_my_product()
