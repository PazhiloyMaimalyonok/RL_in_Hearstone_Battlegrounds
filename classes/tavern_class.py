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

    def get_gold_for_this_turn(self):
        gold = self.turn_number + 2
        if gold > 10:
            gold = 10

        return gold

    def get_minions_per_reroll_for_this_turn(self):
        minions_per_reroll_dictionary = {1: 3, 2: 4, 3: 4, 4: 5, 5: 5}
        if self.player.tavern_tier > 5:
            return 6
        else:
            return minions_per_reroll_dictionary[self.player.tavern_tier]

    def fill_up_board(self):
        minions_list = self.player.frozen_minions
        how_many_minions_to_add = self.minions_per_reroll - len(self.board)
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

    def player_turn(self):
        self.reroll(reroll_type='start_of_the_turn_reroll')
        self.gold = min(2 + 1 * self.turn_number, 10)
        print(f'-------------------------Player {self.player_name} turn-------------------------')
        print(self.tavern_info())
        print(self.player_hand_info())
        print(self.player_board_info())
        print(f'players gold: {self.gold}, playerss hp: {self.player_hp}, players tavern level: {self.level}')
        action_number = -99
        while action_number != 6:
            print(f'Print action number: '
                  f'1 - buy a minion, '
                  f'2 - play a card, '
                  f'3 - sell a minion, '
                  f'4 - reroll, '
                  f'5 - show stats, '
                  f'6 - end the turn')
            action_number = int(input())
            if action_number == 1:
                print(self.tavern_info())
                print(f'Choose minions position. Starting from 0. Can use negatives')
                action_number = int(input())
                self.buy(action_number)

            elif action_number == 2:
                print(self.player_hand_info())
                print(f'Choose minions position. Starting from 0. Can use negatives')
                action_number = int(input())
                self.play_card(action_number)

            elif action_number == 3:
                print(self.player_board_info())
                print(f'Choose minions position. Starting from 0. Can use negatives')
                action_number = int(input())
                self.sell(action_number)

            elif action_number == 4:
                self.reroll()
                print(self.tavern_info())

            elif action_number == 5:
                print(self.tavern_info())
                print(self.player_hand_info())
                print(self.player_board_info())
                print(f'players gold: {self.gold}, playerss hp: {self.player_hp}, players tavern level: {self.level}')

            elif action_number == 6:
                pass
            else:
                print('wrong number')
        self.turn_number += 1
