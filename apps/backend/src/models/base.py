from ..common import get_logger
from ..database import db

logger = get_logger()


class BaseModel:
    """Base model class with common CRUD operations"""

    def insert(self):
        """Insert this model into the database"""
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(
                f"Successfully inserted {self.__class__.__name__} with id {getattr(self, 'id', None)}"
            )
            return self
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error inserting {self.__class__.__name__}: {str(e)}")
            raise

    def update(self):
        """Update this model in the database"""
        try:
            db.session.commit()
            logger.info(
                f"Successfully updated {self.__class__.__name__} with id {getattr(self, 'id', None)}"
            )
            return self
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating {self.__class__.__name__}: {str(e)}")
            raise

    def delete(self):
        """Delete this model from the database"""
        try:
            db.session.delete(self)
            db.session.commit()
            logger.info(
                f"Successfully deleted {self.__class__.__name__} with id {getattr(self, 'id', None)}"
            )
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting {self.__class__.__name__}: {str(e)}")
            raise

    @classmethod
    def get_all(cls):
        """Get all instances of this model"""
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        """Get an instance of this model by ID"""
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id):
        """Get an instance of this model by ID or raise 404"""
        return cls.query.get_or_404(id)
