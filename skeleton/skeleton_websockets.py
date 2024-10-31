import json
import numpy as np
import asyncio
import websockets

from gymnasium import Env
from gymnasium.spaces import Discrete, Box  # , Dict, Tuple, MultiBinary, MultiDiscrete

from stable_baselines3 import PPO

# from stable_baselines3.common.vec_env import VecFrameStack

from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy


class CustomEnv(Env):
    metadata = {"ws_uri": "ws://localhost:8001"}

    def __init__(self):

        self._ws = None
        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self._connect_ws())

        self.action_space = Discrete(3)
        self.observation_space = Box(0, 100, shape=(1,), dtype=int)
        self._obs = np.array([0])
        self._info = {}

    def reset(self, seed=None):
        super().reset(seed=seed)

        response = self._loop.run_until_complete(self._post_ws({"process": "reset"}))
        self._obs = np.array(response["obs"])

        return self._obs, self._info

    def step(self, action):
        response = self._loop.run_until_complete(
            self._post_ws({"process": "step", "action": action})
        )

        self._obs = np.array(response["obs"])
        reward = response["reward"]
        done = True if response["done"] == "True" else False

        return self._obs, reward, done, False, self._info

    def close(self):
        if self._ws:
            self._loop.run_until_complete(self._ws.close())
        self._loop.close()

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
