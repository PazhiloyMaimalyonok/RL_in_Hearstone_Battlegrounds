import copy
import random
import numpy as np

class Fight:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_board = [copy.deepcopy(minion) for minion in first_player.player_board]
        self.second_player_board = [copy.deepcopy(minion) for minion in second_player.player_board]
        self.first_player_attacking_order = self.first_player_board.copy()
        self.second_player_attacking_order = self.second_player_board.copy()
        self.fight_log = []  # Collect fight events for logging or display

    def simulate(self):
        len_first_board = len(self.first_player_board)
        len_second_board = len(self.second_player_board)
        if len_first_board == len_second_board:
            counter = random.randint(0, 1)
        else:
            counter = np.argmax([len_first_board, len_second_board])
        while self.first_player_board and self.second_player_board:
            if counter % 2 == 0:
                self.attack(self.first_player_attacking_order, self.second_player_board)
            else:
                self.attack(self.second_player_attacking_order, self.first_player_board)
            counter += 1
        return self.determine_winner()

    def attack(self, attacking_order, defending_board):
        if not attacking_order or not defending_board:
            return
        attacking_minion = attacking_order.pop(0)
        defending_minion = random.choice(defending_board)

        # Collect attack event data
        attack_event = {
            'attacking_minion': attacking_minion.card_info(),
            'defending_minion': defending_minion.card_info(),
        }
        self.resolve_attack(attacking_minion, defending_minion)

        # Update attack event with post-attack stats
        attack_event.update({
            'attacking_minion_after': attacking_minion.card_info(),
            'defending_minion_after': defending_minion.card_info(),
        })
        self.fight_log.append(attack_event)

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
        elif minion in self.second_player_board:
            self.second_player_board.remove(minion)

    def determine_winner(self):
        result = {}
        if self.first_player_board and not self.second_player_board:
            result['winner'] = self.first_player.player_name
            result['loser'] = self.second_player.player_name
            damage = sum([minion.tavern_level for minion in self.first_player_board]) + self.first_player.level
            result['damage'] = damage
            return 0, damage, result
        elif self.second_player_board and not self.first_player_board:
            result['winner'] = self.second_player.player_name
            result['loser'] = self.first_player.player_name
            damage = sum([minion.tavern_level for minion in self.second_player_board]) + self.second_player.level
            result['damage'] = damage
            return 1, damage, result
        else:
            result['tie'] = True
            return -1, 0, result
