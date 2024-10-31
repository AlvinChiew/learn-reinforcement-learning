import gymnasium as gym
from gymnasium import spaces
import websocket
import json


class GameEnv(gym.Env):
    def __init__(self):
        super(GameEnv, self).__init__()

        # Connect to the Dart WebSocket server
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://localhost:8080")

        # Define action and observation space
        self.action_space = spaces.Discrete(2)  # 0: move_backward, 1: move_forward
        self.observation_space = spaces.Discrete(21)  # position range from -10 to +10

    def reset(self):
        # Send reset signal to the server
        self.ws.send(json.dumps({"action": "reset"}))
        response = json.loads(self.ws.recv())
        return response["state"]

    def step(self, action):
        # Map action to a move
        move = "move_forward" if action == 1 else "move_backward"

        # Send the step action to the Dart server
        self.ws.send(json.dumps({"action": "step", "move": move}))
        response = json.loads(self.ws.recv())

        # Extract state, reward, and done from the response
        state = response["position"]
        reward = response["reward"]
        done = response["done"]

        return state, reward, done, {}

    def close(self):
        self.ws.close()
