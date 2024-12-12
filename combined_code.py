
# ------- card_module.py -------

from mechanics_module import *
import pandas as pd
from events_system_module import EventType, EventManager

class Card:
    cards_data = pd.read_excel('cards_data.xlsx')
    cards_data = cards_data[(cards_data['use_flg'] == 1)]

    def __init__(self, card_name):
        cards_data = Card.cards_data
        cards_data = cards_data[cards_data['card_name'] == card_name]
        if cards_data.shape[0] == 0:
            raise ValueError("No such card yet")
        elif cards_data.shape[0] > 1:
            raise ValueError("Multiple cards with the same name")
        for index, row in cards_data.iterrows():
            self.card_name = row['card_name']
            self.type = row['type']
            self.tavern_level = int(row['tavern_level'])

        self.event_subscribed = []
        self.mechanics_list = []
        self.tavern = None

    def subscribe_mechanics(self, event_manager):
        for mechanic in self.mechanics_list:
            mechanic.subscribe(event_manager)

    def unsubscribe_mechanics(self):
        for mechanic in self.mechanics_list:
            mechanic.unsubscribe_all()

    def enter_board(self, event_manager, tavern):
        self.tavern = tavern
        self.subscribe_mechanics(event_manager)

    def leave_board(self):
        self.unsubscribe_mechanics()
        self.tavern = None

    def card_info(self):
        raise NotImplementedError("Subclass must implement the card_info method.")

class MinionCard(Card):
    minions_from_pool_mask = (Card.cards_data['type'] == 'Minion') & (Card.cards_data['sold_at_tavern'] == 1)
    minions_list = list(Card.cards_data[minions_from_pool_mask]['card_name'].values)

    def __init__(self, card_name):
        super().__init__(card_name)
        cards_data = Card.cards_data[Card.cards_data['type'] == 'Minion']
        cards_data = cards_data[cards_data['card_name'] == card_name]
        if cards_data.shape[0] == 0:
            raise ValueError("No such minion yet")
        elif cards_data.shape[0] > 1:
            raise ValueError("Multiple cards with the same name")
        for index, row in cards_data.iterrows():
            self.card_name = row['card_name']
            self.attack = int(row['attack'])
            self.hp = int(row['hp'])
            self.type = row['type']
            self.klass = row['klass']
            self.tavern_level = int(row['tavern_level'])
            self.card_amount = int(row['card_amount'])
            if pd.notna(row['mechanics_list']):
                self.mechanics_list = [eval(mechanics)(self) for mechanics in row['mechanics_list'].split(',')]
            else:
                self.mechanics_list = []

    def card_info(self):
        return f'Card name: {self.card_name}, card attack: {self.attack}, card hp {self.hp}'

    def buff_card(self, buff_value, buff_type):
        allowed_buff_types = {'hp', 'attack'}
        if buff_type not in allowed_buff_types:
            raise ValueError("Invalid buff type. Must be one of: {}".format(allowed_buff_types))

        original_attack = self.attack
        original_hp = self.hp

        if buff_type == 'hp':
            self.hp += buff_value
        elif buff_type == 'attack':
            self.attack += buff_value

        # Instead of printing, we return the before and after stats
        buff_info = {
            'card_name': self.card_name,
            'original_attack': original_attack,
            'original_hp': original_hp,
            'new_attack': self.attack,
            'new_hp': self.hp
        }
        return buff_info

class SpellCard(Card):
    def __init__(self, card_name):
        super().__init__(card_name)
        cards_data = Card.cards_data[Card.cards_data['type'] == 'Spell']
        cards_data = cards_data[cards_data['card_name'] == card_name]
        if cards_data.shape[0] == 0:
            raise ValueError("No such spell yet")
        elif cards_data.shape[0] > 1:
            raise ValueError("Multiple cards with the same name")
        for index, row in cards_data.iterrows():
            self.card_name = row['card_name']
            self.tavern_level = int(row['tavern_level'])
            self.card_amount = int(row['card_amount'])
            if pd.notna(row['spell_effect_list']):
                self.spell_effect_list = [eval(mechanics) for mechanics in row['spell_effect_list'].split(',')]
            else:
                self.spell_effect_list = []

    def card_info(self):
        info = super().card_info()
        return f'{info}, Effect: {self.effect}'

    def trigger(self, played_card, tavern=None):
        for mechanic in self.spell_effect_list:
            mechanic(card=self, played_card=played_card, tavern=tavern).trigger()

