from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
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


class SituationCard(db.Model):
    __tablename__ = "situationcards"

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    category = db.Column(db.String, nullable=False)
    day_impact = db.Column(db.Integer, nullable=True)
    wait_or_extra_condition_weeks_over = db.Column(db.String, nullable=True)  # to handle weird data for now, should fix later
    # money_impact = db.Column(db.Integer, nullable=True)
    extra_category = db.Column(db.String, default=None)  # if there are prereq categories, e.g. resource agency
    next_category = db.Column(db.String)
    option_text = db.Column(db.String, nullable=False)
    text_badge = db.Column(db.String)
    full_text = db.Column(db.String, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))

    image = relationship("Image", foreign_keys=[image_id])
    # gamedecisions = db.relationship("GameDecision", backref="situationcard")

    def __repr__(self):
        return "<id=%s, category=%s, day_impact=%s, next_category=%s>" % (
            self.id, self.category, self.day_impact, self.next_category
        )


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    short_name = db.Column(db.String)
    location = db.Column(db.String, nullable=False)

    # situationcards = db.relationship("Image", backref="situationcard")
    # biographies = db.relationship("Image", backref="situationcard")

    def __repr__(self):
        return "<id=%s, location=%s>" % (self.id, self.location)


class Biography(db.Model):
    __tablename__ = "biographies"

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String)
    state = db.Column(db.String)
    days_pregnant = db.Column(db.Integer)
    abridged_text = db.Column(db.String)
    full_text = db.Column(db.String, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))

    image = relationship("Image", foreign_keys=[image_id])

    def __repr__(self):
        return "<id=%s, days_pregnant=%s>" % (self.id, self.days_pregnant)


class WHSClinic(db.Model):
    __tablename__ = "clinics"

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    max_weeks_limit = db.Column(db.Integer, nullable=False)


class Game(db.Model):
    """For each game played"""
    __tablename__ = "games"

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    biography_id = db.Column(db.Integer, db.ForeignKey("biographies.id"))
    game_started_ts = db.Column(db.DateTime, nullable=False)

    biography = relationship("Biography", foreign_keys=[biography_id])
    # gamedecisions = db.relationship("GameDecision", backref="game")

    def __repr__(self):
        return "<id=%s, biography_id=%s>" % (self.id, self.biography_id)


class GameDecision(db.Model):
    """For full playthrough sequence"""
    __tablename__ = "gamedecisions"

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    situation_card_id = db.Column(db.Integer, db.ForeignKey("situationcards.id"))
    # choice_ids are the choices that the user is asked to select from
    # once the user selects a card, that will eventually lead into the next game decision
    # (the selected choice_id becomes situation_card_id)
    choice_ids = db.Column(db.String)
    is_end = db.Column(db.Boolean, default=False)

    game = relationship("Game", foreign_keys=[game_id])
    situation_card = relationship("SituationCard", foreign_keys=[situation_card_id])

    def __repr__(self):
        return "<id=%s, game_id=%s, situation_card_id=%s, choice_1_id=%s, choice_2_id=%s, choice_3_id=%s>" % (
            self.id, self.biography_id
        )

# TODO: add player survey reaction at the end
# TODO: fix backrefs?

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
