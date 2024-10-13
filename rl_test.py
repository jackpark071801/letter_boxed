import pickle
from rl_train import LetterBoxedEnv, QLearningAgent, load_word_list

def solve_puzzle(agent_file, letter_square):
    """Solve a new letter box puzzle using the trained agent."""
    word_list = load_word_list('english_words.json')

    with open(agent_file, 'rb') as f:
        trained_agent = pickle.load(f)

    env = LetterBoxedEnv(letter_square, word_list)
    
    state = env.reset()
    done = False
    total_reward = 0
    steps = 0
    
    print("Agent attempting to solve the puzzle...")
    while not done and steps < 50:
        action = trained_agent.choose_action(state)
        next_state, reward, done, _ = env.step(action)
        state = next_state
        total_reward += reward
        steps += 1
        env.render()

    print(f"Solved in {steps} steps with a total reward of {total_reward}!")

if __name__ == "__main__":
    agent_file = 'trained_agent.pkl'
    
    letter_square = [
        ['A', 'D', 'I'],
        ['Y', 'O', 'K'],
        ['W', 'N', 'U'],
        ['Q', 'L', 'R']
    ]
    
    solve_puzzle(agent_file, letter_square)
