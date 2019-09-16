# import os
# from datetime import datetime

# from helpers import hash_password
# from models import AuthToken
# from models.shared import db

# PASSWORD_SALT = os.environ.get("PASSWORD_SALT")
# if PASSWORD_SALT is None:
#     print("Environment Variable PASSWORD_SALT not set!")
#     exit(1)


# class User(db.Model):
#     __tablename__ = "User"

#     id = db.Column(db.Integer, primary_key=True)
#     email_address = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     failed_login_attempts = db.Column(db.Integer, nullable=False)
#     locked = db.Column(db.Boolean, nullable=False)
#     created_datetime = db.Column(db.DateTime, nullable=False)

#     def __init__(self, email_address, password):
#         self.email_address = email_address.lower()
#         self.password = hash_password(password, PASSWORD_SALT)

#         self.failed_login_attempts = 0
#         self.locked = False
#         self.created_datetime = datetime.now()

#     @classmethod
#     def get_token(cls, email_address, password):
#         """Check the declared email address and password and return an
#         AuthToken if valid.

#         Args:
#             email_address (str)
#             password (str)

#         Returns:
#             AuthToken
#         """
#         user = cls.query.filter_by(email_address=email_address.lower()).first()

#         if user is None:
#             return None
#         if user.locked is True:
#             return None  # TODO
#         if hash_password(password, PASSWORD_SALT) != user.password:
#             user.failed_login_attempts += 1
#             if user.failed_login_attempts >= 3:
#                 user.locked = True
#             db.session.commit()
#             return None
#         else:
#             token = AuthToken(user.id)
#             db.session.add(token)
#             db.session.commit()
#             return token
