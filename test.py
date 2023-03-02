from main import Game, Tavern

a = [1 , 2, 3 , 4]
b = [int(x>2) for x in a]
print(b)
print(sum(b))

"""
#testing Fight(). Изменил количества стартового золота для теста
game = Game()
taverna_first_player = Tavern(game)
taverna_first_player.buy(0)
taverna_first_player.buy(0)
taverna_first_player.play_card(0)
taverna_first_player.play_card(0)
print([minion.card_info() for minion in taverna_first_player.player_board])

taverna_second_player = Tavern(game)
taverna_second_player.buy(0)
taverna_second_player.buy(0)
taverna_second_player.play_card(0)
taverna_second_player.play_card(0)
print([minion.card_info() for minion in taverna_second_player.player_board])

fight = Fight(taverna_first_player, taverna_second_player)
print(fight.simulate())
print([minion.card_info() for minion in taverna_first_player.player_board])
print([minion.card_info() for minion in taverna_second_player.player_board])
"""

"""
from main import Game, Tavern
game = Game()
taverna = Tavern(game)
taverna.buy(0)
taverna.play_card(0)
print(taverna.player_board)
abob = list(taverna.player_board)
taverna.player_board[0].hp -= 1
print(taverna.player_board[0].card_info())
print(abob[0].card_info())
"""

"""
#Player tavern check
from main import Game, Tavern

game = Game()
taverna = Tavern(game)
print(taverna.tavern_board)
print(taverna.tavern_info())
taverna.buy(2)
print(taverna.tavern_info())
print(taverna.player_hand[0].card_info())
taverna.play_card(0)
print(taverna.player_board[0].card_info())
print(f'Number of minions in pool before sell: {len(game.cards_pool)}')
taverna.sell(0)
print(taverna.player_board)
print(f'Number of minions in pool after sell: {len(game.cards_pool)}')
taverna.reroll()
print(f'Number of minions in pool after reroll: {len(game.cards_pool)}')
print(taverna.tavern_info())
print('second player')
taverna2 = Tavern(game)
print(taverna2.tavern_info())
print(f'Number of minions in pool after second player started: {len(game.cards_pool)}')
"""
