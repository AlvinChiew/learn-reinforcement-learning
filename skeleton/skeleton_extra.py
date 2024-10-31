from enum import Enum

# import numpy as np
# import pygame

from gymnasium import Env
from gymnasium.spaces import Discrete, Box, Dict


class Actions(Enum):
    UP = 0


class CustomEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size=5):
        self.action_space = Discrete(3)
        self.observation_space = Dict({"agent": Box(0, 100, shape=(1,), dtype=int)})
        self._agent_state = 0

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _get_obs(self):
        return {"agent": self._agent_state}

    def _get_info(self):
        return {"agent": self._agent_state}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # TODO: implement reset

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        # TODO: implement reset step
        reward = 0
        terminated = True

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        # TODO: implement visual with [pygame]
        pass
