import json
import numpy as np
import random
import gym
from gym import spaces
from typing import List, Optional
import pickle

def load_word_list(json_file: str):
    """Load the list of valid words from a JSON file."""
    with open(json_file, 'r') as f:
        word_data = json.load(f)
    return set(word_data)

def load_past_solutions(json_file: str):
    """Load past letter box puzzles from a JSON file."""
    with open(json_file, 'r') as f:
        puzzle_data = json.load(f)
    return puzzle_data

class LetterBoxedEnv(gym.Env):
    def __init__(self, letter_square: List[List[str]], word_list: set, solution: List[str] = None):
        """
        Initialize the environment for either training or testing.
        Args:
            letter_square (List[List[str]]): The square of letters for the puzzle.
            word_list (set): The set of valid words for solving.
            solution (List[str], optional): The known solution for training. Default is None.
        """
        super(LetterBoxedEnv, self).__init__()
        
        self.letter_square = letter_square
        self.square_letters = set(letter for side in letter_square for letter in side)
        self.used_letters = set()
        self.word_list = word_list
        self.solution = solution
        
        if self.solution:
            self.action_space = spaces.Discrete(len(self.solution))
        else:
            self.action_space = spaces.Discrete(len(self.word_list))

        self.observation_space = spaces.MultiBinary(26)
        self.state = self.reset()

    def reset(self):
        """Reset the environment to the initial state."""
        self.used_letters = set()
        return self._get_observation()

    def _get_observation(self):
        """Create an observation based on which letters have been used."""
        obs = np.zeros(26, dtype=int)
        for letter in self.used_letters:
            obs[ord(letter) - ord('A')] = 1
        return obs

    def find_side(self, letter: str) -> Optional[int]:
        """Find the side of the square that contains a given letter."""
        for i, side in enumerate(self.letter_square):
            if letter in side:
                return i
        return None

    def is_valid_word(self, word):
        """Check if the word is valid and uses only the letters from the letter square."""
        prev_side = self.find_side(word[0])
    
        if prev_side is None:
            return False

        for letter in word[1:]:
            current_side = self.find_side(letter)
            if current_side is None or current_side == prev_side:
                return False
            prev_side = current_side
        
        return True

    def step(self, action: int):
        """
        The agent submits a word (by action index), and the environment validates it.
        Args:
            action (int): Index of the word chosen from the solution.
        """
        if self.solution:
            word = self.solution[action]
        else:
            word = list(self.word_list)[action]

        if not self.is_valid_word(word):
            reward = -1
            done = False
        else:
            new_letters = set(word) - self.used_letters
            self.used_letters.update(new_letters)
            reward = len(new_letters)
            done = self.square_letters.issubset(self.used_letters)
            if done:
                reward += 10

        return self._get_observation(), reward, done, {}

    def render(self, mode='human'):
        """Render the current state of the environment."""
        print(f"Used Letters: {''.join(sorted(self.used_letters))}")

    def close(self):
        pass

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995):
        self.env = env
        self.q_table = np.zeros((env.observation_space.n, env.action_space.n))
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.epsilon_decay = exploration_decay

    def choose_action(self, state):
        """Choose an action based on epsilon-greedy policy."""
        if np.random.rand() < self.epsilon:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        """Update Q-values based on the agent's experience."""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.lr * td_error

    def decay_exploration(self):
        """Decay exploration rate after each episode."""
        self.epsilon *= self.epsilon_decay

def train_agent(json_file, num_episodes=1000, max_steps=50):
    past_solutions = load_past_solutions(json_file)
    
    word_list = load_word_list('english_words.json')

    agent = None
    for episode in range(num_episodes):
        puzzle = random.choice(past_solutions)
        letter_square = puzzle['letter_square']
        solution = puzzle['solution']

        env = LetterBoxedEnv(letter_square, word_list, solution=solution)
        
        if agent is None:
            agent = QLearningAgent(env)

        state = env.reset()
        total_reward = 0
        done = False

        for step in range(max_steps):
            if done:
                break

            action = agent.choose_action(state)
            
            next_state, reward, done, _ = env.step(action)

            agent.update(state, action, reward, next_state)

            state = next_state
            total_reward += reward

        agent.decay_exploration()

        print(f"Episode {episode + 1}: Total Reward = {total_reward}, Done = {done}, Steps = {step + 1}")

    return agent


if __name__ == "__main__":
    puzzle_file = 'fixed_solutions.json'
    trained_agent = train_agent(puzzle_file)

    out_file = 'trained_agent.pkl'
    with open(out_file, "wb") as f:
        pickle.dump(trained_agent, f)

    print(f"Training complete! Agent saved as {out_file}")
