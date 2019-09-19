from functools import wraps
from hashlib import sha256

from flask import g, jsonify, request

import language as lang


def hash_password(value, salt):
    """Return a sha256 hash of the declared value and salt.

    Args:
        value (str)
        salt (str)

    Returns:
        str
    """
    hashed_value = sha256((value + salt).encode()).hexdigest()
    return hashed_value


def json_required(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        if request.method in ["POST", "PATCH"]:
            g.parsed_json = request.get_json(silent=True)
            if g.parsed_json is None:
                return api_message(lang.no_json_content, 400)
        return func(*args, **kwargs)

    return wrapped_func


def api_message(message, response_code):
    """Return the message as a jsonify'd Flask response with the declared
    response code.

    Args:
        messages (str): The message(s) to be returned.
        response_code (int): The HTTP response code to use.
    """
    return jsonify({"message": message}), response_code


def setattrs(obj, attrs):
    for key, value in attrs.items():
        setattr(obj, key, value)
    return obj
