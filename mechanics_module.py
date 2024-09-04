
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
    Мысли по улучшению
        --
    """
    def __init__(self, players_number = 2):
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
