from datetime import datetime
from functools import wraps
from hashlib import sha256

from flask import jsonify, request, g
from voluptuous.humanize import humanize_error

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


def datetime_to_str(datetime):
    """Convert a datetime object to an ISO formatted datetime string.

    Args:
        datetime (datetime)

    Returns:
        str
    """
    if datetime is None:
        return None
    else:
        return datetime.isoformat()


def str_to_date(string):
    """Convert an ISO formatted date string to a date.

    Args:
        string (str)
    """
    if string is None:
        return None
    else:
        return datetime.strptime("%Y-%m-%d").date()


def str_to_bool(string):
    """Convert a "true" or "false" string to boolean.

    Args:
        string (str): [description]

    Raises:
        ValueError: If "true" or "false" not passed. Case insensitive.

    Returns:
        bool
    """
    if string is None:
        return None

    string = string.lower()
    if string == "true":
        return True
    elif string == "false":
        return False
    else:
        raise ValueError()


# TODO: Delete
def validation_error(error, data, response_code=400):
    """Return a jsonify'd Flask response with a list of humanized error messages.

    Args:
        error (Invalid or MultipleInvalid): A voluptuous validation exception.
        data (Any): The validated data that caused the error.
        response_code (int, optional): The HTTP response code to use.
            Defaults to 400.

    Returns:
        A JSON / response code tuple.
    """
    humanized_error = humanize_error(data, error)
    return (jsonify({"messages": humanized_error.splitlines()}), response_code)


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