# ------- fight_module.py -------

import copy
import random
import numpy as np

class Fight:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_board = [copy.deepcopy(minion) for minion in first_player.player_board]
        self.second_player_board = [copy.deepcopy(minion) for minion in second_player.player_board]
        self.first_player_attacking_order = self.first_player_board.copy()
        self.second_player_attacking_order = self.second_player_board.copy()
        self.fight_log = []  # Collect fight events for logging or display

    def simulate(self):
        len_first_board = len(self.first_player_board)
        len_second_board = len(self.second_player_board)
        if len_first_board == len_second_board:
            counter = random.randint(0, 1)
        else:
            counter = np.argmax([len_first_board, len_second_board])
        while self.first_player_board and self.second_player_board:
            if counter % 2 == 0:
                self.attack(self.first_player_attacking_order, self.second_player_board)
            else:
                self.attack(self.second_player_attacking_order, self.first_player_board)
            counter += 1
        return self.determine_winner()

    def attack(self, attacking_order, defending_board):
        if not attacking_order or not defending_board:
            return
        attacking_minion = attacking_order.pop(0)
        defending_minion = random.choice(defending_board)

        # Collect attack event data
        attack_event = {
            'attacking_minion': attacking_minion.card_info(),
            'defending_minion': defending_minion.card_info(),
        }
        self.resolve_attack(attacking_minion, defending_minion)

        # Update attack event with post-attack stats
        attack_event.update({
            'attacking_minion_after': attacking_minion.card_info(),
            'defending_minion_after': defending_minion.card_info(),
        })
        self.fight_log.append(attack_event)

        if attacking_minion.hp > 0:
            attacking_order.append(attacking_minion)

    def resolve_attack(self, attacking_minion, defending_minion):
        attacking_minion.hp -= defending_minion.attack
        defending_minion.hp -= attacking_minion.attack

        if attacking_minion.hp <= 0:
            self.remove_minion(attacking_minion)
        if defending_minion.hp <= 0:
            self.remove_minion(defending_minion)

    def remove_minion(self, minion):
        if minion in self.first_player_board:
            self.first_player_board.remove(minion)
        elif minion in self.second_player_board:
            self.second_player_board.remove(minion)

    def determine_winner(self):
        result = {}
        if self.first_player_board and not self.second_player_board:
            result['winner'] = self.first_player.player_name
            result['loser'] = self.second_player.player_name
            damage = sum([minion.tavern_level for minion in self.first_player_board]) + self.first_player.level
            result['damage'] = damage
            return 0, damage, result
        elif self.second_player_board and not self.first_player_board:
            result['winner'] = self.second_player.player_name
            result['loser'] = self.first_player.player_name
            damage = sum([minion.tavern_level for minion in self.second_player_board]) + self.second_player.level
            result['damage'] = damage
            return 1, damage, result
        else:
            result['tie'] = True
            return -1, 0, result

# ------- game_module.py -------

from cards_pool_module import CardsPool
from tavern_module import Tavern
from fight_module import Fight
from events_system_module import EventManager
import random

