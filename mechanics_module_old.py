
# Видимо нужны:
#     update_board() для таверны
#     Card().call_mechanics() -- во время апдейта таверны прохожиться по всем картам и "звать механику"
#     Добавить кэш разыгранной карты в play_card, чтобы при update_board() и/или call_mechanics() было понятно, от какой карты првоерять эффект
#     У каждой карты есть список механик: врожденных и приобритенных. По каждому их них проходимся и они возвращают либо изменение, либо ничего
import random 

class Mechanics:
    """Описание
    Что сейчас класс собой представляет
        --
    Что хочу от класса
        Класс механик -- это как карты на столе, реагируют на разыгранную карту. Вот эту идея возможно поменяю в будущем
        Будет родительский класс Mechanics и много детей. Каждая механика -- это отдельный ребенок.
    Мысли по улучшению
        Отедльно подумать над механиками для покупки карт
    """
    def __init__(self, card, played_card, tavern = None):
        self.card = card # Нужна для того, чтобы отправить запрос на бафф карты
        self.played_card = played_card # Нужна для того, чтобы понять, будет баф или нет. Например, если у меня красненький 1/4, то его не надо бафать, если разыграли мурлока
            # Но надо бафать, если разыграли демона
        self.hp_buff = 0
        self.attack_buff = 0
        self.tavern = tavern # для 1/4 красненького, чтобы хп коцал
    
    def calculate_buffs(self):
        # Расчитываю, какие бафы должна получить карта/таверна
        raise NotImplementedError("Subclass must implement trigger method")
    
    def choose_buff_targets(self):
        # Выбираю цели, которых буду бафать
        raise NotImplementedError("Subclass must implement trigger method")
    
    def trigger(self):
        # # Вызываю бафы. Метод вызывается, чтобы просчитать бафы и забафать карту.
        # # Вероятно это будет реализовано в этом(общем) классе
        # ## Рассчитываю баффы
        # self.calculate_buffs()
        # # Выбираю цели для бафа
        # for minion_to_buff in self.choose_buff_targets(): 
        #     ## Реализую бафы
        #     minion_to_buff.buff_card(self.hp_buff, 'hp')
        #     minion_to_buff.buff_card(self.attack_buff, 'attack') # Могу ли я использовать сел.данные из подкласса
        """Execute the mechanic's effect."""
        raise NotImplementedError("Subclass must implement the trigger method.")
    
class PlayedCardBuffMechanic(Mechanics):
    """Описание
    Что сейчас класс собой представляет
        --
    Что хочу от класса
        Класс, который расчитывает бафы для карты в зависимости от разыгранной карты. А так же коллит карту забафаться.
        Вероятно, сейчас закину сюда несколько похожих механик через if. Потом их либо разнесу по классам, либо еще че придумаю
    Мысли по улучшению
        Дублируются условия применения баффов в calculate_buffs и в choose_buff_targets
        Нужно добавить тип баффа (для красненького отдельный, для мэрлока отдельный)
        
    """
    def __init__(self, card, played_card, tavern):
        super().__init__(card, played_card, tavern) 
        
    def should_trigger(self):
        result = False
        if self.card != self.played_card:
            # Бафает себя при розыгрыше карты
            if self.card.card_name in ['Wrath_Weaver'] and self.played_card.klass == 'Demon':
                result = True
            elif self.card.card_name in ['Molten_Rock', 'Party_Elemental'] and self.played_card.klass == 'Elemental':
                result = True
            elif self.card.card_name in ['Swampstriker', 'Saltscale_Honcho'] and self.played_card.klass == 'Murloc':
                result = True
            elif self.card.card_name in ['Blazing_Skyfin'] and BattlecryMechanic in self.played_card.mechanics_list:
                result = True
        return result  # Placeholder
        
    def trigger(self):
        if self.should_trigger():
            ## Рассчитываю баффы
            self.calculate_buffs()
            # Выбираю цели для бафа
            for minion_to_buff in self.choose_buff_targets(): 
                ## Реализую бафы
                minion_to_buff.buff_card(self.hp_buff, 'hp')
                minion_to_buff.buff_card(self.attack_buff, 'attack') # Могу ли я использовать сел.данные из подкласса
        
    def choose_buff_targets(self) -> list:
        # ПО умолчанию всегда бафает себя
        buff_targets_list = [self.card]
        # Выбираю цели, которых буду бафать
        if self.card.card_name in ['Party_Elemental']:
            buff_candidates = []
            for minion in self.tavern.player_board:
                #второе условие, что в список карт под бафф не попадет только что разыгранная карта
                if minion.klass == 'Elemental' and minion != self.played_card: 
                    buff_candidates.append(minion)
            # По идее в buff_candidates всегда есть хотя бы одна карта - сам чел с механикой
            buff_targets_list = [buff_candidates[random.randint(0, len(buff_candidates) - 1)]]
        elif self.card.card_name in ['Saltscale_Honcho']:
            buff_candidates = []
            for minion in self.tavern.player_board:
                #второе условие, что в список карт под бафф не попадет только что разыгранная карта
                if minion.klass == 'Murloc' and minion != self.played_card: 
                    buff_candidates.append(minion)
            # По идее в buff_candidates всегда есть хотя бы одна карта - сам чел с механикой
            buff_targets_list = [buff_candidates[random.randint(0, len(buff_candidates) - 1)]]
        return buff_targets_list
        
    def calculate_buffs(self):
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
        
