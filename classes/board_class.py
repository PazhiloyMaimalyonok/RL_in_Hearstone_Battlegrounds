import random
from typing import List

from classes.card_class import FightingMinion, MinionCard


class FightingBoard:
    attack_pointer = 0

    def __init__(self, player_board: List[MinionCard]):
        self.fighting_board = [FightingMinion(minion_card=minion_card) for minion_card in player_board]

    @property
    def list_of_positions_to_hit(self):
        list_of_positions_to_hit = []
        for position, minion in enumerate(self.fighting_board):
            if minion.provoke:
                list_of_positions_to_hit.append(position)
        if len(list_of_positions_to_hit) > 0:
            return list_of_positions_to_hit
        else:
            return list(range(len(self.fighting_board)))

    @property
    def defending_minion_position(self):
        return random.choice(self.list_of_positions_to_hit)

    @property
    def defending_minion(self):
        return self.fighting_board[self.defending_minion_position]

    def kill_minion(self, minion: FightingMinion):
        self.fighting_board.remove(minion)

    def get_attacking_minion(self):
        if self.fighting_board[self.attack_pointer].has_attacked:
            self.move_attack_pointer()
        return self.fighting_board[self.attack_pointer]

    def refresh_has_attack_statuses(self):
        for minion in self.fighting_board:
            minion.has_attacked = False

    def move_attack_pointer(self):
        if self.attack_pointer >= len(self.fighting_board):
            self.attack_pointer = 0
            self.refresh_has_attack_statuses()
        else:
            self.attack_pointer += 1
