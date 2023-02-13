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

