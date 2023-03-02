class MinionCard:

    # TODO add card_amount somewhere

 

    def __init__(self, card_name, attack, hp, minion_type, tavern_tier):

        self.card_name = card_name

        self.attack = attack

        self.hp = hp

        self.minion_type = minion_type

        self.tavern_tier = tavern_tier

 

    def card_info(self):

        return f'Card name: {self.card_name}, card attack: {self.attack}, card hp {self.hp}'

class Deck:
    
    def __init__():
        self.pool = self.make_deck
       
    def make_deck(self):
        minions = csv.read('minions.txt')
        for minion in minions:
            card = Card(card_name=minion[0], attack=minion[1], ....)
