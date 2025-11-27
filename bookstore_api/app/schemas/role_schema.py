from marshmallow import fields, validate

from bookstore_api.app.extensions import ma


class RoleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, error="Role name must be at least 2 chars long."))

role = RoleSchema()
