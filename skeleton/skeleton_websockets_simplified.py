import json
import numpy as np
import asyncio
import websockets

# import nest_asyncio  # uncomment this in Jupyter

from gymnasium import Env
from gymnasium.spaces import Discrete, Box  # , Dict, Tuple, MultiBinary, MultiDiscrete

from stable_baselines3 import PPO

# from stable_baselines3.common.vec_env import VecFrameStack

from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy


# nest_asyncio.apply()  # uncomment this in Jupyter


class CustomEnv(Env):
    metadata = {"ws_uri": "ws://localhost:8001"}

    def __init__(self):

        self._ws = None

        self.action_space = Discrete(3)
        self.observation_space = Box(0, 100, shape=(1,), dtype=int)
        self._obs = np.array([0])
        self._info = {}

        asyncio.run(self._connect_ws())

    def reset(self, seed=None):
        super().reset(seed=seed)

        response = asyncio.run(self._post_ws({"process": "reset"}))
        self._obs = np.array(response["obs"])

        return self._obs, self._info

    def step(self, action):
        response = asyncio.run(self._post_ws({"action": action}))

        self._obs = np.array(response["obs"])
        reward = response["reward"]
        done = True if response["done"] == "True" else False

        return self._obs, reward, done, False, self._info

    def close(self):
        asyncio.run(self._ws.close())

    def render(self):
        pass

    async def _connect_ws(self):
        self._ws = await websockets.connect(self.metadata["ws_uri"])

    async def _post_ws(self, message):
        message = {
            k: (v.tolist() if isinstance(v, np.ndarray) else v)
            for k, v in message.items()
        }
        await self._ws.send(json.dumps(message))
        response = await self._ws.recv()
        return json.loads(response)


if __name__ == "__main__":
    env = CustomEnv()
    print(check_env(env, warn=True))

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10)

    model.save("PPO")
    print(evaluate_policy(model, env, n_eval_episodes=10, render=False))

    env.close()
