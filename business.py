import csv

from datetime import datetime
from flask import Flask
from sqlalchemy import func #

from model import (
    db,
    connect_to_db,
    State,
    SituationCard,
    Image,
    Biography,
    Game,
    GameDecision,
    WHSClinic,
)


class NewGame():
    @classmethod
    def generate_new_game(cls):
        # select random biography
        bio_obj = db.session.query(Biography).order_by(func.random()).first()
        # create new game object and save to table
        new_game = Game(biography_id=bio_obj.id, game_started_ts=datetime.now())
        db.session.add(new_game)
        db.session.commit()
        print("{0} id created w/ {1} bio_id".format(new_game.id, bio_obj.id))
        return new_game.id, bio_obj

#### TODO: NEED TO FINISH TEST BELOW
    @classmethod
    def generate_new_game_decision(cls, game_id, last_situation_card_id=None):
        # TODO: switch out to go using only game_id (partial implementation below, scrapped b/c time)
        # find last gamedecision made, go find the situationcard.next
        # last_game_decision_card = db.session.query(GameDecision).filter(
        #     GameDecision.game_id == game_id).order_by(GameDecision.id.desc()).first()
        # last_situation_card = db.session.query(SituationCard).filter(
        #     SituationCard.id == last_game_decision_card.situation_card_id).first()
        # next_category = last_situation_card.next_category_0 or last_situation_card.next_category_1
        
        if last_situation_card_id:
            last_situation_card = SituationCard.query.get(last_situation_card_id)
            next_category = last_situation_card.next_category
            is_end = True
        else:
            # if last card was biography
            is_end = False
            next_category = "language"
        print("next category: {}".format(next_category))

        # TODO: handle extra category part!!!!! #### V IMPORTANT (make sure in pass 2)
        situationcard_objs_list = db.session.query(SituationCard).filter(
            SituationCard.category == next_category).order_by(func.random()
        ).limit(3)
        # will log 3 situationcard-options the user is presented next, as well as what is displayed
        # (unless start card was displayed, then just the options logged for now)
        # TODO: fix to log better^

        choice_ids_str = str([situation_card.id for situation_card in situationcard_objs_list])

        new_game_decision = GameDecision(
            game_id=game_id,
            situation_card_id=last_situation_card_id,
            choice_ids = choice_ids_str,
            is_end=is_end,
        )
        db.session.add(new_game_decision)
        db.session.commit()
        return new_game_decision, situationcard_objs_list
