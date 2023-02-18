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
        self.gold = 9 #!!!!!!!!!!!!!!!!!!!!!! вернуть 3, как и было
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

    def attack_sequence_v1(self): #зарандомить начало
        #Стэк для последовательности ходов и борд игрока отдельно. Работает, когда количество существ на столе не увеличивается. Работает ли, когда количество существ увеличивается?
        #Добавить случайный выбор первого хода, чтобы не всегда ходил игрок а

        #Последовательность аттак реализуется через стэки
        first_player_stack = list(self.first_player_board)
        second_player_stack = list(self.second_player_board)
        counter = 0 #Счетчик ходов, который определяет, какой из игроков атакует

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

                #Если какое-либо существо погибло, то выкидываем его со стола и убираем из стака
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
            #Добавляю конструкцию с трай, так как выкинутый элемент из self.first_player_board мог уже сходить и умереть. 
            #Поэтому он не должен  находиться в first_player_stack
                """
                try: 
                    first_player_stack.remove(attacking_minion_excluded)
                except:
                    pass
                try:
                    second_player_stack.remove(defending_minion_excluded)
                except:
                    pass
                """

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

                #Если какое-либо существо погибло, то выкидываем его со стола
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
            #Добавляю конструкцию с трай, так как выкинутый элемент из self.first_player_board мог уже сходить и умереть. 
            #Поэтому он не должен  находиться в first_player_stack. Добавить для В в итоговой реализации
            """
                try: 
                    second_player_stack.remove(attacking_minion_excluded)
                except:
                    pass
                try:
                    first_player_stack.remove(defending_minion_excluded)
                except:
                    pass
            """

            counter += 1
        
        print(f'Стол первого игрока после боя: {[minion.card_info() for minion in self.first_player_board]}')
        print(f'Стол второго игрока после боя: {[minion.card_info() for minion in self.second_player_board]}')
        if len(self.first_player_board) > 0 and len(self.second_player_board) <= 0:
            print(f'Победил первый')
        elif len(self.second_player_board) > 0 and len(self.first_player_board) <= 0:
            print(f'Победил второй')
        elif len(self.first_player_board) <= 0 and len(self.second_player_board) <= 0:
            print(f'Ничья')
        else:
            print(f'Что-то странное. Количество ударов = {counter}')

    def attack_interaction(self, attacking_minion, defending_minion):#как изменять параметры существа?        
        pass

    pass

#Things to add: second player tavern check - done, fights, turns, players hp, buffs, drawing cards from the pool the same level or lower than your tavern


#testing Fight(). Изменил количества стартового золота для теста
game = Game()
taverna_first_player = Tavern(game)
taverna_first_player.buy(0)
taverna_first_player.buy(0)
taverna_first_player.play_card(0)
taverna_first_player.play_card(0)
print([minion.card_info() for minion in taverna_first_player.player_board])

taverna_second_player = Tavern(game)
taverna_second_player.buy(0)
taverna_second_player.buy(0)
taverna_second_player.play_card(0)
taverna_second_player.play_card(0)
print([minion.card_info() for minion in taverna_second_player.player_board])

fight = Fight(taverna_first_player, taverna_second_player)
fight.attack_sequence_v1()
