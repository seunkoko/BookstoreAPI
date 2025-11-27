from marshmallow import fields, validate

from bookstore_api.app.extensions import ma


class AuthorSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=2, error="Author name must be at least 2 characters long.")
    )
    bio = fields.String()
    books = fields.Nested('BookSchema', many=True, exclude=['author'])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

author = AuthorSchema()
authors = AuthorSchema(many=True)
