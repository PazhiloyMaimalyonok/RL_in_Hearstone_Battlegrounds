class Card:
    """Описание
    Что сейчас класс собой представляет
        Класс с картами. Изначально задумывался только для миньонов. 
    Что хочу от класса
        Класс или несколько классов для всех типов карт: заклинания, миньоны
    Мысли по улучшению
        Перенести стоимость карты из класса Tavern сюда. Базовую стоимость перенести можно сюда, но для игрока существо все равно может стоить по-другому
            . Так что финальную стоимость можно оставить в таверне.
        МБ надо его сделать чуть более общим, чтобы потом сделать дочерние: миньоны, заклинания.
        Может быть клас миньонов надо будет разбить по типам существ
    Вопрос для МВП
        Что делать с триплетами?
    """
    minions_list = ['Wrath_Weaver', 'Tavern_Tipper', 'Backstage_Security']

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
        elif card_name == 'Backstage_Security':
            # Доработать карту
            self.card_name = card_name
            self.attack = 4
            self.hp = 4
            self.type = 'Minion'
            self.klass = 'Demon'
            self.tavern_level = 1
            self.card_amount = 17
        else:
            print('No such card yet')

    def card_info(self):
        return f'Card name: {self.card_name}, card attack: {self.attack}, card hp {self.hp}'
    
    def buff_card(self, buff_value, buff_type):
        allowed_buff_types = {'hp', 'attack'}
        if buff_type not in allowed_buff_types:
            raise ValueError("Invalid buff type. Must be one of: {}".format(allowed_buff_types))
        
        print(f'Card: {self.card_name}, original attack: {self.attack}, original hp {self.hp}')
        if buff_type == 'hp':
            self.hp += buff_value  
        elif buff_type == 'attack':
            self.attack += buff_value
        print(f'Card: {self.card_name}, new attack: {self.attack}, new hp {self.hp}')
