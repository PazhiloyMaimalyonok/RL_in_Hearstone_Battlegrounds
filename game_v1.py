from main import Tavern, Fight
import random
        
class Game_old:
    """Описание
    Что сейчас класс собой представляет
        Класс для партии игры. Определяет очередность действий игроков, выбирает следующего противника
        , рассчитывает урон после сражения, определяет, кто победил в партии
    Что хочу от класса
        Класс или несколько классов для всех типов карт: заклинания, миньоны
    Мысли по улучшению
        Почему пул существ создается в Game, а не в Tavern? 
            Потому что Tavern уникальна для игрока в партии (Game). А пул существ уникален для партии (Game)
        Почему метод card_draw, card_return_to_pool лежат в Game?
        Переделать play_game по совету chatGPT
    """
    def __init__(self, players_number = 2):
        self.players_number = players_number
        self.turn_number = 1
        #Adding required amount of cards to the pool
        self.cards_pool = []
        for card_name in Card.minions_list:
            for card_number in range(Card(card_name).card_amount):
                self.cards_pool.append(Card(card_name))
        random.shuffle(self.cards_pool)
    
    def card_draw(self):
        return self.cards_pool.pop()

    def card_return_to_pool(self, card):
        self.cards_pool.append(card)

    def play_game(self):
        game = Game()
        print('Would u like to name players? 1 - Yes, 0 - No')
        agreement = int(input())
        if agreement == 1:
            print('Enter players names like this "Player1 Player2"')
            players_names = [player_name for player_name in input().split()]
            players_taverns = []
            for i in range(self.players_number):
                players_taverns.append(Tavern(game, player_name = players_names[i]))
        else:
            players_taverns = []
            for i in range(self.players_number):
                players_taverns.append(Tavern(game, player_name = 'Player' + str(i + 1)))
        while len(players_taverns) > 1:
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
                    print('error')
            for player in players_taverns:
                if player.player_hp <= 0:
                    players_taverns.remove(player)

        print(f'Player {players_taverns[0].player_name} won')