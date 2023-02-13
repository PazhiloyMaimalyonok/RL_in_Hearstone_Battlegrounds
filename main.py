import random

class Card:

    minions_list = ['Wrath_Weaver', 'Tavern_Tipper']

    def __init__(self, card_name):
        if card_name == 'Wrath_Weaver':
            self.card_name = card_name
            self.attack = 1
            self.hp = 3
            self.type = 'Minion'
            self.klass = 'Neutral'
            self.tavern_level = 1
            self.card_amount = 3
        elif card_name == 'Tavern_Tipper':
            self.card_name = card_name
            self.attack = 2
            self.hp = 2
            self.type = 'Minion'
            self.klass = 'Neutral'
            self.tavern_level = 1
            self.card_amount = 3
        else:
            print('No such card yet')

    def card_info(self):
        return f'Card name: {self.card_name}, card attack: {self.attack}, card hp {self.hp}'

class Game:

    def __init__(self, players_number = 2):
        self.players_number = players_number
        #Adding required amount of cards to the pool
        self.cards_pool = []
        for card_name in Card.minions_list:
            for card_number in range(Card(card_name).card_amount):
                self.cards_pool.append(Card(card_name))
        random.shuffle(self.cards_pool)
    
    def card_draw(self):
        return self.cards_pool.pop()

    def card_return_to_pool(self, card):
        self.cards_pool.append(card)

class Tavern:

    def __init__(self, game): #Переменная game одна для таверн разных игроков. Реализовать внутри класса Game
        self.gold = 3
        self.level = 1
        self.minions_per_reroll = 3
        self.player_hand = []
        self.player_board = []
        self.tavern_board = []
        self.game = game
        #Starting board minions
        for card_number in range(self.minions_per_reroll):
            self.tavern_board.append(self.game.card_draw())
    
    def tavern_info(self):
        return f'Tavern board: {[card.card_info() for card in self.tavern_board]}'

    def buy(self, position):
        #checking hand size
        if len(self.player_hand) >= 10:
            print('Hand is full. Cannot buy any more cards')
        elif self.gold < 3:
            print('Not enough gold')
        elif position > len(self.tavern_board) - 1:
            print('Card index out of tavern_board range')
        else:
            #return self.tavern_board.pop(position)
            self.gold -= 3
            return self.player_hand.append(self.tavern_board.pop(position))
    
    def play_card(self, position):
        if self.player_hand[position].type != 'Minion':
            print('Can only handle Minion type cards now')
        elif len(self.player_board) >= 7:
            print('Player board is full. Cannot buy any more cards')
        elif position > len(self.player_hand) - 1:
            print('Card index out of player_hand range')
        else:
            return self.player_board.append(self.player_hand.pop(position))

    def sell(self, position):
        if position > len(self.player_board) - 1:
            print('Card index out of player_board range')
        else:
            self.gold += 1 #Change for 3-3 and 2-3 pirates
            self.game.card_return_to_pool(self.player_board.pop(position)) #проверить, что это работает для таверн разных игроков

    def reroll(self):
        if self.gold < 1:
            print('Not enough gold')
        else:
            for card_number in range(len(self.tavern_board)):
                self.game.card_return_to_pool(self.tavern_board.pop())
            for card_number in range(self.minions_per_reroll):
                self.tavern_board.append(self.game.card_draw())

class Fight:

    def __init__(self, first_player, second_player):
        self.first_player_board = []
        self.second_player_board = []
    


#Things to add: second player tavern check - done, fights, turns, players hp, buffs, drawing cards from the pool the same level or lower than your tavern

game = Game()
taverna = Tavern(game)
print(taverna.tavern_board)
print(taverna.tavern_info())
taverna.buy(2)
print(taverna.tavern_info())
print(taverna.player_hand[0].card_info())
taverna.play_card(0)
print(taverna.player_board[0].card_info())
print(f'Number of minions in pool before sell: {len(game.cards_pool)}')
taverna.sell(0)
print(taverna.player_board)
print(f'Number of minions in pool after sell: {len(game.cards_pool)}')
taverna.reroll()
print(f'Number of minions in pool after reroll: {len(game.cards_pool)}')
print(taverna.tavern_info())
print('second player')
taverna2 = Tavern(game)
print(taverna2.tavern_info())
print(f'Number of minions in pool after second player started: {len(game.cards_pool)}')