from marshmallow import fields, validate

from bookstore_api.app.extensions import ma


class ReviewSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    rating = fields.Integer(
        required=True,
        validate=validate.Range(min=1, max=5, error="Rating must be between 1 and 5.")
    )
    comment = fields.String(allow_none=True)
    book = fields.Nested('BookSchema', only=['title'])
    user = fields.Nested('UserSchema', only=['username'])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

author = ReviewSchema()
authors = ReviewSchema(many=True)
