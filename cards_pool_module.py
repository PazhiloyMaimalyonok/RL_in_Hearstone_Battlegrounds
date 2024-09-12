import random
from card_module import Card

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
        for card_name in Card.minions_list:
            for card_number in range(Card(card_name).card_amount):
                self.cards_pool.append(Card(card_name))
        random.shuffle(self.cards_pool)

    def card_draw(self) -> Card:
        return self.cards_pool.pop()

    def card_return_to_pool(self, card: Card):
        self.cards_pool.append(card)
        
# a = CardsPool()
# print([card.card_name for card in a.cards_pool])