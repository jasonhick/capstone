from ..database import db
from .associations import movie_actor
from .base import BaseModel


class Movie(db.Model, BaseModel):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    # Relationship with actors
    actors = db.relationship("Actor", secondary=movie_actor, back_populates="movies")

    def __repr__(self):
        return f"<Movie {self.title}>"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.isoformat(),
            "actors": [actor.serialize_brief() for actor in self.actors],
        }

    def serialize_brief(self):
        """Serialize without relationships to avoid recursion"""
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.isoformat(),
        }
