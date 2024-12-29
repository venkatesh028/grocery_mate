import uuid

from flask_jwt_extended import current_user
from sqlalchemy import and_

from app import db
from app.exception_handler.custom_exception import ProductNotFoundError
from app.models import Product
from app.utils import s3
from app.utils.s3 import generate_presigned_url

from config import Config
from logger import setup_logger

log = setup_logger()


def get_product_by_id(id: int, user_id: int):
    return db.session.query(Product).filter(and_(Product.id == id, Product.user_id == user_id)).first()


def get_all_product():
    products = db.session.query(Product).filter(
        and_(Product.is_sold == False, Product.user_id != current_user.id)).all()
    return [product.to_dict() for product in products]


def get_all_my_product():
    products = db.session.query(Product).filter(Product.user_id == current_user.id).all()
    return [product.to_dict() for product in products]


def create_product_obj(payload: dict):
    product = Product()

    product.type = payload.get('type')
    product.details = payload.get('details')
    product.expiry_date = payload.get('expiry_date')
    product.user_id = current_user.id

    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)
    return product.to_dict()


def update_product_obj(payload: dict):
    product = get_product_by_id(payload.get('id'), current_user.id)

    if not product:
        raise ProductNotFoundError(
            message=f"Invalid product id, there is no product for the given id {payload.get('id')}")

    product.type = payload.get('type')
    product.details = payload.get('details')
    product.expiry_date = payload.get('expiry_date')

    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)
    return product.to_dict()


def mark_as_sold(id: int):
    product = get_product_by_id(id, current_user.id)

    if not product:
        raise ProductNotFoundError(
            message=f"Invalid product id, there is no product for the given id {id}")

    product.is_sold = True

    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)
    return product.to_dict()


def upload_to_s3(file, product_id):
    product = get_product_by_id(product_id, current_user.id)

    if not product:
        raise ProductNotFoundError(
            message=f"Invalid product id, there is no product for the given id {id}")

    image_key = f"{str(uuid.uuid4())}/{file.filename}/"
    response = s3.upload_file(file, image_key, Config.S3_BUCKET_NAME)

    if response:
        product.image_url = generate_presigned_url(image_key)

    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)

    return product.to_dict()
