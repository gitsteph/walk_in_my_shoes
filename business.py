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


# TODO: eventually move to `seed.py`
class CSVParser():
	# csv_category is either biographies or situationcards
	@classmethod
	def read_csv(cls, csv_category):
		if csv_category == "biographies":
			fieldnames = (
				"age",
				"city",
				"state",
				"days_pregnant",
				"abridged_text",
				"full_text",
				"image_id",
			)
		else:
			fieldnames = (
				"category",
				"day_impact",
				"money_impact",
				"option_text",
				"full_text",
				"image_id",
				"next_category_0",
				"next_category_1",
			)

		with open('./seed_files/biographies.csv', 'rb') as csvfile:
			biography_rows = csv.DictReader(
				csvfile,
				fieldnames=fieldnames,
				delimiter=','
			)
			for row in biography_rows:
				print row["age"]
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
				else:
					pass

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
