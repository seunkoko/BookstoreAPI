from marshmallow import fields, validate

from bookstore_api.app.extensions import ma


class BookSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Title must be at least 1 character long.")
    )
    description = fields.String()
    author = fields.Nested('AuthorSchema', only=['name'])
    reviews = fields.Nested('ReviewSchema', many=True, exclude=['book'])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

book = BookSchema()
books = BookSchema(many=True)
