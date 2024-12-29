from flask_jwt_extended import current_user
from sqlalchemy import and_

from app import db
from app.exception_handler.custom_exception import NotFoundError, BadRequestError
from app.models import User
from logger import setup_logger

log = setup_logger()


def get_user_by_id(id: int) -> User:
    return db.session.query(User).filter(User.id == id).first()


def get_user_by_id_and_password(id: int, password: str) -> User:
    return db.session.query(User).filter(and_(User.id == id, User.password == password)).first()


def get_user_by_email_password(email: str, password: str) -> User:
    return db.session.query(User).filter(and_(User.email == email, User.password == password)).first()


def get_user_by_email(email: str) -> User:
    return db.session.query(User).filter(User.email == email).first()


def create_user_obj(user_data: dict) -> User:
    try:
        if get_user_by_email(user_data.get("email")):
            log.error("User with the given email is already exist")
            raise BadRequestError(message="Account with this email is already exist")

        user = User()

        user.first_name = user_data.get("first_name")
        user.last_name = user_data.get("last_name")
        user.full_name = user.first_name + " " + user.last_name
        user.contact_no = user_data.get("contact_no")
        user.email = user_data.get("email")
        user.password = user_data.get("password")
        user.room_no = user_data.get("room_no")

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user.to_dict()
    except Exception as e:
        log.error(f"Something went wrong {str(e)}")
        raise e


def update_user_obj(user_data: dict) -> User:
    user = get_user_by_id(current_user.id)

    if not user:
        raise NotFoundError("User Not Found for the given id ")

    user.first_name = user_data.get("first_name")
    user.last_name = user_data.get("last_name")
    user.full_name = user.first_name + " " + user.last_name
    user.contact_no = user_data.get("contact_no")
    user.email = user_data.get("email")
    user.room_no = user_data.get("room_no")

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return user.to_dict()


def update_user_password(payload: dict) -> User:
    user = get_user_by_id_and_password(current_user.id, payload.get("old_password"))

    if not user:
        raise NotFoundError("User Not Found for the given id and old password")

    user.password = user.get("new_password")

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return user.to_dict()
