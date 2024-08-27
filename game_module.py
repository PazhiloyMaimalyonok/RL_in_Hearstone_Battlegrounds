from cards_pool_module import CardsPool
from tavern_module import Tavern
from fight_module import Fight
import random

class Game:
    """Описание
    Что сейчас класс собой представляет
        Класс для партии игры. Определяет очередность действий игроков, выбирает следующего противника
        , рассчитывает урон после сражения, определяет, кто победил в партии
    Что хочу от класса
        --
    Мысли по улучшению
        --
    """
    def __init__(self, players_number = 2):
        self.players_number = players_number
        self.cards_pool = CardsPool()
    
    def create_players_taverns(self, agreement = 0):
        # Handle player input and create taverns
        # agreement = int(input("Would you like to name players? 1 - Yes, 0 - No"))
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
        
game = Game()