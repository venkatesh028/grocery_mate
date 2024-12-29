import uuid
from datetime import datetime

from sqlalchemy import Text, DateTime, Boolean, UUID

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    contact_no = db.Column(db.String(255), nullable=False)
    room_no = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'contact_no': self.contact_no,
            'room_no': self.room_no
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    details = db.Column(Text)
    expiry_date = db.Column(DateTime)
    create_at = db.Column(DateTime, default=datetime.now)
    update_at = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_sold = db.Column(Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, nullable=False)
    image_url = db.Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'details': self.details,
            'expiry_date': self.expiry_date,
            'user_id': self.user_id,
            'create_at': self.create_at,
            'is_sold': self.is_sold,
            'image_url': self.image_url
        }