class BattlecryMechanic(Mechanics):
    """Описание
    Что сейчас класс собой представляет
        --
    Что хочу от класса
        Класс, реализующий механику батлкраев
    Мысли по улучшению
        --
    """
    def __init__(self, card, played_card, tavern):
        super().__init__(card, played_card, tavern) 
        
    def should_trigger(self):
        result = False
        if self.card == self.played_card:
            if self.played_card.card_name in ['Coldlight_Seer', 'Backstage_Security']:
                result = True
            elif self.card.card_name in ['Picky_Eater']:
                if self.tavern.tavern_board != []:
                    result = True
            elif self.card.card_name in ['Mind_Muck']:
                if self.tavern.tavern_board != []:
                    # Условие, что на столе есть демоны помимо 3/2 Mind_Muck, которых можно забафать
                    buff_targets_list = []
                    for minion in self.tavern.player_board:
                        if minion.klass == 'Demon' and minion != self.card:
                            buff_targets_list.append(minion)
                    if buff_targets_list != []:
                        result = True
        return result  # Placeholder
        
    def trigger(self):
        if self.should_trigger():
            ## Рассчитываю баффы
            self.calculate_buffs()
            # Выбираю цели для бафа
            for minion_to_buff in self.choose_buff_targets(): 
                ## Реализую бафы
                minion_to_buff.buff_card(self.hp_buff, 'hp')
                minion_to_buff.buff_card(self.attack_buff, 'attack') # Могу ли я использовать сел.данные из подкласса
            self.trigger_change_tavern()
        
    def choose_buff_targets(self) -> list:
        # Выбираю цели, которых буду бафать
        buff_targets_list = []
        if self.played_card.card_name == 'Coldlight_Seer':
            for minion in self.tavern.player_board:
                if minion.klass == 'Murloc' and minion != self.card:
                    buff_targets_list.append(minion)
        elif self.played_card.card_name == 'Picky_Eater':
            buff_targets_list = [self.card]
        elif self.played_card.card_name == 'Mind_Muck':
            possible_target_list = []
            for minion in self.tavern.player_board:
                if minion.klass == 'Demon' and minion != self.card:
                    possible_target_list.append(minion)
            # лишний if
            if possible_target_list != []:
                print(self.tavern.player_board_info(possible_target_list))
                print(f'Choose minions position. Starting from 0. Can use negatives')
                minion_to_buff_position = int(input())
                buff_targets_list = [possible_target_list[minion_to_buff_position]]
        return buff_targets_list
        
    def calculate_buffs(self):
        if self.played_card.card_name in ['Coldlight_Seer']:
            self.attack_buff += 0
            self.hp_buff += 2
        elif self.card.card_name in ['Picky_Eater']:
            minion_to_eat = self.tavern.tavern_board[random.randint(0, len(self.tavern.tavern_board) - 1)]
            self.attack_buff += minion_to_eat.attack
            self.hp_buff += minion_to_eat.hp
            self.tavern.eat_minion(minion_to_eat)
        elif self.card.card_name in ['Mind_Muck']:
            buff_targets_list = []
            for minion in self.tavern.player_board:
                if minion.klass == 'Demon' and minion != self.card:
                    buff_targets_list.append(minion)
            # лишний if
            if buff_targets_list != []:
                minion_to_eat = self.tavern.tavern_board[random.randint(0, len(self.tavern.tavern_board) - 1)]
                self.attack_buff += minion_to_eat.attack
                self.hp_buff += minion_to_eat.hp
                self.tavern.eat_minion(minion_to_eat)
        else:
            pass
        
    def trigger_change_tavern(self):
        """В этом методе реализуются различные тригеры, связанные с изменением таверны"""
        if self.played_card.card_name == 'Backstage_Security':
            # Поменять потом это на метод внутри таверны, который уменьшает хп на 1
            self.tavern.change_player_hp_during_turn(amount = -1)

# class SoldCardMechanic(Mechanics):
#     """Описание
#         Нужно добавить событие продажи карты, после которой эта механика будет работать
#     """
#     def __init__(self, card, played_card, tavern):
#         super().__init__(card, played_card, tavern) 
     
#     # # ПОка это не надо   
#     # def should_trigger(self):
#     #     result = False
#     #     # Бафает себя при розыгрыше карты
#     #     if self.card.card_name == 'Sellemental':
#     #         result = True
#     #     return result  # Placeholder
#     def trigger(self):
#         if self.card.card_name == 'Sellemental':
#             self.tavern.add_card_to_player_hand('Water_Droplet')