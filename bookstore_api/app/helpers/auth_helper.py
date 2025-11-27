import os
import re
from datetime import timedelta
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

ACCESS_EXPIRES = timedelta(hours=1)

def revoke_token(redis_db, jti: str):
    redis_db.setex(jti, os.getenv('JWT_ACCESS_TOKEN_EXPIRES', ACCESS_EXPIRES), 'true')
    return jsonify({"message": "Access token revoked"}), 200


def is_valid_email_format(email):
    """
    Validates the format of an email address using a regular expression.
    """
    # A standard, reasonably comprehensive regex pattern for email validation
    email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return email_regex.fullmatch(email) is not None

def is_strong_password(password):
    """
    Validates password strength using a regular expression with lookaheads.
    Enforces:
    - Minimum 8 characters total.
    - At least one uppercase letter.
    - At least one lowercase letter.
    - At least one digit.
    - At least one special character (from !@#$%^&*).
    """
    # Lookahead assertions:
    # (?=.*[A-Z]) - Must contain at least one uppercase letter
    # (?=.*[a-z]) - Must contain at least one lowercase letter
    # (?=.*\d)    - Must contain at least one digit
    # (?=.*[!@#$%^&*]) - Must contain at least one special character
    # .{8,}       - Must be 8 characters or more

    strong_password_regex = re.compile(
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$"
    )
    return strong_password_regex.fullmatch(password) is not None
