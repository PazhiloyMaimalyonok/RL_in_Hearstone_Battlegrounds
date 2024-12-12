# bg_env.py
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector
import numpy as np

from game_module import Game

class BattlegroundsAECEnv(AECEnv):
    metadata = {"render.modes": ["human"]}

    def __init__(self, players_number=2):
        super().__init__()
        self.players_number = players_number
        self.agents = [f"player_{i}" for i in range(players_number)]
        self.possible_agents = self.agents[:]
        self.agent_selector = agent_selector(self.agents)
        self.action_spaces = {agent: self._get_action_space() for agent in self.agents}
        self.observation_spaces = {agent: self._get_observation_space() for agent in self.agents}
        self.game = Game(players_number=self.players_number)

    def _get_action_space(self):
        # Define a discrete or dict action space for each agent
        from gymnasium import spaces
        return spaces.Dict({
            'action_type': spaces.Discrete(7),
            'position': spaces.Discrete(30)
        })

    def _get_observation_space(self):
        from gymnasium import spaces
        # Define the observation space
        return spaces.Box(low=0, high=100, shape=(100,), dtype=np.float32)

    def reset(self, seed=None, return_info=False, options=None):
        self.has_reset = True
        self.game.reset()
        self.game.create_players_taverns()
        self.turn = 0
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()
        self.done = {agent: False for agent in self.agents}
        self.reward = {agent: 0 for agent in self.agents}
        self.info = {agent: {} for agent in self.agents}

    def observe(self, agent):
        return self._get_observation_for_agent(agent)

    def _get_observation_for_agent(self, agent):
        # Convert the agent's current state into a numeric observation
        # Identify which player index this agent corresponds to
        idx = self.agents.index(agent)
        current_player = self.game.players_taverns[idx]
        obs = np.zeros((100,), dtype=np.float32)
        obs[0] = current_player.gold
        obs[1] = current_player.player_hp
        obs[2] = current_player.level
        # Add more encoding as needed
        return obs

    def step(self, action):
        # action is what the current agent chooses
        if self.done[self.agent_selection]:
            # If this agent is done, skip
            self._was_done_step(action)
            return

        idx = self.agents.index(self.agent_selection)
        current_player = self.game.players_taverns[idx]

        # Apply action
        turn_log = current_player.player_turn([action])
        
        # Check if this action ends the turn
        if action['action_type'] == 6:
            # End turn logic
            # Move to next agent
            self.agent_selection = self._agent_selector.next()
            # If we wrapped around to the first agent, it means a round ended
            if self.agent_selection == self.agents[0]:
                round_log = self.game.play_round()
                # Calculate rewards based on round outcome
                self._assign_rewards(round_log)

        # Check if game over
        if len(self.game.players_taverns) == 1:
            winner_name = self.game.players_taverns[0].player_name
            # Find which agent is winner
            winner_idx = [p.player_name for p in self.game.players_taverns].index(winner_name)
            # Assign terminal rewards
            for i, ag in enumerate(self.agents):
                if i == winner_idx:
                    self.reward[ag] = 100
                else:
                    self.reward[ag] = -50
                self.done[ag] = True
        else:
            # No game over yet, continue
            pass

        self._clear_rewards()  # Clears previous rewards
        self._accumulate_rewards()

    def _assign_rewards(self, round_log):
        # Assign partial rewards based on round outcome
        # E.g., if an agent survived, +1; if dealt damage, +damage/10
        # This depends on how you track agent performance
        pass

    def render(self, mode="human"):
        # Optional: print or visualize the state
        pass
