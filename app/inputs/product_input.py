from marshmallow import Schema, fields, EXCLUDE


class ProductInput(Schema):
    type = fields.String(
        required=True
    )
    details = fields.String(
        required=True
    )
    expiry_date = fields.DateTime(
        required=True
    )

    class Meta:
        unknown = EXCLUDE


class ProductUpdate(Schema):
    id = fields.Integer(
        required=True
    )
    type = fields.String(
        required=True
    )
    details = fields.String(
        required=True
    )
    expiry_date = fields.DateTime(
        required=True
    )

    class Meta:
        unknown = EXCLUDE
