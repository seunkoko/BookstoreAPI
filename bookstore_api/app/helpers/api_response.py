from flask import jsonify, make_response

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
