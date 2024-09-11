
# Видимо нужны:
#     update_board() для таверны
#     Card().call_mechanics() -- во время апдейта таверны прохожиться по всем картам и "звать механику"
#     Добавить кэш разыгранной карты в play_card, чтобы при update_board() и/или call_mechanics() было понятно, от какой карты првоерять эффект
#     У каждой карты есть список механик: врожденных и приобритенных. По каждому их них проходимся и они возвращают либо изменение, либо ничего

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
    
    def trigger_buffs(self):
        # Вызываю бафы. Метод вызывается, чтобы просчитать бафы и забафать карту.
        # Вероятно это будет реализовано в этом(общем) классе
        ## Рассчитываю баффы
        self.calculate_buffs()
        ## Реализую бафы
        self.card.buff_card(self.hp_buff, 'hp')
        self.card.buff_card(self.attack_buff, 'attack') # Могу ли я использовать сел.данные из подкласса
    
class PlayedCardBuffMechanic(Mechanics):
    """Описание
    Что сейчас класс собой представляет
        --
    Что хочу от класса
        Класс, который расчитывает бафы для карты в зависимости от разыгранной карты. А так же коллит карту забафаться.
        Вероятно, сейчас закину сюда несколько похожих механик через if. Потом их либо разнесу по классам, либо еще че придумаю
    Мысли по улучшению
        Нужно добавить тип баффа (для красненького отдельный, для мэрлока отдельный)
    """
    def __init__(self, card, played_card, tavern=None):
        super().__init__(card, played_card, tavern) 
        # self.buff_name = buff_name# like '1/4 wraith weaver buff'
        
    def calculate_buffs(self):
        if self.card.card_name in ['Wrath_Weaver']:
            if self.played_card.klass == 'Demon':
                self.attack_buff += 2
                self.hp_buff += 1
        elif self.card.card_name in ['Molten_Rock']:
            if self.played_card.klass == 'Elemental':
                self.attack_buff += 0
                self.hp_buff += 1
        elif self.card.card_name in ['Swampstriker']:
            if self.played_card.klass == 'Murloc':
                self.attack_buff += 1
                self.hp_buff += 0
        else:
            pass
