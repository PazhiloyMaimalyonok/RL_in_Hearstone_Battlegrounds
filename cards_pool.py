import random
from card import Card

class CardsPool:
    """Описание
    Что сейчас класс собой представляет

    Что хочу от класса

    Мысли по улучшению

    """
    def __init__(self):
        self.cards_pool = []
        for card_name in Card.minions_list:
            for card_number in range(Card(card_name).card_amount):
                self.cards_pool.append(Card(card_name))
        random.shuffle(self.cards_pool)

    def card_draw(self) -> Card:
        return self.cards_pool.pop()

    def card_return_to_pool(self, card: Card):
        self.cards_pool.append(card)
        
a = CardsPool()
a.card_draw()