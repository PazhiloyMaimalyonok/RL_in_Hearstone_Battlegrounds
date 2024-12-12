from game_module import Game
from command_line_interface_module import (
    get_player_action_cli,
    display_tavern_info,
    display_player_hand,
    display_player_board,
    display_player_stats,
    display_turn_log
)

def main():
    game = Game()
    player_names = ['Player1', 'Player2']  # You can customize player names here.
    game.create_players_taverns(player_names)

    while len(game.players_taverns) > 1:
        # Each player takes a turn
        for tavern in game.players_taverns:
            # Handle start-of-turn logic (reroll, set gold, etc.)
            tavern.start_of_turn()

            # Display the state after start_of_turn()
            print(f"------------------------- {tavern.player_name}'s turn -------------------------")
            display_tavern_info(tavern)
            display_player_hand(tavern)
            display_player_board(tavern)
            display_player_stats(tavern)

            # Collect actions from the player until they choose to end the turn
            action_list = []
            while True:
                action = get_player_action_cli()
                action_type = action['action_type']

                if action_type == 6:
                    # End turn
                    break
                elif action_type == 5:
                    # Show stats again (no change to state, just re-display)
                    display_tavern_info(tavern)
                    display_player_hand(tavern)
                    display_player_board(tavern)
                    display_player_stats(tavern)
                else:
                    # These actions modify the state and should be recorded
                    action_list.append(action)

            # Execute all actions chosen by the player
            turn_log = tavern.player_turn(action_list)
            
            # Print detailed results of each action
            for entry in turn_log:
                if 'error' in entry:
                    print(f"Error: {entry['error']}")
                else:
                    if entry.get('action') == 'buy':
                        print(f"You bought a minion: {entry['card']}")
                    elif entry.get('action') == 'play_card':
                        print(f"You played a card: {entry['card']}")
                    elif entry.get('action') == 'sell':
                        print(f"You sold a minion: {entry['card']}")
                    elif entry.get('action') == 'reroll':
                        print("You rerolled the tavern board!")
                        print("New Tavern Board:")
                        for minion_info in entry.get('tavern_board', []):
                            print(minion_info)

            # Display a summary of all actions taken this turn
            print("Actions taken this turn:")
            display_turn_log(turn_log)

        # After all players have completed their turns, simulate the fight phase
        round_log = game.play_round()
        # Print results of the fights
        for fight_result in round_log:
            if 'tie' in fight_result:
                print("It's a tie this round!")
            else:
                print(f"{fight_result['winner']} defeated {fight_result['loser']} dealing {fight_result['damage']} damage!")

    # When only one player remains, declare the winner
    winner = game.declare_winner()
    print(f"The winner is {winner}")

if __name__ == "__main__":
    main()
