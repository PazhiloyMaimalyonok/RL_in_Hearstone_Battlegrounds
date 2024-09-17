
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
    
    def trigger_buffs(self):
        # Вызываю бафы. Метод вызывается, чтобы просчитать бафы и забафать карту.
        # Вероятно это будет реализовано в этом(общем) классе
        ## Рассчитываю баффы
        self.calculate_buffs()
        # Выбираю цели для бафа
        for minion_to_buff in self.choose_buff_targets(): 
            ## Реализую бафы
            minion_to_buff.buff_card(self.hp_buff, 'hp')
            minion_to_buff.buff_card(self.attack_buff, 'attack') # Могу ли я использовать сел.данные из подкласса
    
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
        
    def choose_buff_targets(self) -> list:
        # ПО умолчанию всегда бафает себя
        buff_targets_list = [self.card]
        # Выбираю цели, которых буду бафать
        if self.card.card_name in ['Party_Elemental']:
            if self.played_card.klass == 'Elemental' and self.card != self.played_card:
                buff_candidates = []
                for minion in self.tavern.player_board:
                    #второе условие, что в список карт под бафф не попадет только что разыгранная карта
                    if minion.klass == 'Elemental' and minion != self.played_card: 
                        buff_candidates.append(minion)
                # По идее в buff_candidates всегда есть хотя бы одна карта - сам чел с механикой
                buff_targets_list = [buff_candidates[random.randint(0, len(buff_candidates) - 1)]]
        elif self.card.card_name in ['Saltscale_Honcho']:
            if self.played_card.klass == 'Murloc' and self.card != self.played_card:
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
            if self.played_card.klass == 'Demon':
                self.attack_buff += 2
                self.hp_buff += 1
        elif self.card.card_name in ['Molten_Rock']:
            if self.played_card.klass == 'Elemental' and self.card != self.played_card:
                self.attack_buff += 0
                self.hp_buff += 1
        elif self.card.card_name in ['Swampstriker']:
            if self.played_card.klass == 'Murloc' and self.card != self.played_card:
                self.attack_buff += 1
                self.hp_buff += 0
        elif self.card.card_name in ['Blazing_Skyfin']:
            if BattlecryMechanic in self.played_card.mechanics_list:
                self.attack_buff += 1
                self.hp_buff += 1
        elif self.card.card_name in ['Party_Elemental']:
            if self.played_card.klass == 'Elemental' and self.card != self.played_card:
                self.attack_buff += 2
                self.hp_buff += 1
        elif self.card.card_name in ['Saltscale_Honcho']:
            if self.played_card.klass == 'Murloc' and self.card != self.played_card:
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
        
    def choose_buff_targets(self) -> list:
        # Выбираю цели, которых буду бафать
        buff_targets_list = []
        if self.played_card.card_name == 'Coldlight_Seer' and self.card == self.played_card:
            for minion in self.tavern.player_board:
                if minion.klass == 'Murloc' and minion != self.card:
                    buff_targets_list.append(minion)
        return buff_targets_list
        
    def calculate_buffs(self):
        if self.played_card.card_name in ['Coldlight_Seer'] and self.card == self.played_card:
            self.attack_buff += 0
            self.hp_buff += 2
        # elif self.card.card_name in ['Molten_Rock']:
        #     if self.played_card.klass == 'Elemental' and self.card != self.played_card:
        #         self.attack_buff += 0
        #         self.hp_buff += 1
        else:
            pass
