def handle_errors(description, status_code=None, e: Exception = None):
    payload = {
        "error": e
    }

    raise ApiError(description, status_code, payload)


class ApiError(Exception):
    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)

        self.message = message
        self.payload = payload

        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message

        return rv
