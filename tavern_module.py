from card_module import MinionCard
from events_system_module import GameEvent, EventType
from mechanics_module import *

class Tavern:
    def __init__(self, game, player_name='Player1'):
        self.game = game
        self.player_name = player_name
        self.player_hand = []
        self.player_board = []
        self.tavern_board = []
        self.gold = 3
        self.player_hp = 5
        self.turn_number = 1
        self.level = 1
        self.minions_per_reroll = 3
        self.max_player_board_size = 7  # Added this line to define the attribute
        self.event_manager = self.game.event_manager  # Reference to the game's event manager

    def get_object(self):
        return self

    def tavern_info(self):
        return f'Tavern board: {[minion.card_info() for minion in self.tavern_board]}'

    def player_hand_info(self):
        return f'Player hand: {[card.card_info() for card in self.player_hand]}'

    def player_board_info(self):
        return f'Player board: {[card.card_info() for card in self.player_board]}'

    def change_player_hp_during_turn(self, amount):
        self.player_hp += amount

    def buy(self, position):
        if position > len(self.tavern_board) - 1:
            print('Card index out of tavern_board range')
        elif self.gold < 3:
            print('Not enough gold')
        elif len(self.player_hand) >= 10:
            print('Player hand is full')
        else:
            self.gold -= 3
            self.player_hand.append(self.tavern_board.pop(position))

    def play_card(self, position):
        if position > len(self.player_hand) - 1:
            print('Card index out of player_hand range')
        elif len(self.player_board) >= self.max_player_board_size:
            print('Player board is full')
        else:
            card = self.player_hand.pop(position)
            self.player_board.append(card)
            card.enter_board(self.event_manager, self)  # Subscribe to events and set tavern reference

            # Trigger BattlecryMechanic directly if present
            for mechanic in card.mechanics_list:
                if isinstance(mechanic, BattlecryMechanic):  # <-- Added
                    mechanic.trigger()                       # <-- Added
                    print(f"{card.card_name}'s battlecry triggered.")  # <-- Added

            # Emit the CardPlayed event after battlecry has resolved
            played_card = card
            self.event_manager.emit(GameEvent(EventType.CARD_PLAYED, payload=played_card))
            """Закомментил код снизу, так как он больше не нужен
            self.update_board(played_card)

    def update_board(self, played_card):
        for minion in self.player_board:
            minion.trigger(played_card)
            """

    def sell(self, position):
        if position > len(self.player_board) - 1:
            print('Card index out of player_board range')
        else:
            self.gold += 1
            card_to_sell = self.player_board.pop(position)
            card_to_sell.leave_board()
            self.game.card_return_to_pool(card_to_sell)

    def eat_minion(self, minion):
        if minion in self.tavern_board:
            self.tavern_board.remove(minion)
            self.game.card_return_to_pool(minion)
        else:
            print(f'Minion not in tavern board')

    def reroll(self, reroll_type='usual'):
        if self.gold < 1 and reroll_type == 'usual':
            print('Not enough gold')
        else:
            if reroll_type == 'usual':
                self.gold -= 1  # Deduct 1 gold for usual reroll

            # Return all minions on the tavern board to the cards pool
            while self.tavern_board:
                minion = self.tavern_board.pop()
                self.game.card_return_to_pool(minion)

            # Draw new minions from the cards pool
            for _ in range(self.minions_per_reroll):
                new_minion = self.game.card_draw()
                self.tavern_board.append(new_minion)

    def player_turn(self):
        self.reroll(reroll_type='start_of_the_turn_reroll')
        self.gold = min(2 + 1 * self.turn_number, 10)
        print(f'-------------------------Player {self.player_name} turn-------------------------')
        print(self.tavern_info())
        print(self.player_hand_info())
        print(self.player_board_info())
        print(f'Players gold: {self.gold}, players hp: {self.player_hp}, players tavern level: {self.level}')
        action_number = -99
        while action_number != 6:
            print('Print action number: 1 - buy a minion, 2 - play a card, 3 - sell a minion, 4 - reroll, 5 - show stats, 6 - end the turn')
            action_number = int(input())
            if action_number == 1:
                print(self.tavern_info())
                print('Choose minion position. Starting from 0. Can use negatives')
                position = int(input())
                self.buy(position)
            elif action_number == 2:
                print(self.player_hand_info())
                print('Choose card position. Starting from 0. Can use negatives')
                position = int(input())
                self.play_card(position)
            elif action_number == 3:
                print(self.player_board_info())
                print('Choose minion position. Starting from 0. Can use negatives')
                position = int(input())
                self.sell(position)
            elif action_number == 4:
                self.reroll()
                print(self.tavern_info())
            elif action_number == 5:
                print(self.tavern_info())
                print(self.player_hand_info())
                print(self.player_board_info())
                print(f'Players gold: {self.gold}, players hp: {self.player_hp}, players tavern level: {self.level}')
            elif action_number == 6:
                pass
            else:
                print('Wrong number')
        self.turn_number += 1
