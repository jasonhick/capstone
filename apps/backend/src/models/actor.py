from ..database import db

# from .movie import movie_actor_association


class Actor(db.Model):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.Date)

    # Relationship with movies
    movies = db.relationship("Movie", secondary="movie_actor", back_populates="actors")

    def __repr__(self):
        return f"<Actor {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "birthdate": self.birthdate.isoformat() if self.birthdate else None,
            "movies": [movie.serialize_brief() for movie in self.movies],
        }

    def serialize_brief(self):
        """Serialize without relationships to avoid recursion"""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
        }

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            db.session.rollback()
            raise

    def update(self):
        try:
            db.session.commit()
            return self
        except:
            db.session.rollback()
            raise

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise
