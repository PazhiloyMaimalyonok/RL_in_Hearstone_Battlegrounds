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
