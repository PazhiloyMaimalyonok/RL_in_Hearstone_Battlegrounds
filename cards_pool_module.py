import random
from card_module import *

class CardsPool:
    """Описание
    Что сейчас класс собой представляет
        Класс, который отвечает за создание пула карт для конкретной игры.
        Сейчас шафлит все карты. А что делать, если у юзера первая таверна, а в пуле есть карты второй таверны?
    Что хочу от класса
        --
    Мысли по улучшению
        Сейчас шафлит все карты. А что делать, если у юзера первая таверна, а в пуле есть карты второй таверны?
    Вопрос для МВП
        Что делать с доставанием карт из своей таверны? Это к классу Tavern?
    """
    def __init__(self):
        self.cards_pool = []
        for card_name in MinionCard.minions_list:
            for card_number in range(MinionCard(card_name).card_amount):
                self.cards_pool.append(MinionCard(card_name))
        random.shuffle(self.cards_pool)

    def card_draw(self) -> MinionCard:
        return self.cards_pool.pop()

    def card_return_to_pool(self, card: MinionCard):
        if card.card_name in MinionCard.minions_list:
            self.cards_pool.append(card)
        
# a = CardsPool()
# print([card.card_name for card in a.cards_pool])