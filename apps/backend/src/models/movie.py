from backend.src.database import db

# Create the association table
movie_actor = db.Table(
    "movie_actor",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column("actor_id", db.Integer, db.ForeignKey("actors.id"), primary_key=True),
)


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    # Relationship with actors
    actors = db.relationship("Actor", secondary="movie_actor", back_populates="movies")
