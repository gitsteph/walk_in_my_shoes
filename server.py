from flask import Flask, render_template, request
from model import connect_to_db, db, State

app = Flask(__name__)


# general card sequence:
# start -> language -> provider -> payment ->
# transportation -> childcare -> confidentiality -> time off -> health -> final
# (resource agency optional)

@app.route('/', methods=['GET'])
def render_homepage():
	placeholder_text = "PLACEHOLDER HERE"
	return render_template("test.html", color_or_state=placeholder_text)


@app.route('/start', methods=['POST'])
def start_new_game():
	image_location = "./static/img/nytimes_img.png"  # placeholder image location only
	return render_template("main_game.html", image_location=image_location)


@app.route('/<game_id>', methods=['GET'])
def render_next_game_state(game_id):
	print(game_id)
	image_location = "./static/img/nytimes_img.png"  # placeholder image location only
	is_final = False  # change after db is seeded
	return render_template("main_game.html", image_location=image_location, is_final=is_final)


@app.route('/sample_state', methods=['GET'])
def render_state():
	state = db.session.query(State).first()
	state_name = state.name if state else "filler state if no state in db"
	return render_template("test.html", color_or_state=state_name)


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

################################################################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)  # set to false before deploying
