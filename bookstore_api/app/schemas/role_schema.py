from marshmallow import fields

from bookstore_api.app.extensions import ma


class RoleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

role = RoleSchema()
