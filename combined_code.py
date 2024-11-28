
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
        for index, row in cards_data.iterrows():  # Iterate over a single row
            self.card_name = row['card_name']
            self.type = row['type']
            self.tavern_level = int(row['tavern_level'])

        self.event_subscribed = []  # Track events the card is subscribed to
        self.mechanics_list = []
        self.tavern = None  # Reference to the tavern

    def subscribe_mechanics(self, event_manager):
        for mechanic in self.mechanics_list:
            for event_type in mechanic.get_event_types():
                mechanic.subscribe(event_manager, event_type)
                if event_type not in self.event_subscribed:
                    self.event_subscribed.append(event_type)
                    print(f"{self.card_name} subscribed to {event_type}")

    def unsubscribe_mechanics(self):
        for mechanic in self.mechanics_list:
            for event_type in mechanic.event_subscribed[:]:  # Copy the list to avoid modification during iteration
                mechanic.unsubscribe(event_type)
                if event_type in self.event_subscribed:
                    self.event_subscribed.remove(event_type)
                    print(f"{self.card_name} unsubscribed from {event_type}")

    def enter_board(self, event_manager, tavern):
        self.tavern = tavern  # Set the tavern reference
        self.subscribe_mechanics(event_manager)

    def leave_board(self):
        self.unsubscribe_mechanics()
        self.tavern = None  # Clear the tavern reference

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
                # Instantiate mechanics with reference to this card
                self.mechanics_list = [eval(mechanics)(self) for mechanics in row['mechanics_list'].split(',')]
            else:
                self.mechanics_list = []

    def card_info(self):
        return f'Card name: {self.card_name}, card attack: {self.attack}, card hp {self.hp}'

    def buff_card(self, buff_value, buff_type):
        allowed_buff_types = {'hp', 'attack'}
        if buff_type not in allowed_buff_types:
            raise ValueError("Invalid buff type. Must be one of: {}".format(allowed_buff_types))

        print(f'Card: {self.card_name}, original attack: {self.attack}, original hp: {self.hp}')
        if buff_type == 'hp':
            self.hp += buff_value
        elif buff_type == 'attack':
            self.attack += buff_value
        print(f'Card: {self.card_name}, new attack: {self.attack}, new hp: {self.hp}')

    # Remove old subscribe/unsubscribe methods as they are handled in the base class

    def trigger(self, played_card):
        for mechanic in self.mechanics_list:
            mechanic.trigger(GameEvent(EventType.CARD_PLAYED, payload=played_card))

# SpellCard remains unchanged...


class SpellCard(Card):
    def __init__(self, card_name):
        super().__init__(card_name)
        cards_data = Card.cards_data[Card.cards_data['type'] == 'Spell']
        cards_data = cards_data[cards_data['card_name'] == card_name]
        if cards_data.shape[0] == 0:
            raise ValueError("No such spell yet")
        elif cards_data.shape[0] > 1:
            raise ValueError("Несколько карт с одинаковым названием")
        for index, row in cards_data.iterrows():  # итерируется по одной строке
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
        # Implement spell-specific mechanics if any
        for mechanic in self.spell_effect_list:
            mechanic(card=self, played_card=played_card, tavern=tavern).trigger()


# ------- fight_module.py -------

import copy
import random
import numpy as np

