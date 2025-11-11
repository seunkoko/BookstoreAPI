from marshmallow import fields

from app.extensions import ma


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    reviews = fields.Nested('ReviewSchema', many=True, exclude=['user'])

user = UserSchema()
users = UserSchema(many=True)
