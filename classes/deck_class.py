import csv
import random

from classes.card_class import MinionCard


class Deck:

    def __init__(self, minions_information_file_path='minions_information.csv'):
        self.cards_pool = []

        self.fill_up(minions_information_file_path=minions_information_file_path)

    def __repr__(self):
        return f'Class: {self.__class__.__name__}, cards amount: {self.cards_amount()}'

    def fill_up(self, minions_information_file_path):
        with open(file=minions_information_file_path, newline='') as csv_file:
            minions = csv.reader(csv_file, delimiter=',')
            for minion in minions:
                for i in range(int(minion[6])):
                    self.cards_pool.append(MinionCard(name=minion[0], attack=int(minion[1]), health=int(minion[2]),
                                                      minion_type=minion[3], tavern_tier=int(minion[4]),
                                                      provoke=minion[5]))

    def cards_amount(self):
        return len(self.cards_pool)

    def draw_card(self, players_tavern_tier):
        for i in range(10000):
            random_card_position = random.randint(0, self.cards_amount() - 1)
            random_card = self.cards_pool[random_card_position]
            if random_card.tavern_tier <= players_tavern_tier:
                return self.cards_pool.pop(random_card_position)
