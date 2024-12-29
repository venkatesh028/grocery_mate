from marshmallow import Schema, fields, validate, EXCLUDE


class UserRegisterInput(Schema):
    email = fields.String(
        required=True,
        validate=[
            validate.Email(error="Invalid email format"),
            validate.Length(min=6, max=120, error="Email length must be between 6 and 120 characters")
        ]
    )
    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, error="Password must be at least 8 characters long"),
            validate.Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$',
                            error="Password must contain letters and numbers")
        ]
    )
    contact_no = fields.String(
        required=True,
        validate=validate.Regexp(r'^\+?[1-9]\d{1,14}$', error="Invalid phone number format")
    )
    first_name = fields.String(
        required=True
    )
    last_name = fields.String(
        required=True
    )
    room_no = fields.String(
        required=True
    )

    class Meta:
        unknown = EXCLUDE


class UserUpdateInput(Schema):
    email = fields.String(
        required=True,
        validate=[
            validate.Email(error="Invalid email format"),
            validate.Length(min=6, max=120, error="Email length must be between 6 and 120 characters")
        ]
    )
    contact_no = fields.String(
        required=True,
        validate=validate.Regexp(r'^\+?[1-9]\d{1,14}$', error="Invalid phone number format")
    )
    first_name = fields.String(
        required=True
    )
    last_name = fields.String(
        required=True
    )
    room_no = fields.String(
        required=True
    )

    class Meta:
        unknown = EXCLUDE


class UserPasswordInput(Schema):

    old_password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, error="Old Password must be at least 8 characters long"),
            validate.Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$',
                            error="Password must contain letters and numbers")
        ]
    )
    new_password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, error="New Password must be at least 8 characters long"),
            validate.Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$',
                            error="Password must contain letters and numbers")
        ]
    )


    class Meta:
        unknown = EXCLUDE