class Fight:
    """Описание
    Что сейчас класс собой представляет
        Класс отвечает за файт между двумя тавернами
    Что хочу от класса
        Хочу, чтобы правильно работал
        Надо подумать, как сюда добавить всякие интеракции
    Мысли по улучшению
        Как добавить механики типа секретов?
        Как добавить баффы, которые получает пользователь во время боя, а они сохраняются на всю жизнь
    Вопрос для МВП
        --
    """
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_board = [copy.deepcopy(minion) for minion in first_player.player_board]
        self.second_player_board = [copy.deepcopy(minion) for minion in second_player.player_board]
        self.first_player_attacking_order = self.first_player_board
        self.second_player_attacking_order = self.second_player_board

    def simulate(self):
        # Решаю, кто первый будет атаковая. Задача каунтера -- передавать инициативу атаки от одного другому
        len_first_board = len(self.first_player_board)
        len_second_board = len(self.second_player_board)
        if len_first_board == len_second_board:
            counter = random.randint(0, 1)
        else:
            counter = np.argmax([len_first_board, len_second_board])
        # Мб вынести определения, кто первый атакует или вообще определение кто в принципе атакует в отедльную функцию
        while self.first_player_board and self.second_player_board:
            if counter % 2 == 0:
                self.attack(self.first_player_attacking_order, self.second_player_board)
            else:
                self.attack(self.second_player_attacking_order, self.first_player_board)
            counter += 1

        return self.determine_winner()

    def attack(self, attacking_order, defending_board):
        attacking_minion = attacking_order.pop(0)
        defending_minion = random.choice(defending_board)

        print(f"Attacking minion: {attacking_minion.card_info()}")
        print(f"Defending minion: {defending_minion.card_info()}")

        self.resolve_attack(attacking_minion, defending_minion)

        print(f"Attacking minion stats after attack: {attacking_minion.card_info()}")
        print(f"Defending minion stats after attack: {defending_minion.card_info()}")

        # Добавляю существо в конец очереди атаки, если он не умер
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
            # self.first_player_attacking_order.remove(minion)
        elif minion in self.second_player_board:
            self.second_player_board.remove(minion)
            # self.second_player_attacking_order.remove(minion)

    def determine_winner(self):
        if self.first_player_board and not self.second_player_board:
            print(f"Player {self.first_player.player_name} wins!")
            return 0, sum([minion.tavern_level for minion in self.first_player_board]) + self.first_player.level
        elif self.second_player_board and not self.first_player_board:
            print(f"Player {self.second_player.player_name} wins!")
            return 1, sum([minion.tavern_level for minion in self.second_player_board]) + self.second_player.level
        else:
            print("It's a tie!")
            return -1, 0
# ------- game_module.py -------

from cards_pool_module import CardsPool
from tavern_module import Tavern
from fight_module import Fight
from events_system_module import EventManager
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
        self.event_manager = EventManager()
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
# ------- tavern_module.py -------

from card_module import MinionCard
from events_system_module import GameEvent, EventType

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
            played_card = card
            self.event_manager.emit(GameEvent(EventType.CARD_PLAYED, payload=played_card))
            card.enter_board(self.event_manager, self)  # Subscribe to events and set tavern reference
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
            for _ in range(len(self.tavern_board)):
                self.game.card_return_to_pool(self.tavern_board.pop())
            for _ in range(self.minions_per_reroll):
                self.tavern_board.append(self.game.card_draw())

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

# ------- mechanics_module.py -------


# Видимо нужны:
#     update_board() для таверны
#     Card().call_mechanics() -- во время апдейта таверны прохожиться по всем картам и "звать механику"
#     Добавить кэш разыгранной карты в play_card, чтобы при update_board() и/или call_mechanics() было понятно, от какой карты првоерять эффект
#     У каждой карты есть список механик: врожденных и приобритенных. По каждому их них проходимся и они возвращают либо изменение, либо ничего
import random
from events_system_module import EventType, GameEvent, EventManager

class PlayedCardBuffMechanic:
    """This class calculates buffs for a card depending on a played card."""
    def __init__(self, card):
        self.card = card
        self.event_subscribed = []
        self.event_manager = None  # Will be set when subscribing

    def get_event_types(self):
        return [EventType.CARD_PLAYED]

    def subscribe(self, event_manager, event_type):
        self.event_manager = event_manager  # Set the event manager
        if event_type not in self.event_subscribed:
            event_manager.subscribe(event_type, self.trigger)
            self.event_subscribed.append(event_type)
            print(f"{self.card.card_name}'s mechanic subscribed to {event_type}")

    def unsubscribe(self, event_type):
        if event_type in self.event_subscribed and self.event_manager:
            self.event_manager.unsubscribe(event_type, self.trigger)
            self.event_subscribed.remove(event_type)
            print(f"{self.card.card_name}'s mechanic unsubscribed from {event_type}")
            if not self.event_subscribed:
                self.event_manager = None  # Clear event manager when no events are subscribed

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
                minion_to_buff.buff_card(self.hp_buff, 'hp')
                minion_to_buff.buff_card(self.attack_buff, 'attack')

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
        tavern = self.card.tavern  # Reference to the tavern
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

