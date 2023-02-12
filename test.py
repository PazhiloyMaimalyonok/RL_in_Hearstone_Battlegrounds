class Card:

    cards_list = ['Wrath_Weaver', 'Tavern_Tipper']

    def __init__(self, card_name):
        if card_name == 'Wrath_Weaver':
            self.card_name = card_name
            self.attack = 1
            self.hp = 3
            self.type = 'Neutral'
            self.tavern_level = 1
            self.card_amount = 3
        elif card_name == 'Tavern_Tipper':
            self.card_name = card_name
            self.attack = 2
            self.hp = 2
            self.type = 'Neutral'
            self.tavern_level = 1
            self.card_amount = 3
        else:
            print('No such card yet')

    pass

class Game:

    def __init__(self, players_number = 2):
        self.players_number = players_number
        #Adding required amount of cards to the pool
        self.cards_pool = []
        for card_name in Card.cards_list:
            for card_number in range(Card(card_name).card_amount):
                cards_pool.append(Card(card_name))
    
    pass

class Tavern:

    def __init__(self):
        self.gold = 3
        self.level = 1
        self.player_board = []
        self.tavern_board = []

    def buy(self):
        pass

    pass

cards_pool = []
for card_name in Card.cards_list:
    for card_number in range(Card(card_name).card_amount):
        print(card_name, card_number + 1)
        cards_pool.append(Card(card_name))

for card in cards_pool:
    print(card.card_name)