import gymnasium as gym
from gymnasium import spaces
import numpy as np

class InterviewEnv(gym.Env):
    def __init__(self, max_questions=10):
        super(InterviewEnv, self).__init__()
        self.max_questions = max_questions
        
        # Actions: 0 (Easy), 1 (Medium), 2 (Hard)
        self.action_space = spaces.Discrete(3)
        self.difficulty_map = {0: -2.0, 1: 0.0, 2: 2.0}
        
        # State: [mu (skill estimate), sigma (uncertainty), questions_asked]
        self.observation_space = spaces.Box(
            low=np.array([-5.0, 0.0, 0.0]), 
            high=np.array([5.0, 5.0, self.max_questions]), 
            dtype=np.float32
        )

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.true_skill = np.random.uniform(-3.0, 3.0)
        self.current_mu = 0.0
        self.current_sigma = 3.0 
        self.questions_asked = 0
        return self._get_state(), {}

    def step(self, action):
        difficulty = self.difficulty_map[action]
        
        # Simulate candidate answer
        prob_correct = 1 / (1 + np.exp(-(self.true_skill - difficulty)))
        is_correct = np.random.random() < prob_correct
        
        # Bayesian update
        prev_sigma = self.current_sigma
        learning_rate = 0.5 * self.current_sigma
        
        if is_correct:
            self.current_mu += learning_rate * (1 - prob_correct)
        else:
            self.current_mu -= learning_rate * prob_correct
            
        self.current_sigma *= 0.8 
        self.questions_asked += 1
        
        # Reward: Maximizing Information Gain (reducing uncertainty)
        reward = (prev_sigma - self.current_sigma) 
        
        terminated = self.questions_asked >= self.max_questions
        return self._get_state(), reward, terminated, False, {}

    def _get_state(self):
        return np.array([self.current_mu, self.current_sigma, self.questions_asked], dtype=np.float32)