from flask import Flask, redirect, render_template, Response, request
from flask_cors import CORS, cross_origin
import json

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

    response_payload = {
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
    # return render_template("main_game.html", **args)
    return Response(json.dumps(response_payload),
                    mimetype='application/json',
                    headers={'Cache-Control': 'no-cache'})


@app.route('/decision', methods=['POST'])
def process_decision():
    """
    AJAX route to process decision and redirect to next game state.
    Will send post request from HTML form asynchronously, process info, then reroute to next game state.
    """
    game_id = request.form.get("game_id")
    selected_choice_id = int(request.form.get("choice_id"))
    days_pregnant_int = int(request.form.get("bio_days_pregnant"))
    last_category = request.form.get("current_category")

    # last_situation_card_id is the one that was selected to be processed... will return that card's
    # content to be rendered along with next choices
    new_situationcard_to_render = SituationCard.query.get(selected_choice_id)
    next_category = new_situationcard_to_render.next_category
    game_decision_obj, situationcard_objs_list = NewGame.generate_new_game_decision(
        game_id=game_id, last_situation_card_id=selected_choice_id
    )
    days_pregnant_int += int(new_situationcard_to_render.day_impact)

    response_payload = {
        "game_id": game_id,
        "current_category": next_category,
        "bio_days_pregnant": days_pregnant_int,
        "image_location": new_situationcard_to_render.image.location,
        "next_path": "decision",
        "game_decision_id": game_decision_obj.id,
        "choice1_option_text": situationcard_objs_list[0].option_text,
        "choice1_id": situationcard_objs_list[0].id,
        "choice2_option_text": situationcard_objs_list[1].option_text,
        "choice2_id": situationcard_objs_list[1].id,
        "choice3_option_text": situationcard_objs_list[2].option_text,
        "choice3_id": situationcard_objs_list[2].id,
    }
    print(args)
    # return redirect("/{0}/{1}".format(game_id, game_decision_obj.id))
    return Response(json.dumps(response_payload),
                    mimetype='application/json',
                    headers={'Cache-Control': 'no-cache'})


#### BELOW NOT USED WITH REACT FRONTEND
@app.route('/<game_id>/<game_decision_id>', methods=['GET'])
def render_next_game_state(game_id, game_decision_id):
    """
    Renders template with image location, player info, and gamedecision object to use.
    Also passes up situationcard data.
    Detect if you have reached the final card.
    """
    gamedecision_obj = GameDecision.query.get(game_decision_id)
    situationcard_to_render = gamedecision_obj.situation_card
    next_category = situationcard_to_render.next_category
    situationcards = SituationCard.query.filter(
        SituationCard.id.in_(
            (
                gamedecision_obj.choice_id_1,
                gamedecision_obj.choice_id_2,
                gamedecision_obj.choice_id_3,
            )
        )
    )
    print("sit cards {}".format(len(list(situationcards))))
    print(situationcards)
    for c in situationcards:
        print c.category

    try:
        image_obj = db.session.query(Image).filter(Image.short_name == situationcard_to_render.category).first()
    except:
        image_obj = db.session.query(Image).filter(Image.short_name == "data_diagram").first()

    image_location = image_obj.location
    args = {
        "game_id": game_id,
        "current_category": situationcard_to_render.category,
        "bio_days_pregnant": gamedecision_obj.current_days_pregnant,
        "image_location": image_location,
        "full_text": situationcard_to_render.full_text,
        "next_path": "decision",
        "game_decision_id": gamedecision_obj.id,
        "is_final": gamedecision_obj.is_end,
    }
    for index in xrange(len(list(situationcards))):
        args["choice{}_option_text".format(index)] = situationcards[index].option_text
    print(args)
    print(game_id)
    print(game_decision_id)
    # image location doesn't send through here to render... why?
    return render_template("main_game.html", **args)


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
