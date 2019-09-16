# from datetime import datetime, timedelta
# from functools import wraps
# from uuid import uuid4

# from flask import g, jsonify, request

# from helpers import datetime_to_str
# from models.shared import db


# class AuthToken(db.Model):
#     __tablename__ = "AuthToken"

#     id = db.Column(db.String(36), primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
#     expiry_datetime = db.Column(db.DateTime, nullable=False)
#     last_used_datetime = db.Column(db.DateTime, nullable=False)
#     created_datetime = db.Column(db.DateTime, nullable=False)

#     user = db.relationship("User")

#     def __init__(self, user_id):
#         self.user_id = user_id

#         self.id = str(uuid4())
#         self.expiry_datetime = datetime.now() + timedelta(days=30)
#         self.last_used_datetime = datetime.now()
#         self.created_datetime = datetime.now()

#     def get_data(self):
#         """Return a json.dumps compatible dictionary of AuthToken data.

#         Returns:
#             dict
#         """
#         return {
#             "token": self.id,
#             "expiry_datetime": datetime_to_str(self.expiry_datetime),
#             "last_used_datetime": datetime_to_str(self.last_used_datetime),
#             "created_datetime": datetime_to_str(self.created_datetime),
#         }

#     @classmethod
#     def authenticate(cls, token):
#         """Authenticate the validity of a token and return a user if valid.

#         Args:
#             token (str)

#         Returns:
#             User: A User object.
#         """
#         auth_token = cls.query.filter(
#             AuthToken.id == token, AuthToken.expiry_datetime > datetime.now()
#         ).first()
#         if auth_token is None:
#             return None

#         return auth_token.user

#     @classmethod
#     def required(cls, func):
#         """Require an authentication token in order to execute the decorated
#         function. Add the authenticated user to Flask's g local proxy.

#         Args:
#             func (function): The decorated function.

#         Returns:
#             If a valid token is passed the decorated function is returned,
#             else a 401 response is returned.
#         """

#         @wraps(func)
#         def wrapped_func(*args, **kwargs):
#             token_id = request.headers.get("token")
#             if token_id is None:
#                 return (
#                     jsonify({"message": "Authentication token missing."}),
#                     401,
#                 )

#             user = cls.authenticate(token_id)
#             if user is None:
#                 return (
#                     jsonify({"message": "Authentication token invalid."}),
#                     401,
#                 )

#             g.user = user

#             return func(*args, **kwargs)

#         return wrapped_func
