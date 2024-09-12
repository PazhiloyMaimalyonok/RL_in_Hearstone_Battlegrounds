class MinionCard:
    def __init__(self, name, attack, health, minion_type, tavern_tier, provoke):
        # TODO add information if minion is from deck or has been spawned by other cards
        self.name = name
        self.attack = attack
        self.health = health
        self.minion_type = minion_type
        self.tavern_tier = tavern_tier

        self.provoke: bool = provoke

    def __repr__(self):
        return f'Class: {self.__class__.__name__}, name: {self.name}, attack: {self.attack}, health: {self.health}'


class FightingMinion(MinionCard):
    has_attacked = False

    def __init__(self, minion_card: MinionCard):
        super().__init__(minion_card.name, minion_card.attack, minion_card.health, minion_card.minion_type,
                         minion_card.tavern_tier, minion_card.provoke)
