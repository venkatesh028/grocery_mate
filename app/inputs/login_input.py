from marshmallow import Schema, fields, validate, EXCLUDE


class LoginInput(Schema):
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

    class Meta:
        unknown = EXCLUDE

