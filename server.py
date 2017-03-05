from flask import Flask, render_template, request
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
    return render_template("homepage.html", placeholder_text=placeholder_text, image_location=image.location)


@app.route('/start', methods=['GET'])
def start_new_game():
    """
    Start a new game.
    Pull random bio from database, create player record, and pass bio information to template.
    """
    choice = request.args.get('choice')

    if not choice:
        days = 3 * 7
        category = 'Start'
        card_text = "Hello and welcome to Walk in my Shoes!"
        next_card_id = "a_bio"

        choices = [
            {
                'value': 'start',
                'text': 'Begin'
            }
        ]

    else:
        # Should have chosen option and weeks pregnant
        current_card_id = request.args.get('current')
        next_card_id = choice
        days = request.args.get('days')
        try:
            days = int(days)
        except (ValueError, TypeError) as e:
            days = 12 * 7

        days += 3

        choices = [
            {
                'value': 'choice_1',
                'text': 'A Choice'
            },
            {
                'value': 'choice_2',
                'text': 'Another Choice'
            },
            {
                'value': 'choice_3',
                'text': 'Last Choice'
            }
        ]

        category = 'Category'
        card_text = "You chose {choice} and are {days} days pregnant".format(choice=choice, days=days)

    image = db.session.query(Image).filter(Image.short_name == "language").first()
    args = {
        'image_location': image.location,  # placeholder image location only
        'current': next_card_id,
        'card_text': card_text,
        'category': category,
        'days': days,
        'choices': choices
    }

    # TODO: create new game instance with a randomly selected biography

    return render_template("main_game.html", **args)


#### IN PROGRESS
@app.route('/decision', methods=['POST'])
def process_decision():
    """
    AJAX route to process decision and redirect to next game state.
    Will send post request from HTML form asynchronously, process info, then reroute to next game state.
    """
    selected_choice_id = request.form.get("selected_choice_id")
    days_pregnant_int = request.form.get("current_day_int")

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
