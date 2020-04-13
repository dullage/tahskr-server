import secrets

from components.system.model import System

CURRENT_SCHEMA_VERSION = "1"


def init(db, app):
    db.init_app(app)
    with app.app_context():
        # Initialise Database
        db.create_all()
        db.session.commit()

        # Initialise Password Salt
        password_salt_key = "password_salt"
        if System.get(password_salt_key) is None:
            System(
                {"key": password_salt_key, "value": secrets.token_urlsafe(32)}
            )

        # Schema Version
        schema_version_key = "schema_version"
        db_schema_version = System.get(schema_version_key)
        if db_schema_version is None:
            System(
                {"key": schema_version_key, "value": CURRENT_SCHEMA_VERSION}
            )
