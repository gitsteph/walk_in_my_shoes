import csv

from datetime import datetime
from flask import Flask
from sqlalchemy import func #

from model import db, connect_to_db, State, SituationCard, Image, Biography, Game, GameDecision
from server import app


# TODO: Fix ipython stuff related to this file
app = Flask(__name__)
app.secret_key = "###"
connect_to_db(app)

class StaticData():
    @classmethod
    def add_new_state(cls, name, abbrev):
        new_state = State(name=name, abbrev=abbrev)
        db.session.add(new_state)
        db.session.commit()
        print("state {0} {1} added to 'states' table".format(name, abbrev))

    @classmethod
    def add_biography(cls, age, city, state, days_pregnant, abridged_text, full_text, image_id):
        new_bio = Biography(age=age,
                            city=city,
                            state=state,
                            days_pregnant=days_pregnant,
                            abridged_text=abridged_text,
                            full_text=full_text,
                            image_id=image_id)
        db.session.add(new_bio)
        db.session.commit()
        print("bio {0} added to {1} table".format(new_bio.id, Biography.__tablename__))

    @classmethod
    def add_image(cls, image_location):
        new_image = Image(location=image_location)
        db.session.add(new_image)
        db.session.commit()
        print("image {0} added to {1} table".format(new_image.id, Image.__tablename__))

    @classmethod
    def add_situation_card(cls,
                           category,
                           day_impact,
                           wait_or_extra_condition_weeks_over,
                           extra_category,
                           next_category,
                           option_text,
                           text_badge,
                           full_text,
                           image_id):
        new_situation_card = SituationCard(
            category=category,
            day_impact=day_impact,
            wait_or_extra_condition_weeks_over=wait_or_extra_condition_weeks_over,
            extra_category=extra_category,
            next_category=next_category,
            option_text=option_text,
            text_badge=text_badge,
            full_text=full_text,
            image_id=image_id,
        )
        db.session.add(new_situation_card)
        db.session.commit()
        print("situation card {0} added to {1} table".format(
            new_situation_card.id, SituationCard.__tablename__)
        )


# TODO: eventually move to `seed.py`
class CSVParser():
    # csv_category is either biographies or situationcards
    @classmethod
    def read_csv(cls, csv_category):
        seed_file = "biographies.csv" if csv_category == "biographies" else "situationcards.csv"
        with open("./seed_files/{}".format(seed_file), 'rb') as csvfile:
            rows = csv.DictReader(
                csvfile,
                delimiter=','
            )
            for row in rows:
                if csv_category == "biographies":
                    StaticData.add_biography(
                        age=row["age"],
                        city=row["city"],
                        state=row["state"],
                        days_pregnant=row["days_pregnant"],
                        abridged_text=row["abridged_text"],
                        full_text=row["full_text"],
                        image_id=int(row["image_id"])
                    )
                    print row["age"]
                else:
                    StaticData.add_situation_card(
                        category=row["category"],
                        day_impact=int(row["day_impact"]),
                        wait_or_extra_condition_weeks_over=(int(row["wait_or_extra_condition_weeks_over"])
                            if row["wait_or_extra_condition_weeks_over"] else None),
                        extra_category=row["extra_category"],
                        next_category=row["next_category"],
                        option_text=row["option_text"],
                        text_badge=row["text_badge"],
                        full_text=row["full_text"],
                        image_id=int(row["image_id"]),
                    )
                    print row["category"]

class Game():
    @classmethod
    def generate_new_game(cls):
        # select random biography
        bio_obj = db.session.query(Biography).order_by(func.random()).first()
        # create new game object and save to table
        new_game = Game(biography_id=bio_obj.id, game_started_ts=datetime.now())
        return new_game.id, bio_obj

    @classmethod
    def generate_new_game_decision(cls, game_id):
        # find last gamedecision made, go find the situationcard.next
        last_game_decision_card = db.session.query(GameDecision).filter(
            GameDecision.game_id == game_id).order_by(GameDecision.id.desc()).first()
        last_situation_card = db.session.query(SituationCard).filter(
            SituationCard.id == last_game_decision_card.situation_card_id).first()
        next_category = last_situation_card.next_category_0 or last_situation_card.next_category_1
        pass
