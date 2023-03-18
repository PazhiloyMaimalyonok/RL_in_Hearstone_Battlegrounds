import random
from typing import List

from classes.deck_class import Deck
from classes.fight_class import Fight
from classes.player_class import Player
from classes.tavern_class import Tavern


class Game:
    max_turn_number = 100

    def __init__(self, players: List[Player], deck: Deck):
        self.players = players
        self.turn_number = 1
        self.deck = deck

    @property
    def alive_players(self) -> List[Player]:
        return [player for player in self.players if player.health > 0]

    @property
    def dead_players(self) -> List[Player]:
        return [player for player in self.players if player.health <= 0]

    def return_fighting_list(self) -> List[Player]:
        if len(self.alive_players) % 2 == 0:
            return self.alive_players
        else:
            return self.alive_players + [random.choice(self.dead_players)]

    def make_tavern_turn(self, player: Player):
        tavern = Tavern(player=player, deck=self.deck, turn_number=self.turn_number)
        print(f'Player: {player.name} turn')
        while True:
            print(f'Print action number: \n'
                  f'1 - buy a minion, \n'
                  f'2 - play a card, \n'
                  f'3 - sell a minion, \n'
                  f'4 - reroll, \n'
                  f'5 - show stats, \n'
                  f'6 - end the turn')
            action_number = int(input())
            action_dictionary = {1: 'Buy minion', 2: 'Play card', 3: 'Sell minion', 4: 'Reroll', 5: 'Stats'}
            if action_number in action_dictionary:
                tavern.player_turn(action=action_dictionary[action_number])
            elif action_number == 6:
                tavern.clear_board()
                break
            else:
                print('Wrong input')

    def do_tavern_cycle(self):
        for player in self.alive_players:
            self.make_tavern_turn(player=player)

    def do_fighting_cycle(self):
        fighting_spisok = self.return_fighting_list()
        print('Fighting cycle begins')
        for i in range(len(fighting_spisok) // 2):
            fighter1, fighter2 = random.sample(fighting_spisok, 2)
            fighting_spisok.remove(fighter1)
            fighting_spisok.remove(fighter2)
            fight = Fight(first_player=fighter1, second_player=fighter2)
            fight.simulate()

    def play_game(self):
        for i in range(self.max_turn_number):
            if len(self.alive_players) < 2:
                break
            self.do_tavern_cycle()
            self.do_fighting_cycle()

            self.turn_number += 1
