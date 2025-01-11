from backend.src.database import db

# from .movie import movie_actor_association


class Actor(db.Model):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.Date)

    # Relationship with movies
    movies = db.relationship("Movie", secondary="movie_actor", back_populates="actors")
