import copy
import random
import numpy as np

class Fight:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_board = [copy.deepcopy(minion) for minion in first_player.player_board]
        self.second_player_board = [copy.deepcopy(minion) for minion in second_player.player_board]
        self.first_player_attacking_order = self.first_player_board
        self.second_player_attacking_order = self.second_player_board

    def simulate(self):
        # Решаю, кто первый будет атаковая. Задача каунтера -- передавать инициативу атаки от одного другому
        len_first_board = len(self.first_player_board)
        len_second_board = len(self.second_player_board)
        if len_first_board == len_second_board:
            counter = random.randint(0, 1)
        else:
            counter = np.argmax([len_first_board, len_second_board])
        # Мб вынести определения, кто первый атакует или вообще определение кто в принципе атакует в отедльную функцию
        while self.first_player_board and self.second_player_board:
            if counter % 2 == 0:
                self.attack(self.first_player_attacking_order, self.second_player_board)
            else:
                self.attack(self.second_player_attacking_order, self.first_player_board)
            counter += 1

        self.determine_winner()

    def attack(self, attacking_order, defending_board):
        attacking_minion = attacking_order.pop(0)
        defending_minion = random.choice(defending_board)

        print(f"Attacking minion: {attacking_minion.card_info()}")
        print(f"Defending minion: {defending_minion.card_info()}")

        self.resolve_attack(attacking_minion, defending_minion)

        print(f"Attacking minion stats after attack: {attacking_minion.card_info()}")
        print(f"Defending minion stats after attack: {defending_minion.card_info()}")

        # Добавляю существо в конец очереди атаки, если он не умер
        if attacking_minion.hp > 0:
            attacking_order.append(attacking_minion)
        
    def resolve_attack(self, attacking_minion, defending_minion):
        attacking_minion.hp -= defending_minion.attack
        
        defending_minion.hp -= attacking_minion.attack

        if attacking_minion.hp <= 0:
            self.remove_minion(attacking_minion)
        if defending_minion.hp <= 0:
            self.remove_minion(defending_minion)

    def remove_minion(self, minion):
        if minion in self.first_player_board:
            self.first_player_board.remove(minion)
            # self.first_player_attacking_order.remove(minion)
        elif minion in self.second_player_board:
            self.second_player_board.remove(minion)
            # self.second_player_attacking_order.remove(minion)

    def determine_winner(self):
        if self.first_player_board and not self.second_player_board:
            print(f"Player {self.first_player.player_name} wins!")
            return 0, sum([minion.tavern_level for minion in self.first_player_board]) + self.first_player.level
        elif self.second_player_board and not self.first_player_board:
            print(f"Player {self.second_player.player_name} wins!")
            return 1, sum([minion.tavern_level for minion in self.second_player_board]) + self.second_player.level
        else:
            print("It's a tie!")
            return -1, 0