from pprint import pprint

from classes.card_class import MinionCard
from classes.deck_class import Deck
from classes.player_class import Player


class Tavern:

    def __init__(self, player: Player, deck: Deck, turn_number):
        self.player = player
        self.deck = deck
        self.turn_number = turn_number

        # Get Tavern's parameters depending on turn number
        self.gold = self.get_gold_for_this_turn()
        self.minions_per_reroll = self.get_minions_per_reroll_for_this_turn()

        # Fill the board at the start of each tavern turn
        self.board = self.fill_up_board()

    def board_information(self):
        print("Tavern's board:")
        pprint(self.board)

    def get_gold_for_this_turn(self):
        return min(self.turn_number + 2, 10)

    def get_minions_per_reroll_for_this_turn(self):
        minions_per_reroll_dictionary = {1: 3, 2: 4, 3: 4, 4: 5, 5: 5}
        if self.player.tavern_tier > 5:
            return 6
        else:
            return minions_per_reroll_dictionary[self.player.tavern_tier]

    def fill_up_board(self):
        minions_list = self.player.frozen_minions
        how_many_minions_to_add = self.minions_per_reroll - len(self.player.frozen_minions)
        for i in range(how_many_minions_to_add):
            minions_list.append(self.deck.draw_card(players_tavern_tier=self.player.tavern_tier))
        return minions_list

    def clear_board(self):
        for minion in self.board:
            self.deck.cards_pool.append(minion)
        self.board.clear()

    def update_board(self):
        for i in range(self.minions_per_reroll):
            self.board.append(self.deck.draw_card(players_tavern_tier=self.player.tavern_tier))

    def buy(self, position):
        # checking hand size
        if len(self.player.hand) == 10:
            print('Hand is full. Cannot buy any more cards')
        elif self.gold < 3:
            print('Not enough gold')
        elif position > len(self.board) - 1:
            print('Card index out of tavern_board range')
        else:
            self.gold -= 3
            return self.player.hand.append(self.board.pop(position))

    def play_card(self, position):
        if position > len(self.player.hand) - 1:
            print('Card index out of player_hand range')
        elif self.player.hand[position].__class__ != MinionCard:
            print('Can only handle Minion type cards now')
        elif len(self.player.board) >= 7:
            print('Player board is full. Cannot buy any more cards')
        else:
            return self.player.board.append(self.player.hand.pop(position))

    def sell(self, position):
        if position > len(self.player.board) - 1:
            print('Card index out of player_board range')
        else:
            # TODO Change for 3-3 and 2-3 pirates
            self.gold += 1
            self.deck.cards_pool.append(self.player.board.pop(position))

    def reroll(self, reroll_type='usual'):
        if self.gold < 1 and reroll_type == 'usual':
            print('Not enough gold')
        else:
            self.clear_board()
            self.update_board()

    def player_turn(self, action):
        if action == 'Buy minion':
            self.board_information()
            print(f"Choose minion's position. Starting from 0. Can use negatives")
            self.buy(position=int(input()))

        elif action == 'Play card':
            self.player.hand_information()
            print(f"Choose minion's position. Starting from 0. Can use negatives")
            self.play_card(position=int(input()))

        elif action == 'Sell minion':
            self.player.board_information()
            print(f"Choose minion's position. Starting from 0. Can use negatives")
            self.sell(position=int(input()))

        elif action == 'Reroll':
            self.reroll()
            self.board_information()

        elif action == 'Stats':
            self.board_information()
            self.player.hand_information()
            self.player.board_information()
            print(f"Player's gold: {self.gold}, player's hp: {self.player.health}, "
                  f"player's tavern tier: {self.player.tavern_tier})")
