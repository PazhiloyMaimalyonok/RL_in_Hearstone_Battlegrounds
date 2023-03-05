import csv
import random
from typing import List

from classes.card_class import MinionCard


class Deck:
    cards_pool: List[MinionCard] = []

    def fill_up(self, minions_information_file_path='minions_information.csv'):
        with open(file=minions_information_file_path, newline='') as csv_file:
            minions = csv.reader(csv_file, delimiter=',')
            for minion in minions:
                for i in range(int(minion[5])):
                    self.cards_pool.append(MinionCard(name=minion[0], attack=minion[1], health=minion[2],
                                                      minion_type=minion[3], tavern_tier=minion[4]))

    def cards_amount(self):
        return len(self.cards_pool)

    def __repr__(self):
        return (f'Class: {self.__class__.__name__}\n'
                f'Cards amount: {self.cards_amount()}')

    def draw_card(self, players_tavern_tier):
        for i in range(10000):
            random_card_position = random.randint(0, self.cards_amount() - 1)
            random_card = self.cards_pool[random_card_position]
            if random_card.tavern_tier <= players_tavern_tier:
                return random_card
