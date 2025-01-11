from backend.src.database import db

# movie_actor_association = db.Table(
#     "movie_actor",
#     db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
#     db.Column("actor_id", db.Integer, db.ForeignKey("actors.id"), primary_key=True),
# )


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date)

    # actors = db.relationship(
    #     "Actor", secondary=movie_actor_association, back_populates="movies"
    # )
