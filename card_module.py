from mechanics_module import *
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
    cards_data = pd.read_excel('cards_data.xlsx')
    cards_data = cards_data[(cards_data['use_flg'] == 1)]

    def __init__(self, card_name):
        cards_data = Card.cards_data
        cards_data = cards_data[cards_data['card_name'] == card_name]
        if cards_data.shape[0] == 0:
            raise ValueError("No such card yet")
        elif cards_data.shape[0] > 1:
            raise ValueError("Несколько карт с одинаковым названием")
        for index, row in cards_data.iterrows(): # итерируется по одной строке
            self.card_name = row['card_name']
            self.type = row['type']
            self.tavern_level = int(row['tavern_level'])

    def card_info(self):
        raise NotImplementedError("Subclass must implement the card_info method.")

class MinionCard(Card):
    minions_from_pool_mask = (Card.cards_data['type'] == 'Minion') & (Card.cards_data['sold_at_tavern'] == 1)
    minions_list = list(Card.cards_data[minions_from_pool_mask]['card_name'].values)
    def __init__(self, card_name):
        super().__init__(card_name)
        cards_data = Card.cards_data[Card.cards_data['type'] == 'Minion']
        cards_data = cards_data[cards_data['card_name'] == card_name]
        if cards_data.shape[0] == 0:
            raise ValueError("No such minion yet")
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
        
        print(f'Card: {self.card_name}, original attack: {self.attack}, original hp: {self.hp}')
        if buff_type == 'hp':
            self.hp += buff_value  
        elif buff_type == 'attack':
            self.attack += buff_value
        print(f'Card: {self.card_name}, new attack: {self.attack}, new hp: {self.hp}')

    def trigger(self, played_card, tavern=None):
        for mechanic in self.mechanics_list:
            mechanic(card = self, played_card = played_card, tavern = tavern).trigger()
            
class SpellCard(Card):
    def __init__(self, card_name):
        super().__init__(card_name)
        cards_data = Card.cards_data[Card.cards_data['type'] == 'Spell']
        cards_data = cards_data[cards_data['card_name'] == card_name]
        if cards_data.shape[0] == 0:
            raise ValueError("No such spell yet")
        elif cards_data.shape[0] > 1:
            raise ValueError("Несколько карт с одинаковым названием")
        for index, row in cards_data.iterrows(): # итерируется по одной строке
            self.card_name = row['card_name']            
            self.tavern_level = int(row['tavern_level'])
            self.card_amount = int(row['card_amount'])
            if pd.notna(row['spell_effect_list']):
                self.spell_effect_list = [eval(mechanics) for mechanics in row['spell_effect_list'].split(',')]
            else:
                self.spell_effect_list = []
        # Add other spell-specific attributes as needed

    def card_info(self):
        info = super().card_info()
        return f'{info}, Effect: {self.effect}'

    def trigger(self, played_card, tavern=None):
        # Implement spell-specific mechanics if any
        for mechanic in self.spell_effect_list:
            mechanic(card = self, played_card = played_card, tavern = tavern).trigger()
