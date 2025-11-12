from marshmallow import fields

from bookstore_api.app.extensions import ma


class ReviewSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    rating = fields.Integer(required=True)
    comment = fields.String()
    book = fields.Nested('BookSchema', only=['title'])
    user = fields.Nested('UserSchema', only=['username'])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

author = ReviewSchema()
authors = ReviewSchema(many=True)
