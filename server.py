from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

from business import NewGame
from model import (
    connect_to_db,
    db,
    State,
    SituationCard,
    Image,
    Biography,
    Game,
    GameDecision,
    WHSClinic,
)

app = Flask(__name__)
CORS(app)


# general card sequence:
# start -> language -> provider -> payment ->
# transportation -> childcare -> confidentiality -> time off -> health -> final
# (resource agency optional)


@app.route('/', methods=['GET'])
def render_homepage():
    """
    Homepage, before the player starts the game.
    Frontend will have some button to trigger `/start`.
    """
    placeholder_text = "PLACEHOLDER LANGUAGE IMAGE BELOW!"
    image = db.session.query(Image).filter(Image.short_name == "language").first() # maybe have an image for the bio/start one?
    return render_template(
        "homepage.html", placeholder_text=placeholder_text, image_location=image.location, next_path="start")


@app.route('/start', methods=['POST'])
def start_new_game():
    """
    Start a new game.
    Pull random bio from database, create player record, and pass bio information to template.
    """
    new_game_id, biography_obj = NewGame.generate_new_game()
    image = db.session.query(Image).filter(Image.short_name == "language").first() # maybe have an image for the bio/start one?
    print(biography_obj.image.location)
    first_situationcard_category = "language"  # probably can remove this

    game_decision_obj, situationcard_objs_list = NewGame.generate_new_game_decision(new_game_id)

    args = {
        "game_id": new_game_id,
        "current_category": "start",
        "bio_age": biography_obj.age,
        "bio_city": biography_obj.city,
        "bio_state": biography_obj.state,
        "bio_days_pregnant": biography_obj.days_pregnant,
        "bio_abridged_text": biography_obj.abridged_text,
        "bio_full_text": biography_obj.full_text,
        "image_location": biography_obj.image.location,
        "next_path": "decision",
        "game_decision_id": game_decision_obj.id,
        "choice1_option_text": situationcard_objs_list[0].option_text,
        "choice1_id": situationcard_objs_list[0].id,
        "choice2_option_text": situationcard_objs_list[1].option_text,
        "choice2_id": situationcard_objs_list[1].id,
        "choice3_option_text": situationcard_objs_list[2].option_text,
        "choice3_id": situationcard_objs_list[2].id,
    }
    return render_template("main_game.html", **args)


#### IN PROGRESS
@app.route('/decision', methods=['POST'])
def process_decision():
    """
    AJAX route to process decision and redirect to next game state.
    Will send post request from HTML form asynchronously, process info, then reroute to next game state.
    """
    selected_choice_id = request.form.get("choice_id")
    days_pregnant_int = request.form.get("days")

    # TODO: create new gamedecision instance and store to db, return gamedecision.id
    # hard-coding this value in for now until we have a seeded database

    day_diff_int = 4  # add four days
    days_pregnant_int += day_diff_int

    game_id = 4  # placeholder value
    game_decision_id = 10  # placeholder value
    return redirect("/{0}/{1}".format(game_id, game_decision_id))


@app.route('/<game_id>/<game_decision_id>', methods=['GET'])
def render_next_game_state(game_id, game_decision_id):
    """
    Renders template with image location, player info, and gamedecision object to use.
    Also passes up situationcard data.
    Detect if you have reached the final card.
    """

    # TODO: eventually change this so that you only need the game_id,
    # and it navigates you to the last situation_card you were on
    print(game_id)
    print(game_decision_id)
    image_location = "./static/img/nytimes_img.png"  # placeholder image location only
    is_final = False  # change after db is seeded
    return render_template("main_game.html", image_location=image_location, is_final=is_final)


# Below are several sample Flask routes to reference
# @app.route('/test', methods=['GET'])
# def print_test():
#     html = "<html><body>Hello World 2</body></html>"
#     return html


# @app.route('/test2', methods=['GET'])
# def print_test_2():
#     strvar_to_insert = 'blue'
#     return render_template("test.html", color_or_state=strvar_to_insert)


# @app.route('/test3/<captured_arg>', methods=['GET'])
# def print_captured_arg(captured_arg):
#     print(captured_arg)
#     return render_template("test.html", color_or_state=captured_arg)


# @app.route('/sample_state', methods=['GET'])
# def render_state():
#     state = db.session.query(State).first()
#     state_name = state.name if state else "filler state if no state in db"
#     return render_template("test.html", color_or_state=state_name)


################################################################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)  # set to false before deploying
