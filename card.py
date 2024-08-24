class Card:
    """Описание
    Что сейчас класс собой представляет
        Класс с картами. Изначально задумывался только для миньонов. 
    Что хочу от класса
        Класс или несколько классов для всех типов карт: заклинания, миньоны
    Мысли по улучшению
        Перенести стоимость карты из класса Tavern сюда
        МБ надо его сделать чуть более общим, чтобы потом сделать дочерние: миньоны, заклинания.
        Может быть клас миньонов надо будет разбить по типам существ
    Returns:
        _type_: _description_
    """
    minions_list = ['Wrath_Weaver', 'Tavern_Tipper']

    def __init__(self, card_name):
        if card_name == 'Wrath_Weaver':
            self.card_name = card_name
            self.attack = 1
            self.hp = 3
            self.type = 'Minion'
            self.klass = 'Neutral'
            self.tavern_level = 1
            self.card_amount = 17
        elif card_name == 'Tavern_Tipper':
            self.card_name = card_name
            self.attack = 2
            self.hp = 2
            self.type = 'Minion'
            self.klass = 'Neutral'
            self.tavern_level = 1
            self.card_amount = 17
        else:
            print('No such card yet')

    def card_info(self):
        return f'Card name: {self.card_name}, card attack: {self.attack}, card hp {self.hp}'