class Game:
    def __init__(self, players_number=2):
        self.event_manager = EventManager()
        self.players_number = players_number
        self.cards_pool = CardsPool()
        self.players_taverns = []
        self.turn_number = 1  # Added to keep track of turns

    def create_players_taverns(self, player_names=None):
        if player_names:
            players_names = player_names
        else:
            players_names = [f"Player{i+1}" for i in range(self.players_number)]
        self.players_taverns = [Tavern(self, player_name=name) for name in players_names]
        return self.players_taverns

    def card_draw(self):
        return self.cards_pool.card_draw()

    def card_return_to_pool(self, card):
        self.cards_pool.card_return_to_pool(card)

    def play_round(self):
        round_log = []
        for player in self.players_taverns:
            player.player_turn()
        fighting_list = list(self.players_taverns)
        while len(fighting_list) > 1:
            fighter1, fighter2 = random.sample(fighting_list, 2)
            fighting_list.remove(fighter1)
            fighting_list.remove(fighter2)
            fight = Fight(fighter1, fighter2)
            player_won, damage_dealt, fight_result = fight.simulate()
            round_log.append(fight_result)
            if player_won == -1:
                pass
            elif player_won == 0:
                fighter2.player_hp -= damage_dealt
            elif player_won == 1:
                fighter1.player_hp -= damage_dealt
            else:
                pass
        self.players_taverns = [player for player in self.players_taverns if player.player_hp > 0]
        self.turn_number += 1
        return round_log

    def declare_winner(self):
        if self.players_taverns:
            winner = self.players_taverns[0].player_name
            return winner
        return None

    def play_game(self, player_names=None):
        self.create_players_taverns(player_names)
        game_log = []
        while len(self.players_taverns) > 1:
            round_log = self.play_round()
            game_log.append(round_log)
        winner = self.declare_winner()
        return winner, game_log

    def reset(self):
        self.cards_pool = CardsPool()
        self.event_manager = EventManager()
        self.players_taverns = []
        self.turn_number = 1

# ------- tavern_module.py -------

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

# ------- mechanics_module.py -------

import random
from events_system_module import EventType, GameEvent, EventManager

class Mechanic:
    def __init__(self, card):
        self.card = card

    def subscribe(self, event_manager):
        pass

    def unsubscribe_all(self):
        pass

class PlayedCardBuffMechanic(Mechanic):
    def __init__(self, card):
        super().__init__(card)
        self.event_subscribed = []
        self.event_manager = None

    def get_event_types(self):
        return [EventType.CARD_PLAYED]

    def subscribe(self, event_manager):
        self.event_manager = event_manager
        event_type = EventType.CARD_PLAYED
        if event_type not in self.event_subscribed:
            event_manager.subscribe(event_type, self.trigger)
            self.event_subscribed.append(event_type)

    def unsubscribe_all(self):
        if self.event_manager:
            for event_type in self.event_subscribed[:]:
                self.event_manager.unsubscribe(event_type, self.trigger)
                self.event_subscribed.remove(event_type)
            if not self.event_subscribed:
                self.event_manager = None

    def should_trigger(self, played_card):
        result = False
        if self.card != played_card:
            if self.card.card_name in ['Wrath_Weaver'] and played_card.klass == 'Demon':
                result = True
            elif self.card.card_name in ['Molten_Rock', 'Party_Elemental'] and played_card.klass == 'Elemental':
                result = True
            elif self.card.card_name in ['Swampstriker', 'Saltscale_Honcho'] and played_card.klass == 'Murloc':
                result = True
            elif self.card.card_name in ['Blazing_Skyfin'] and any(isinstance(m, BattlecryMechanic) for m in played_card.mechanics_list):
                result = True
        return result

    def trigger(self, event):
        played_card = event.payload
        if self.should_trigger(played_card):
            self.calculate_buffs()
            for minion_to_buff in self.choose_buff_targets():
                buff_info_hp = minion_to_buff.buff_card(self.hp_buff, 'hp')
                buff_info_attack = minion_to_buff.buff_card(self.attack_buff, 'attack')
                # You can collect buff_info_hp and buff_info_attack if needed

    def calculate_buffs(self):
        self.attack_buff = 0
        self.hp_buff = 0

        if self.card.card_name in ['Wrath_Weaver']:
            self.attack_buff += 2
            self.hp_buff += 1
        elif self.card.card_name in ['Molten_Rock']:
            self.attack_buff += 0
            self.hp_buff += 1
        elif self.card.card_name in ['Swampstriker']:
            self.attack_buff += 1
            self.hp_buff += 0
        elif self.card.card_name in ['Blazing_Skyfin']:
            self.attack_buff += 1
            self.hp_buff += 1
        elif self.card.card_name in ['Party_Elemental']:
            self.attack_buff += 2
            self.hp_buff += 1
        elif self.card.card_name in ['Saltscale_Honcho']:
            self.attack_buff += 0
            self.hp_buff += 1
        else:
            pass

    def choose_buff_targets(self) -> list:
        tavern = self.card.tavern
        buff_targets_list = [self.card]
        if self.card.card_name in ['Party_Elemental']:
            buff_candidates = [minion for minion in tavern.player_board if minion.klass == 'Elemental' and minion != self.card]
            if buff_candidates:
                buff_targets_list = [random.choice(buff_candidates)]
        elif self.card.card_name in ['Saltscale_Honcho']:
            buff_candidates = [minion for minion in tavern.player_board if minion.klass == 'Murloc' and minion != self.card]
            if buff_candidates:
                buff_targets_list = [random.choice(buff_candidates)]
        return buff_targets_list

