from flask import Flask, render_template, request
from model import connect_to_db, db, State

app = Flask(__name__)


# general card sequence:
# start -> language -> provider -> payment ->
# transportation -> childcare -> confidentiality -> time off -> health -> final
# (resource agency optional)


# IN PROGRESS
# @app.route('/decision', methods=['POST'])
# def process_decision():
# 	"""AJAX route to process decision and redirect to next game state"""
# 	selected_choice_id = request.form.get("selected_choice_id")
# 	days_pregnant_int = request.form.get("current_day_int")

# 	# hard-coding this value in for now until we have a seeded database
# 	day_diff_int = 4  # add four days
# 	days_pregnant_int += day_diff_int


@app.route('/', methods=['GET'])
def render_homepage():
	"""
	Homepage, before the player starts the game.
	Frontend will have some button to trigger `/start`.
	"""
	placeholder_text = "PLACEHOLDER HERE"
	return render_template("test.html", color_or_state=placeholder_text)


@app.route('/start', methods=['POST'])
def start_new_game():
	"""
	Start a new game.
	Pull random bio from database, create player record, and pass bio information to template.
	"""
	image_location = "./static/img/nytimes_img.png"  # placeholder image location only
	return render_template("main_game.html", image_location=image_location)


@app.route('/<game_id>', methods=['POST'])
def render_next_game_state(game_id):
	print(game_id)
	image_location = "./static/img/nytimes_img.png"  # placeholder image location only
	is_final = False  # change after db is seeded
	return render_template("main_game.html", image_location=image_location, is_final=is_final)


# Below are several sample Flask routes to reference
@app.route('/test', methods=['GET'])
def print_test():
	html = "<html><body>Hello World 2</body></html>"
	return html


@app.route('/test2', methods=['GET'])
def print_test_2():
	strvar_to_insert = 'blue'
	return render_template("test.html", color_or_state=strvar_to_insert)


@app.route('/test3/<captured_arg>', methods=['GET'])
def print_captured_arg(captured_arg):
	print(captured_arg)
	return render_template("test.html", color_or_state=captured_arg)


@app.route('/sample_state', methods=['GET'])
def render_state():
	state = db.session.query(State).first()
	state_name = state.name if state else "filler state if no state in db"
	return render_template("test.html", color_or_state=state_name)


################################################################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)  # set to false before deploying
