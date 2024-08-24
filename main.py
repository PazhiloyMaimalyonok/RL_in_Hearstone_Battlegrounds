import random
import copy
from cards_pool import CardsPool

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

class Game:
    """Описание
    Что сейчас класс собой представляет
        Класс для партии игры. Определяет очередность действий игроков, выбирает следующего противника
        , рассчитывает урон после сражения, определяет, кто победил в партии
    Что хочу от класса
        Класс или несколько классов для всех типов карт: заклинания, миньоны
    Мысли по улучшению
        Почему пул существ создается в Game, а не в Tavern? 
            Потому что Tavern уникальна для игрока в партии (Game). А пул существ уникален для партии (Game)
        Почему метод card_draw, card_return_to_pool лежат в Game?
        Переделать play_game по совету chatGPT
    """
    def __init__(self, players_number = 2):
        self.players_number = players_number
        self.cards_pool = CardsPool()
    
    def create_players_taverns(self):
        # Handle player input and create taverns
        agreement = int(input("Would you like to name players? 1 - Yes, 0 - No"))
        if agreement == 1:
            players_names = [player_name for player_name in input("Enter players names like this 'Player1 Player2'").split()]
        else:
            players_names = [f"Player{i+1}" for i in range(self.players_number)]
        return [Tavern(self, player_name=player_name) for player_name in players_names]
    
    def card_draw(self):
        return self.cards_pool.card_draw()

    def card_return_to_pool(self, card):
        self.cards_pool.card_return_to_pool(card)

    def play_round(self, players_taverns):
        # Play a round of the game
        for player in players_taverns:
            player.player_turn()
        fighting_spisok = list(players_taverns)
        while len(fighting_spisok) > 1:
            fighter1, fighter2 = random.sample(fighting_spisok, 2)
            fighting_spisok.remove(fighter1)
            fighting_spisok.remove(fighter2)
            player_won, damage_dealt = Fight(fighter1, fighter2).simulate()
            if player_won == -1:
                pass
            elif player_won == 0:
                fighter2.player_hp -= damage_dealt
            elif player_won == 1:
                fighter1.player_hp -= damage_dealt
            else:
                print("error")
        for player in players_taverns:
            if player.player_hp <= 0:
                players_taverns.remove(player)

    def declare_winner(self, players_taverns):
        # Declare the winner
        print(f"Player {players_taverns[0].player_name} won")
        
    def play_game(self):
        players_taverns = self.create_players_taverns()
        while len(players_taverns) > 1:
            self.play_round(players_taverns)
        self.declare_winner(players_taverns)
        
