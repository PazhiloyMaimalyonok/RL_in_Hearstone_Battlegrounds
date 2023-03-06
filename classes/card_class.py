class MinionCard:
    def __init__(self, name, attack, health, minion_type, tavern_tier):
        # TODO add information if minion is from deck or has been spawned by other cards
        self.name = name
        self.attack = attack
        self.health = health
        self.minion_type = minion_type
        self.tavern_tier = tavern_tier

    def __repr__(self):
        return f'Class: {self.__class__.__name__}, name: {self.name}, attack: {self.attack}, health: {self.health}'