class BattlecryMechanic:
    """This class implements battlecry mechanics."""
    def __init__(self, card):
        self.card = card
        self.event_subscribed = []
        self.event_manager = None  # Will be set when subscribing

    def get_event_types(self):
        return [EventType.CARD_PLAYED]

    def subscribe(self, event_manager, event_type):
        self.event_manager = event_manager
        if event_type not in self.event_subscribed:
            event_manager.subscribe(event_type, self.trigger)
            self.event_subscribed.append(event_type)
            print(f"{self.card.card_name}'s mechanic subscribed to {event_type}")

    def unsubscribe(self, event_type):
        if event_type in self.event_subscribed and self.event_manager:
            self.event_manager.unsubscribe(event_type, self.trigger)
            self.event_subscribed.remove(event_type)
            print(f"{self.card.card_name}'s mechanic unsubscribed from {event_type}")
            if not self.event_subscribed:
                self.event_manager = None

    def should_trigger(self, played_card):
        return self.card == played_card

    def trigger(self, event):
        played_card = event.payload
        if self.should_trigger(played_card):
            self.calculate_buffs()
            for minion_to_buff in self.choose_buff_targets():
                minion_to_buff.buff_card(self.hp_buff, 'hp')
                minion_to_buff.buff_card(self.attack_buff, 'attack')
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
            possible_target_list = [minion for minion in tavern.player_board if minion.klass == 'Demon' and minion != self.card]
            if possible_target_list:
                print('Possible targets:')
                for idx, minion in enumerate(possible_target_list):
                    print(f'{idx}: {minion.card_info()}')
                while True:
                    try:
                        choice = int(input('Choose minion position (starting from 0): '))
                        if 0 <= choice < len(possible_target_list):
                            buff_targets_list = [possible_target_list[choice]]
                            break
                        else:
                            print('Invalid choice. Try again.')
                    except ValueError:
                        print('Please enter a valid integer.')
            else:
                print('No valid targets to buff.')
                buff_targets_list = []
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
        """Unsubscribe a specific callback from an event."""
        if event_type in self.subscribers and callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)

    def emit(self, event):
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                callback(event)



# ------- cards_pool_module.py -------

import random
from card_module import *

class CardsPool:
    """Описание
    Что сейчас класс собой представляет
        Класс, который отвечает за создание пула карт для конкретной игры.
        Сейчас шафлит все карты. А что делать, если у юзера первая таверна, а в пуле есть карты второй таверны?
    Что хочу от класса
        --
    Мысли по улучшению
        Сейчас шафлит все карты. А что делать, если у юзера первая таверна, а в пуле есть карты второй таверны?
    Вопрос для МВП
        Что делать с доставанием карт из своей таверны? Это к классу Tavern?
    """
    def __init__(self):
        self.cards_pool = []
        for card_name in MinionCard.minions_list:
            for card_number in range(MinionCard(card_name).card_amount):
                self.cards_pool.append(MinionCard(card_name))
        random.shuffle(self.cards_pool)

    def card_draw(self) -> MinionCard:
        return self.cards_pool.pop()

    def card_return_to_pool(self, card: MinionCard):
        if card.card_name in MinionCard.minions_list:
            original_card = MinionCard(card.card_name)  # Create a new card instance with original stats
            self.cards_pool.append(original_card)        
# a = CardsPool()
# print([card.card_name for card in a.cards_pool])