from card_module import *

class Tavern:
    """Описание
    Что сейчас класс собой представляет
        Класс Таверны игрока: ее уровень, количество карт в реролле, количество максимально золота.
        Также тут лежит хп игрока и метод player_turn, который по факту запускает ход. Вынести его в отдельный класс? наверное нет, ведь он меняет селф.переменные класса Таверн.
        Логично его оставить тут же
    Что хочу от класса
        Хочу, чтобы юзер на первой таверне не получил карт второго уровня.
        Хочу, чтобы мог собрать триплет.
    Мысли по улучшению
        Почему player_turn лежит тут, а не в классе Game
            В нем используются методы из этого класса, поэтому тут и лежит. Вроде это ок
    Вопрос для МВП
        Хочу, чтобы юзер на первой таверне не получил карт второго уровня.
        Хочу, чтобы мог собрать триплет.
    """
    def __init__(self, game, player_name = 'user'): #Переменная game одна для таверн разных игроков. Реализовать внутри класса Game
        self.player_name = player_name
        self.gold = 3
        self.level = 1
        self.minions_per_reroll = 3
        self.player_hand = []
        self.player_board = []
        self.tavern_board = []
        self.turn_number = 1
        self.player_hp = 5
        self.game = game
        #Starting board minions
        for card_number in range(self.minions_per_reroll):
            self.tavern_board.append(self.game.card_draw())
            
    def get_object(self):
        return self
    
    def change_player_hp_during_turn(self, amount):
        self.player_hp += amount
    
    def tavern_info(self):
        return f'Tavern board: {[card.card_info() for card in self.tavern_board]}'
    
    def player_hand_info(self):
        return f'Player hand: {[card.card_info() for card in self.player_hand]}'
    
    def player_board_info(self, board = None):
        if board == None:
            return f'Player board: {[card.card_info() for card in self.player_board]}'
        else:
            return f'Player board: {[card.card_info() for card in board]}'

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
        
    # def add_card_to_player_hand(self, card_name):
    #     if Card(card_name).type == 'Minion':
    #         self.player_hand.append(MinionCard(card_name))
    #     else:
    #         print('Is not able to add anything other than minions right now')
    
    def play_card(self, position):
        if position > len(self.player_hand) - 1:
            print('Card index out of player_hand range')
        elif self.player_hand[position].type != 'Minion':
            print('Can only handle Minion type cards now')
        elif len(self.player_board) >= 7:
            print('Player board is full. Cannot buy any more cards')
        else:
            played_card = self.player_hand.pop(position)
            self.player_board.append(played_card)
            self.update_board(played_card)
        
    def rearrange_board(self):
        # метод позволяет переставлять минионов местами
        pass
        
    def update_board(self, played_card):
        # Метод проходится по каждой карте и ее бафам и смотрит, как она забафается при выставлении текущей карты на стол
        for minion in self.player_board:
            minion.trigger(played_card, tavern = self.get_object())            

    def sell(self, position):
        if position > len(self.player_board) - 1:
            print('Card index out of player_board range')
        else:
            self.gold += 1 #Change for 3-3 and 2-3 pirates
            card_to_sell = self.player_board.pop(position)
            # card_to_sell.trigger(played_card = card_to_sell, tavern = self)
            self.game.card_return_to_pool(card_to_sell) #проверить, что это работает для таверн разных игроков

    def eat_minion(self, minion):
        if minion in self.tavern_board:
            # eat
            self.tavern_board.remove(minion)
            # return to pool
            self.game.card_return_to_pool(minion)
        else:
            print(f'minion not in tavern board')
        pass
        
    def reroll(self, reroll_type = 'usual'):
        if self.gold < 1 and reroll_type == 'usual':
            print('Not enough gold')
        else:
            for card_number in range(len(self.tavern_board)):
                self.game.card_return_to_pool(self.tavern_board.pop())
            for card_number in range(self.minions_per_reroll):
                self.tavern_board.append(self.game.card_draw())

    def player_turn(self):
        self.reroll(reroll_type = 'start_of_the_turn_reroll')
        self.gold = min(2 + 1 * self.turn_number, 10)
        print(f'-------------------------Player {self.player_name} turn-------------------------')
        print(self.tavern_info())
        print(self.player_hand_info())
        print(self.player_board_info())
        print(f'players gold: {self.gold}, playerss hp: {self.player_hp}, players tavern level: {self.level}')
        action_number = -99
        while action_number != 6:
            print(f'Print action number: 1 - buy a minion, 2 - play a card, 3 - sell a minion, 4 - reroll, 5 - show stats, 6 - end the turn')
            action_number = int(input())
            if action_number == 1:
                print(self.tavern_info())
                print(f'Choose minions position. Starting from 0. Can use negatives')
                action_number = int(input())
                self.buy(action_number)

            elif action_number == 2:
                print(self.player_hand_info())
                print(f'Choose minions position. Starting from 0. Can use negatives')
                action_number = int(input())
                self.play_card(action_number)

            elif action_number == 3:
                print(self.player_board_info())
                print(f'Choose minions position. Starting from 0. Can use negatives')
                action_number = int(input())
                self.sell(action_number)

            elif action_number == 4:
                self.reroll()
                print(self.tavern_info())

            elif action_number == 5:
                print(self.tavern_info())
                print(self.player_hand_info())
                print(self.player_board_info())
                print(f'players gold: {self.gold}, playerss hp: {self.player_hp}, players tavern level: {self.level}')

            elif action_number == 6:
                pass
            else:
                print('wrong number')
        self.turn_number += 1