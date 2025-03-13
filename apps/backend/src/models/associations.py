from ..database import db

# Association table for Movie and Actor relationship
movie_actor = db.Table(
    "movie_actor",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column("actor_id", db.Integer, db.ForeignKey("actors.id"), primary_key=True),
)

# Add other association tables here as needed