class BattlecryMechanic(Mechanic):
    def __init__(self, card):
        super().__init__(card)
        self.event_subscribed = []

    def trigger(self):
        self.calculate_buffs()
        for minion_to_buff in self.choose_buff_targets():
            buff_info_hp = minion_to_buff.buff_card(self.hp_buff, 'hp')
            buff_info_attack = minion_to_buff.buff_card(self.attack_buff, 'attack')
            # Collect buff_info_hp and buff_info_attack if needed
        self.trigger_change_tavern()

    def calculate_buffs(self):
        self.attack_buff = 0
        self.hp_buff = 0

        if self.card.card_name in ['Coldlight_Seer']:
            self.attack_buff += 0
            self.hp_buff += 2
        elif self.card.card_name in ['Picky_Eater']:
            tavern = self.card.tavern
            if tavern.tavern_board:
                minion_to_eat = random.choice(tavern.tavern_board)
                self.attack_buff += minion_to_eat.attack
                self.hp_buff += minion_to_eat.hp
                tavern.eat_minion(minion_to_eat)
        elif self.card.card_name in ['Mind_Muck']:
            tavern = self.card.tavern
            buff_targets_list = [minion for minion in tavern.player_board if minion.klass == 'Demon' and minion != self.card]
            if buff_targets_list and tavern.tavern_board:
                minion_to_eat = random.choice(tavern.tavern_board)
                self.attack_buff += minion_to_eat.attack
                self.hp_buff += minion_to_eat.hp
                tavern.eat_minion(minion_to_eat)

    def choose_buff_targets(self) -> list:
        tavern = self.card.tavern
        buff_targets_list = []
        if self.card.card_name == 'Coldlight_Seer':
            buff_targets_list = [minion for minion in tavern.player_board if minion.klass == 'Murloc' and minion != self.card]
        elif self.card.card_name == 'Picky_Eater':
            buff_targets_list = [self.card]
        elif self.card.card_name == 'Mind_Muck':
            buff_targets_list = [minion for minion in tavern.player_board if minion.klass == 'Demon' and minion != self.card]
            # Selection logic can be implemented in the interface
        return buff_targets_list

    def trigger_change_tavern(self):
        if self.card.card_name == 'Backstage_Security':
            tavern = self.card.tavern
            tavern.change_player_hp_during_turn(amount=-1)

# ------- events_system_module.py -------

class GameEvent:
    def __init__(self, event_type, payload=None):
        self.event_type = event_type
        self.payload = payload

class EventType:
    CARD_PLAYED = "CardPlayed"
    CARD_SOLD = "CardSold"
    TURN_START = "TurnStart"
    TURN_END = "TurnEnd"

class EventManager:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self.subscribers and callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)

    def emit(self, event):
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                callback(event)




# ------- command_line_interface_module.py -------

def get_player_action_cli():
    print('Choose an action number:')
    print('1 - Buy a minion')
    print('2 - Play a card')
    print('3 - Sell a minion')
    print('4 - Reroll')
    print('5 - Show stats')
    print('6 - End the turn')

    while True:
        try:
            action_number = int(input())
            if action_number in [1, 2, 3, 4, 5, 6]:
                break
            else:
                print("Invalid choice. Try again:")
        except ValueError:
            print("Please enter a valid integer for the action number.")

    position = None
    if action_number in [1, 2, 3]:  # Actions that require a position
        print('Enter the position (starting from 0):')
        while True:
            try:
                position = int(input())
                break
            except ValueError:
                print("Please enter a valid integer for position.")

    return {'action_type': action_number, 'position': position}


def display_tavern_info(tavern):
    tavern_board_info = [minion.card_info() for minion in tavern.tavern_board]
    print(f'Tavern board: {tavern_board_info}')


