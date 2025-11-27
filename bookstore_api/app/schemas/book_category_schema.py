from marshmallow import fields, validate

from bookstore_api.app.extensions import ma


class BookCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=2, error="Name must be greater than 2 characters.")
    )
    description = fields.String()
    books = fields.Nested('BookSchema', many=True, exclude=['category'])
