import json
import numpy as np
import websocket

from gymnasium import Env
from gymnasium.spaces import Discrete, Box  # , Dict, Tuple, MultiBinary, MultiDiscrete

from stable_baselines3 import PPO

# from stable_baselines3.common.vec_env import VecFrameStack

from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy


class CustomEnv(Env):
    metadata = {"game_uri": "ws://localhost:8080"}

    def __init__(self):

        self._ws = websocket.WebSocket()
        self._ws.connect(self.metadata["game_uri"])

        self.action_space = Discrete(3)
        self.observation_space = Box(0, 100, shape=(1,), dtype=int)
        self._obs = np.array([0])
        self._info = {}

    def reset(self, seed=None):
        super().reset(seed=seed)

        self._ws.send(json.dumps({"process": "reset"}))
        response = json.loads(self._ws.recv())
        self._obs = response["state"]

        return self._obs, self._info

    def step(self, action):
        self._ws.send(json.dumps({"process": "step", "action": action}))
        response = json.loads(self._ws.recv())

        self._obs = response["obs"]
        reward = response["reward"]
        done = response["done"]

        return self._obs, reward, done, False, self._info

    def render(self):
        pass


if __name__ == "__main__":
    env = CustomEnv()
    check_env(env, warn=True)

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10)

    model.save("PPO")
    print(evaluate_policy(model, env, n_eval_episodes=10, render=False))

    env.close()
