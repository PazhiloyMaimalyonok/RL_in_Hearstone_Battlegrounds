import random
from card_module import *

class CardsPool:
    def __init__(self):
        self.cards_pool = []
        for card_name in MinionCard.minions_list:
            for card_number in range(MinionCard(card_name).card_amount):
                self.cards_pool.append(MinionCard(card_name))
        random.shuffle(self.cards_pool)

    def card_draw(self) -> MinionCard:
        if self.cards_pool:
            index = random.randrange(len(self.cards_pool))
            return self.cards_pool.pop(index)
        else:
            raise Exception("No cards left in the pool")

    def card_return_to_pool(self, card: MinionCard):
        if card.card_name in MinionCard.minions_list:
            original_card = MinionCard(card.card_name)
            self.cards_pool.append(original_card)
