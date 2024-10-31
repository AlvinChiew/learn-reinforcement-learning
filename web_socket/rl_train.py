from stable_baselines3 import PPO
from rl_game_server import GameEnv

# Initialize the environment and the model
env = GameEnv()
model = PPO("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)

# Save the model
model.save("trained_bot")

# Close the environment
env.close()
