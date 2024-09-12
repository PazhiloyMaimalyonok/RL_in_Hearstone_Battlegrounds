from classes.deck_class import Deck
from classes.game_class import Game
from classes.player_class import Player


def start_game():
    players_number = 2
    players = []
    for i in range(1, players_number + 1):
        players.append(Player(name=f'Player {i}'))
    deck = Deck()
    game = Game(players=players, deck=deck)
    game.play_game()


if __name__ == '__main__':
    start_game()
