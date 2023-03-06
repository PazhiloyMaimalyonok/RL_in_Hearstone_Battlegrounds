from typing import List

from classes.deck_class import Deck
from classes.player_class import Player


class Game:

    def __init__(self, players: List[Player], deck: Deck):
        self.players = players
        self.turn_number = 1
        self.deck = deck

    def play_game(self):
        game = Game()
        print('Would u like to name players? 1 - Yes, 0 - No')
        agreement = int(input())
        if agreement == 1:
            print('Enter players names like this "Player1 Player2"')
            players_names = [player_name for player_name in input().split()]
            players_taverns = []
            for i in range(self.players_number):
                players_taverns.append(Tavern(game, player_name=players_names[i]))
        else:
            players_taverns = []
            for i in range(self.players_number):
                players_taverns.append(Tavern(game, player_name='Player' + str(i + 1)))
        while len(players_taverns) > 1:
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
                    print('error')
            for player in players_taverns:
                if player.player_hp <= 0:
                    players_taverns.remove(player)

        print(f'Player {players_taverns[0].player_name} won')
