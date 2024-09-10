# В этом файле я запускаю игру
import random
import copy
from cards_pool_module import CardsPool
from game_module import Game
from tavern_module import Tavern
from fight_module import Fight
from card_module import Card

#Things to add: second player tavern check - done, fights - done, fights results, turns, players hp, pygame visualization
# , triplets, drawing cards from the pool the same level or lower than your tavern, buffs

#Trying all game at once
game = Game()
game.play_game()