from cards_pool_module import CardsPool
from tavern_module import Tavern
from fight_module import Fight
from events_system_module import EventManager
import random

class Game:
    def __init__(self, players_number=2):
        self.event_manager = EventManager()
        self.players_number = players_number
        self.cards_pool = CardsPool()
        self.players_taverns = []
        self.turn_number = 1  # Added to keep track of turns

    def create_players_taverns(self, player_names=None):
        if player_names:
            players_names = player_names
        else:
            players_names = [f"Player{i+1}" for i in range(self.players_number)]
        self.players_taverns = [Tavern(self, player_name=name) for name in players_names]
        return self.players_taverns

    def card_draw(self):
        return self.cards_pool.card_draw()

    def card_return_to_pool(self, card):
        self.cards_pool.card_return_to_pool(card)

    def play_round(self):
        round_log = []
        for player in self.players_taverns:
            player.player_turn()
        fighting_list = list(self.players_taverns)
        while len(fighting_list) > 1:
            fighter1, fighter2 = random.sample(fighting_list, 2)
            fighting_list.remove(fighter1)
            fighting_list.remove(fighter2)
            fight = Fight(fighter1, fighter2)
            player_won, damage_dealt, fight_result = fight.simulate()
            round_log.append(fight_result)
            if player_won == -1:
                pass
            elif player_won == 0:
                fighter2.player_hp -= damage_dealt
            elif player_won == 1:
                fighter1.player_hp -= damage_dealt
            else:
                pass
        self.players_taverns = [player for player in self.players_taverns if player.player_hp > 0]
        self.turn_number += 1
        return round_log

    def declare_winner(self):
        if self.players_taverns:
            winner = self.players_taverns[0].player_name
            return winner
        return None

    def play_game(self, player_names=None):
        self.create_players_taverns(player_names)
        game_log = []
        while len(self.players_taverns) > 1:
            round_log = self.play_round()
            game_log.append(round_log)
        winner = self.declare_winner()
        return winner, game_log

    def reset(self):
        self.cards_pool = CardsPool()
        self.event_manager = EventManager()
        self.players_taverns = []
        self.turn_number = 1
