from mechanics_module import PlayedCardBuffMechanic, BattlecryMechanic
import pandas as pd

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
    cards_data_outer = pd.read_excel('cards_data.xlsx')
    minions_list = list(cards_data_outer[cards_data_outer['use_flg'] == 1]['card_name'].values)

    def __init__(self, card_name):
        cards_data = pd.read_excel('cards_data.xlsx')
        cards_data = cards_data[(cards_data['use_flg'] == 1) & (cards_data['card_name'] == card_name)]
        if cards_data.shape[0] == 0:
            raise ValueError("No such card yet")
        elif cards_data.shape[0] > 1:
            raise ValueError("Несколько карт с одинаковым названием")
        for index, row in cards_data.iterrows(): # итерируется по одной строке
            self.card_name = row['card_name']
            self.attack = int(row['attack'])
            self.hp = int(row['hp'])
            self.type = row['type']
            self.klass = row['klass']
            self.tavern_level = int(row['tavern_level'])
            self.card_amount = int(row['card_amount'])
            if pd.notna(row['mechanics_list']):
                self.mechanics_list = [eval(mechanics) for mechanics in row['mechanics_list'].split(',')]
            else:
                self.mechanics_list = []

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
    
    def get_object(self):
        return self
    
    def trigger_buffs(self, played_card, tavern=None):
        # При разыгрывании карты триггерит бафы
        for mechanic in self.mechanics_list:
            mechanic(self.get_object(), played_card, tavern).trigger_buffs()
