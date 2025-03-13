from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from .common import get_logger

# Get logger
logger = get_logger()

# Configure naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()


class DBTransaction:
    """Context manager for database transactions"""

    def __init__(self, session=None, message=None):
        self.session = session or db.session
        self.message = message

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
            logger.error(f"Transaction failed: {exc_val}")
            return False
        else:
            try:
                self.session.commit()
                if self.message:
                    logger.info(f"Transaction successful: {self.message}")
                return True
            except Exception as e:
                self.session.rollback()
                logger.error(f"Failed to commit transaction: {str(e)}")
                raise


def init_db(app):
    # Import models here to ensure they're registered with SQLAlchemy
    from .models import actor, movie

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
