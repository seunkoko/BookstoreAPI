from marshmallow import fields, validate

from bookstore_api.app.extensions import ma


class BookSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Title must be at least 1 character long.")
    )
    description = fields.String()
    isbn = fields.String(
        required=True,
        validate=validate.Length(equal=13, error="ISBN must be exactly 13 characters long.")
    )
    cover_image_url = fields.String(load_only=True)
    cover_image_s3_key = fields.String(load_only=True)
    publication_year = fields.Integer()
    author = fields.Nested('AuthorSchema', only=['name'])
    category = fields.Nested('BookCategorySchema', only=['name'])
    reviews = fields.Nested('ReviewSchema', many=True, exclude=['book'])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

book = BookSchema()
books = BookSchema(many=True)
