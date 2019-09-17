import os

PASSWORD_SALT = os.environ.get("PASSWORD_SALT")
if PASSWORD_SALT is None:
    print("Environment Variable PASSWORD_SALT not set!")
    exit(1)