class Tavern:
    """Описание
    Что сейчас класс собой представляет
        Класс Таверны игрока: ее уровень, количество карт в реролле, количество максимально золота.
        Также тут лежит хп игрока и метод player_turn, который по факту запускает ход.
    Что хочу от класса
    Мысли по улучшению
        Почему player_turn лежит тут, а не в классе Game
            В нем используются методы из этого класса, поэтому тут и лежит. Вроде это ок
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
    
    def tavern_info(self):
        return f'Tavern board: {[card.card_info() for card in self.tavern_board]}'
    
    def player_hand_info(self):
        return f'Player hand: {[card.card_info() for card in self.player_hand]}'
    
    def player_board_info(self):
        return f'Player board: {[card.card_info() for card in self.player_board]}'

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
        if position > len(self.player_hand) - 1:
            print('Card index out of player_hand range')
        elif self.player_hand[position].type != 'Minion':
            print('Can only handle Minion type cards now')
        elif len(self.player_board) >= 7:
            print('Player board is full. Cannot buy any more cards')
        else:
            return self.player_board.append(self.player_hand.pop(position))

    def sell(self, position):
        if position > len(self.player_board) - 1:
            print('Card index out of player_board range')
        else:
            self.gold += 1 #Change for 3-3 and 2-3 pirates
            self.game.card_return_to_pool(self.player_board.pop(position)) #проверить, что это работает для таверн разных игроков

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

class Fight:
    """Описание
    Что сейчас класс собой представляет
        Класс симуляции боя
    Что хочу от класса
        Класс симуляции боя, но более читаемый
    Мысли по улучшению
        Разбить его на несколько методов
    """

    def __init__(self, first_player, second_player):
        #self.first_player_board = list(first_player.player_board) #Надо ли делать копию? Yes
        #self.second_player_board = list(second_player.player_board)
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_board = [copy.deepcopy(minion) for minion in first_player.player_board]
        self.second_player_board = [copy.deepcopy(minion) for minion in second_player.player_board]

    def simulate(self): #зарандомить начало
        #Стэк для последовательности ходов и борд игрока отдельно. Работает, когда количество существ на столе не увеличивается. Работает ли, когда количество существ увеличивается?
        #Добавить случайный выбор первого хода, чтобы не всегда ходил игрок а

        #Последовательность аттак реализуется через стэки
        first_player_stack = list(self.first_player_board)
        second_player_stack = list(self.second_player_board)

        counter = random.randint(0, 1) #Счетчик ходов, который определяет, какой из игроков атакует. Генерируется случайно, чтобы не всегда атаковал первый

        while len(self.first_player_board) * len(self.second_player_board) > 0: #прекращаем битву, когда у одного из игроков умрут все существа. Добавить ограничение на кол-во ударов
            if counter % 2 == 0: # разбиваем на ход первого игрока и второго
                print('---------------------------------------Ход первого игрока---------------------------------------')
                if first_player_stack == []:
                    first_player_stack = list(self.first_player_board)
                print(f'first_player_stack: {[minion.card_info() for minion in first_player_stack]}, second_player_stack: {[minion.card_info() for minion in second_player_stack]}')

                #Выбираем существо, которое будет атаковать. Убираем его из стака
                attacking_minion = first_player_stack.pop(0)
                print(f'У первого игрока атакует карта: {attacking_minion.card_info()}, ее позиция на столе: {self.first_player_board.index(attacking_minion)}')
                #Выбираем существо, которое будет защищаться
                defending_minion = self.second_player_board[random.randint(0, len(self.second_player_board) - 1)]
                print(f'У второго игрока защищается карта: {defending_minion.card_info()}, ее позиция на столе: {self.second_player_board.index(defending_minion)}')

                #Если какое-либо существо погибло, то выкидываем его со стола и из стека
                attacking_minion.hp -= defending_minion.attack
                defending_minion.hp -= attacking_minion.attack
                if attacking_minion.hp <= 0:
                    attacking_minion_excluded = self.first_player_board.remove(attacking_minion)
                    try: 
                        first_player_stack.remove(attacking_minion)
                    except:
                        pass
                if defending_minion.hp <= 0:
                    defending_minion_excluded = self.second_player_board.remove(defending_minion)
                    try:
                        second_player_stack.remove(defending_minion)
                    except:
                        pass
                print(f'Статы атакующей карты после атаки: {attacking_minion.card_info()}, Статы защищающейся карты после атаки: {defending_minion.card_info()}')
                print(f'Стол атакующего игрока после атаки: {[minion.card_info() for minion in self.first_player_board]}\
                    , Стол защищающегося игрока после атаки: {[minion.card_info() for minion in self.second_player_board]}')

            else:
                print('---------------------------------------Ход второго игрока---------------------------------------')
                if second_player_stack == []:
                    second_player_stack = list(self.second_player_board)
                print(f'first_player_stack: {[minion.card_info() for minion in first_player_stack]}, second_player_stack: {[minion.card_info() for minion in second_player_stack]}')

                #Выбираем существо, которое будет атаковать. Убираем его из стака
                attacking_minion = second_player_stack.pop(0)
                print(f'У второго игрока атакует карта: {attacking_minion.card_info()}, ее позиция на столе: {self.second_player_board.index(attacking_minion)}')
                #Выбираем существо, которое будет защищаться
                defending_minion = self.first_player_board[random.randint(0, len(self.first_player_board) - 1)]
                print(f'У первого игрока защищается карта: {defending_minion.card_info()}, ее позиция на столе: {self.first_player_board.index(defending_minion)}')

                #Если какое-либо существо погибло, то выкидываем его со стола и из стека
                attacking_minion.hp -= defending_minion.attack
                defending_minion.hp -= attacking_minion.attack
                if attacking_minion.hp <= 0:
                    attacking_minion_excluded = self.second_player_board.remove(attacking_minion)
                    try: 
                        second_player_stack.remove(attacking_minion)
                    except:
                        pass
                if defending_minion.hp <= 0:
                    defending_minion_excluded = self.first_player_board.remove(defending_minion)
                    try:
                        first_player_stack.remove(defending_minion)
                    except:
                        pass
                print(f'Статы атакующей карты после атаки: {attacking_minion.card_info()}, Статы защищающейся карты после атаки: {defending_minion.card_info()}')
                print(f'Стол атакующего игрока после атаки: {[minion.card_info() for minion in self.second_player_board]}\
                    , Стол защищающегося игрока после атаки: {[minion.card_info() for minion in self.first_player_board]}')

            counter += 1
        
        print(f'Стол первого игрока после боя: {[minion.card_info() for minion in self.first_player_board]}')
        print(f'Стол второго игрока после боя: {[minion.card_info() for minion in self.second_player_board]}')
        if len(self.first_player_board) > 0 and len(self.second_player_board) <= 0:
            print(f'Победил {self.first_player.player_name}')
            player_won = 0
            damage_dealt = sum([minion.tavern_level for minion in self.first_player_board]) + self.first_player.level
            return player_won, damage_dealt
        elif len(self.second_player_board) > 0 and len(self.first_player_board) <= 0:
            print(f'Победил {self.second_player.player_name}')
            player_won = 1
            damage_dealt = sum([minion.tavern_level for minion in self.second_player_board]) + self.second_player.level
            return player_won, damage_dealt
        elif len(self.first_player_board) <= 0 and len(self.second_player_board) <= 0:
            print(f'Ничья')
            player_won = -1
            damage_dealt = 0
            return player_won, damage_dealt
        else:
            print(f'Что-то странное. Количество ударов = {counter}')

    def attack_interaction(self, attacking_minion, defending_minion):#как изменять параметры существа?        
        pass

    pass

#Things to add: second player tavern check - done, fights - done, fights results, turns, players hp, pygame visualization, triplets, drawing cards from the pool the same level or lower than your tavern, buffs

#Trying all game at once
game = Game()
game.play_game()

"""
game = Game()
taverna_first_player = Tavern(game)
for i in range(10):
    taverna_first_player.player_turn()
"""