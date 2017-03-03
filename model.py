from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


class State(db.Model):
    """US States"""
    __tablename__ = "states"

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    abbrev = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return "<State id=%s, State Name=%s, State Abbrev=%s>" % (self.id, self.name, self.abbrev)


################################################################################################
def connect_to_db(app):
    """Connect to database."""

    app.secret_key = '###'  # TODO: Change this later, hook in secrets
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///aah'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    # this creates all the tables in this file
    # (need to drop and recreate if table already exists and schema was changed)
    db.create_all() 


################################################################################################
if __name__ == "__main__":
    # If module is run interactively, user will be able to work with db directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
