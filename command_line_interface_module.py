def get_player_action_cli():
    print('Choose an action number:')
    print('1 - Buy a minion')
    print('2 - Play a card')
    print('3 - Sell a minion')
    print('4 - Reroll')
    print('5 - Show stats')
    print('6 - End the turn')

    while True:
        try:
            action_number = int(input())
            if action_number in [1, 2, 3, 4, 5, 6]:
                break
            else:
                print("Invalid choice. Try again:")
        except ValueError:
            print("Please enter a valid integer for the action number.")

    position = None
    if action_number in [1, 2, 3]:  # Actions that require a position
        print('Enter the position (starting from 0):')
        while True:
            try:
                position = int(input())
                break
            except ValueError:
                print("Please enter a valid integer for position.")

    return {'action_type': action_number, 'position': position}


def display_tavern_info(tavern):
    tavern_board_info = [minion.card_info() for minion in tavern.tavern_board]
    print(f'Tavern board: {tavern_board_info}')


def display_player_hand(tavern):
    hand_info = [card.card_info() for card in tavern.player_hand]
    print(f'Player hand: {hand_info}')


def display_player_board(tavern):
    board_info = [card.card_info() for card in tavern.player_board]
    print(f'Player board: {board_info}')


def display_player_stats(tavern):
    print(f'Player gold: {tavern.gold}, HP: {tavern.player_hp}, Tavern level: {tavern.level}')


def display_turn_log(turn_log):
    for i, entry in enumerate(turn_log, start=1):
        if 'error' in entry:
            print(f"{i}. Error: {entry['error']}")
        else:
            action = entry.get('action', 'No action')
            card = entry.get('card', 'No card')
            print(f"{i}. {action.capitalize()} - {card}")
