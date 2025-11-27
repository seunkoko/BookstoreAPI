from marshmallow import fields, validate

from bookstore_api.app.extensions import ma
from bookstore_api.app.helpers import is_strong_password

def validate_strong_password(password):
    if not is_strong_password(password):
        raise validate.ValidationError("Password must be strong.")


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(
        required=True,
        validate=validate.Length(min=3, error="Username must be at least 3 chars long.")
    )
    email = fields.String(
        required=True,
        validate=validate.Length(min=5, error="Email must be at least 5 chars long.")
    )
    password = fields.String(required=True, validate=[
        validate.Length(min=8),
        validate_strong_password
    ], load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    reviews = fields.Nested('ReviewSchema', many=True, exclude=['user'])
    role = fields.Nested('RoleSchema', only=['name'])

user = UserSchema()
users = UserSchema(many=True)