def display_player_hand(tavern):
    hand_info = [card.card_info() for card in tavern.player_hand]
    print(f'Player hand: {hand_info}')


def display_player_board(tavern):
    board_info = [card.card_info() for card in tavern.player_board]
    print(f'Player board: {board_info}')


def display_player_stats(tavern):
    print(f'Player gold: {tavern.gold}, HP: {tavern.player_hp}, Tavern level: {tavern.level}')


def display_turn_log(turn_log):
    for i, entry in enumerate(turn_log, start=1):
        if 'error' in entry:
            print(f"{i}. Error: {entry['error']}")
        else:
            action = entry.get('action', 'No action')
            card = entry.get('card', 'No card')
            print(f"{i}. {action.capitalize()} - {card}")

# ------- main_cli.py -------

from game_module import Game
from command_line_interface_module import (
    get_player_action_cli,
    display_tavern_info,
    display_player_hand,
    display_player_board,
    display_player_stats,
    display_turn_log
)

def main():
    game = Game()
    player_names = ['Player1', 'Player2']  # You can customize player names here.
    game.create_players_taverns(player_names)

    while len(game.players_taverns) > 1:
        # Each player takes a turn
        for tavern in game.players_taverns:
            # Handle start-of-turn logic (reroll, set gold, etc.)
            tavern.start_of_turn()

            # Display the state after start_of_turn()
            print(f"------------------------- {tavern.player_name}'s turn -------------------------")
            display_tavern_info(tavern)
            display_player_hand(tavern)
            display_player_board(tavern)
            display_player_stats(tavern)

            # Collect actions from the player until they choose to end the turn
            action_list = []
            while True:
                action = get_player_action_cli()
                action_type = action['action_type']

                if action_type == 6:
                    # End turn
                    break
                elif action_type == 5:
                    # Show stats again (no change to state, just re-display)
                    display_tavern_info(tavern)
                    display_player_hand(tavern)
                    display_player_board(tavern)
                    display_player_stats(tavern)
                else:
                    # These actions modify the state and should be recorded
                    action_list.append(action)

            # Execute all actions chosen by the player
            turn_log = tavern.player_turn(action_list)
            
            # Print detailed results of each action
            for entry in turn_log:
                if 'error' in entry:
                    print(f"Error: {entry['error']}")
                else:
                    if entry.get('action') == 'buy':
                        print(f"You bought a minion: {entry['card']}")
                    elif entry.get('action') == 'play_card':
                        print(f"You played a card: {entry['card']}")
                    elif entry.get('action') == 'sell':
                        print(f"You sold a minion: {entry['card']}")
                    elif entry.get('action') == 'reroll':
                        print("You rerolled the tavern board!")
                        print("New Tavern Board:")
                        for minion_info in entry.get('tavern_board', []):
                            print(minion_info)

            # Display a summary of all actions taken this turn
            print("Actions taken this turn:")
            display_turn_log(turn_log)

        # After all players have completed their turns, simulate the fight phase
        round_log = game.play_round()
        # Print results of the fights
        for fight_result in round_log:
            if 'tie' in fight_result:
                print("It's a tie this round!")
            else:
                print(f"{fight_result['winner']} defeated {fight_result['loser']} dealing {fight_result['damage']} damage!")

    # When only one player remains, declare the winner
    winner = game.declare_winner()
    print(f"The winner is {winner}")

if __name__ == "__main__":
    main()

# ------- main.py -------

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
# ------- cards_pool_module.py -------

import random
from card_module import *

class CardsPool:
    def __init__(self):
        self.cards_pool = []
        for card_name in MinionCard.minions_list:
            for card_number in range(MinionCard(card_name).card_amount):
                self.cards_pool.append(MinionCard(card_name))
        random.shuffle(self.cards_pool)

    def card_draw(self) -> MinionCard:
        if self.cards_pool:
            index = random.randrange(len(self.cards_pool))
            return self.cards_pool.pop(index)
        else:
            raise Exception("No cards left in the pool")

    def card_return_to_pool(self, card: MinionCard):
        if card.card_name in MinionCard.minions_list:
            original_card = MinionCard(card.card_name)
            self.cards_pool.append(original_card)
