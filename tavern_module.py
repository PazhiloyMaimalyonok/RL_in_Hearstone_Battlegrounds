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
        self.gold = 10
        self.player_hp = 30
        self.turn_number = 1
        self.level = 1
        self.minions_per_reroll = 3
        self.max_player_board_size = 7
        self.event_manager = self.game.event_manager

    def get_object(self):
        return self

    def change_player_hp_during_turn(self, amount):
        self.player_hp += amount

    def buy(self, position):
        if position > len(self.tavern_board) - 1 or position < 0:
            return {'error': 'Card index out of tavern_board range'}
        elif self.gold < 3:
            return {'error': 'Not enough gold'}
        elif len(self.player_hand) >= 10:
            return {'error': 'Player hand is full'}
        else:
            self.gold -= 3
            bought_card = self.tavern_board.pop(position)
            self.player_hand.append(bought_card)
            return {'action': 'buy', 'card': bought_card.card_info()}

    def play_card(self, position):
        if position > len(self.player_hand) - 1 or position < 0:
            return {'error': 'Card index out of player_hand range'}
        elif len(self.player_board) >= self.max_player_board_size:
            return {'error': 'Player board is full'}
        else:
            card = self.player_hand.pop(position)
            self.player_board.append(card)
            card.enter_board(self.event_manager, self)

            # Trigger BattlecryMechanic directly if present
            for mechanic in card.mechanics_list:
                if isinstance(mechanic, BattlecryMechanic):
                    mechanic.trigger()
            played_card = card
            self.event_manager.emit(GameEvent(EventType.CARD_PLAYED, payload=played_card))
            return {'action': 'play_card', 'card': card.card_info()}

    def sell(self, position):
        if position > len(self.player_board) - 1 or position < 0:
            return {'error': 'Card index out of player_board range'}
        else:
            self.gold += 1
            card_to_sell = self.player_board.pop(position)
            card_to_sell.leave_board()
            self.game.card_return_to_pool(card_to_sell)
            return {'action': 'sell', 'card': card_to_sell.card_info()}

    def eat_minion(self, minion):
        if minion in self.tavern_board:
            self.tavern_board.remove(minion)
            self.game.card_return_to_pool(minion)
        else:
            pass  # Minion not in tavern board

    def reroll(self, reroll_type='usual'):
        if self.gold < 1 and reroll_type == 'usual':
            return {'error': 'Not enough gold'}
        else:
            if reroll_type == 'usual':
                self.gold -= 1

            while self.tavern_board:
                minion = self.tavern_board.pop()
                self.game.card_return_to_pool(minion)

            for _ in range(self.minions_per_reroll):
                new_minion = self.game.card_draw()
                self.tavern_board.append(new_minion)
            return {'action': 'reroll', 'tavern_board': [minion.card_info() for minion in self.tavern_board]}

    def start_of_turn(self):
        self.reroll(reroll_type='start_of_the_turn_reroll')
        self.gold = min(2 + 1 * self.turn_number, 10)
    
    def player_turn(self, action_list=None):
        if action_list is None:
            action_list = []
        self.reroll(reroll_type='start_of_the_turn_reroll')
        self.gold = min(2 + 1 * self.turn_number, 10)
        turn_log = []
        for action in action_list:
            action_number = action.get('action_type')
            position = action.get('position', None)
            if action_number == 1:
                result = self.buy(position)
                turn_log.append(result)
            elif action_number == 2:
                result = self.play_card(position)
                turn_log.append(result)
            elif action_number == 3:
                result = self.sell(position)
                turn_log.append(result)
            elif action_number == 4:
                result = self.reroll()
                turn_log.append(result)
            elif action_number == 5:
                pass  # Show stats can be handled by the interface
            elif action_number == 6:
                break  # End the turn
            else:
                turn_log.append({'error': 'Invalid action number'})
        self.turn_number += 1
        return turn_log
