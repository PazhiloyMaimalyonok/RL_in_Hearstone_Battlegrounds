from classes.board_class import FightingBoard
from classes.player_class import Player


class Fight:
    max_attack_number = 100
    attacking_board = FightingBoard(player_board=[])
    defending_board = FightingBoard(player_board=[])

    def __init__(self, first_player: Player, second_player: Player):
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_fighting_board = FightingBoard(player_board=first_player.board)
        self.second_player_fighting_board = FightingBoard(player_board=second_player.board)

    @property
    def someone_has_won(self):
        return len(self.first_player_fighting_board.fighting_board) == 0 \
               or len(self.second_player_fighting_board.fighting_board) == 0

    def prepare_for_first_player_attack(self):
        self.attacking_board = self.first_player_fighting_board
        self.defending_board = self.second_player_fighting_board

    def prepare_for_second_player_attack(self):
        self.attacking_board = self.first_player_fighting_board
        self.defending_board = self.second_player_fighting_board

    def attack(self):
        attacking_minion = self.attacking_board.get_attacking_minion()
        defending_minion = self.defending_board.defending_minion

        attacking_minion.health -= defending_minion.attack
        defending_minion.health -= attacking_minion.attack

        if attacking_minion.health <= 0:
            self.first_player_fighting_board.kill_minion(minion=attacking_minion)
        if defending_minion.health <= 0:
            self.second_player_fighting_board.kill_minion(minion=defending_minion)

    def punch_first_player(self):
        damage = self.second_player.tavern_tier + sum([minion.tavern_tier for minion in
                                                       self.second_player_fighting_board.fighting_board])
        self.first_player.health -= damage
        print(f'{self.second_player.name} punches {self.first_player.name} for {damage} damage')

    def punch_second_player(self):
        damage = self.first_player.tavern_tier + sum([minion.tavern_tier for minion in
                                                      self.first_player_fighting_board.fighting_board])
        self.first_player.health -= damage
        print(f'{self.first_player.name} punches {self.second_player.name} for {damage} damage')

    def punch_someone(self):
        if len(self.first_player_fighting_board.fighting_board) != 0:
            self.punch_second_player()
        elif len(self.second_player_fighting_board.fighting_board) != 0:
            self.punch_first_player()

    def simulate(self):
        print(f'{self.first_player.name} vs {self.second_player.name}')
        for i in range(self.max_attack_number):
            if self.someone_has_won:
                break
            self.prepare_for_first_player_attack()
            self.attack()

            if self.someone_has_won:
                break
            self.prepare_for_second_player_attack()
            self.attack()

        self.punch_someone()
