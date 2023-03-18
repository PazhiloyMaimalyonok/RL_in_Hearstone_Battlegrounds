import uuid
from pprint import pprint


class Player:
    def __init__(self, name=str(uuid.uuid4()), health=40, tavern_tier=1, board=list(), hand=list()):
        self.name = name
        self.health = health
        self.tavern_tier = tavern_tier
        self.board = board
        self.hand = hand
        self.frozen_minions = []

    def __repr__(self):
        return f'Class: {self.__class__.__name__}, name: {self.name}, health: {self.health}, ' \
               f'tavern_tier: {self.tavern_tier}'

    def hand_information(self):
        print("Player's hand:")
        pprint(self.hand)

    def board_information(self):
        print("Player's board:")
        pprint(self.board)