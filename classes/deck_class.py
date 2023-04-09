import csv
import random

from classes.card_class import MinionCard


class Deck:

    def __init__(self):
        self.cards_pool = []
        self.cards_dik = {'Wrath_Weaver' : {'name': 'Wrath_Weaver', 'attack': 1, 'health': 3, 'minion_type': 'neutral', 'tavern_tier': 1, 'provoke': False, 'amount': 3}\
                    , 'Tavern_Tipper' : {'name': 'Tavern_Tipper', 'attack': 2, 'health': 2, 'minion_type': 'neutral', 'tavern_tier': 1, 'provoke': False, 'amount': 1}\
                    , 'Bomber' : {'name': 'Bomber', 'attack': 10, 'health': 10, 'minion_type': 'neutral', 'tavern_tier': 1, 'provoke': False, 'amount': 1}}

        self.fill_up()

    def __repr__(self):
        return f'Class: {self.__class__.__name__}, cards amount: {self.cards_amount()}'

    def fill_up(self):
        for minion in self.cards_dik:
            for i in range(int(self.cards_dik[minion]['amount'])):
                self.cards_pool.append(MinionCard(name=self.cards_dik[minion]['name'], attack=int(self.cards_dik[minion]['attack']), health=int(self.cards_dik[minion]['health']),
                                                      minion_type=self.cards_dik[minion]['minion_type'], tavern_tier=int(self.cards_dik[minion]['tavern_tier']),
                                                      provoke=self.cards_dik[minion]['provoke']))

    def cards_amount(self):
        return len(self.cards_pool)

    def draw_card(self, players_tavern_tier):
        while True:
            random_card_position = random.randint(0, self.cards_amount() - 1)
            random_card = self.cards_pool[random_card_position]
            if random_card.tavern_tier <= players_tavern_tier:
                return self.cards_pool.pop(random_card_position)
