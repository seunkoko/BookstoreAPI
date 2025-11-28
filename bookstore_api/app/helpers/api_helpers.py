from flask import jsonify, make_response
from sqlalchemy import or_, func

from bookstore_api.app.models import Book, Author, BookCategory

def api_response(data=None, message="Success", status_code=200, **kwargs):
    """
    Creates a consistent JSON response structure for success.
    """
    response_body = {
        'status': 'success',
        'message': message,
        'data': data,
    }

    # Add any extra keyword arguments (e.g., pagination metadata)
    response_body.update(kwargs)

    # Use make_response to set the HTTP status code
    return make_response(jsonify(response_body), status_code)


def search_filter_and_sort_books(books_query, filters):
    """Apply filtering and sorting to the books query based on request args."""
    # Searching
    search_term = filters.get('search')
    if search_term:
        search_pattern = f"%{search_term.lower()}%"
        books_query = books_query.join(Author, isouter=True).join(BookCategory, isouter=True).filter(
            or_(
                func.lower(Book.title).like(search_pattern),
                func.lower(Author.name).like(search_pattern),
                func.lower(BookCategory.name).like(search_pattern)
            )
        )

    # Filtering
    author_id = filters.get('author_id')
    category_id = filters.get('category_id')
    publication_year = filters.get('publication_year')

    if author_id:
        books_query = books_query.filter(Book.author_id == author_id)
    if category_id:
        books_query = books_query.filter(Book.category_id == category_id)
    if publication_year:
        books_query = books_query.filter(Book.publication_year >= publication_year)
    # TODO: Filter by minimum rating when reviews are implemented

    # Sorting
    sort_by = filters.get('sort_by', 'title')  # Default sort by title
    sort_order = filters.get('sort_order', 'asc')  # Default ascending order

    if hasattr(Book, sort_by):
        sort_column = getattr(Book, sort_by)
        if sort_order == 'desc':
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
        books_query = books_query.order_by(sort_column)

    return books_query
