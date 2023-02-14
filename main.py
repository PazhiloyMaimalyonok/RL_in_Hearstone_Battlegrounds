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
        self.first_player_board = list(first_player.player_board) #Надо ли делать копию? Yes
        self.second_player_board = list(second_player.player_board)

    pass

#experimental vibes
board_a = [1,2,3, 4, 5, 6, 7]
board_b = [1,2,3]
#Стэк для последовательности ходов и борд игрока отдельно. Работает с неизменяющимися, Работает с изменяющимися
stack_a = list(board_a)
stack_b = list(board_b)
#while len(board_a) * len(board_b)>0:
cnt = 0
while cnt < 9:
    if stack_a == []:
        stack_a = list(board_a)
    if stack_b == []:
        stack_b = list(board_b)
    print(f'A-stack: {stack_a}, B-stack: {stack_b}')
    elem_a, elem_b = stack_a.pop(0), stack_b.pop(0)
    print(f'A-elem: {elem_a}, B-elem: {elem_b}')
    excluded = board_a.pop(random.randint(0, len(board_a) - 1)) 
    print(f'Выкинули: {excluded}')
    #Добавляю конструкцию с трай, так как выкинутый элемент из board_a мог уже сходить и не находиться в stack_a
    try: 
        stack_a.remove(excluded)
    except:
        pass
    cnt += 1
    
"""
#Остаток от деления. Работает с неизменяющимися, не работает с изменяющимися
cnt = 0
#while len(a) * len(b)>0:
while cnt < 9:
    print(f'Counter: {cnt}')
    print(f'A-array: {a}')
    print(f'A-element: {a[cnt % len(a)]}, B-element: {b[cnt % len(b)]}')
    print(f'Остаток от деления для а: {cnt % len(a)}, Остаток от деления для В: {cnt % len(b)}')
    excluded = a.pop(random.randint(0, len(a) - 1)) 
    print(f'Выкинули: {excluded}')
    cnt += 1
"""

"""
a = [1,2,3, 4, 5, 6, 7]
b = list(a)
print(a)
while len(a) * len(b)>0:
    for x in a:
        print(x)
        a.pop(random.randint(0, len(a) - 1))    
        print(a)
"""

#Things to add: second player tavern check - done, fights, turns, players hp, buffs, drawing cards from the pool the same level or lower than your tavern
