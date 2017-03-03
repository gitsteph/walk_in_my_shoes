from flask import Flask
from model import db, connect_to_db, State
from server import app

# TODO: Fix ipython stuff related to this file
app = Flask(__name__)
app.secret_key = "###"
connect_to_db(app)


def add_new_state(name, abbrev):
	new_state = State(name=name, abbrev=abbrev)
	db.session.add(new_state)
	db.session.commit()
	print("state {0} {1} added to 'states' table".format(name, abbrev))
