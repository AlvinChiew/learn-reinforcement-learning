import numpy as np

from gymnasium import Env
from gymnasium.spaces import Discrete, Box
from stable_baselines3 import PPO

# from stable_baselines3.common.vec_env import VecFrameStack

from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy


class LogicChessTrackGameEnv(Env):
    def __init__(self):
        self.action_space = Discrete(3)
        self.observation_space = Box(0, 100, shape=(1,), dtype=int)
        self._obs = np.array([0])
        self._info = {}

    def step(self, action):
        reward = 0
        terminated = True

        return self._obs, reward, terminated, False, self._info

    def render(self):
        pass

    def reset(self, seed=None):
        super().reset(seed=seed)
        return self._obs, self._info


if __name__ == "__main__":
    env = LogicChessTrackGameEnv()
    check_env(env, warn=True)

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10)

    model.save("PPO")
    print(evaluate_policy(model, env, n_eval_episodes=10, render=False))
