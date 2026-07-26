import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from env import InterviewEnv
from agent import InterviewDQN, ReplayBuffer

def train():
    env = InterviewEnv()
    policy_net = InterviewDQN()
    target_net = InterviewDQN()
    target_net.load_state_dict(policy_net.state_dict())
    
    optimizer = optim.Adam(policy_net.parameters(), lr=1e-3)
    memory = ReplayBuffer(capacity=10000)
    
    batch_size = 64
    gamma = 0.99
    epsilon = 1.0
    epsilon_decay = 0.995
    
    print("Initiating training sequence...")
    for episode in range(2000):
        state, _ = env.reset()
        done = False
        
        while not done:
            if np.random.random() < epsilon:
                action = env.action_space.sample()
            else:
                with torch.no_grad():
                    state_tensor = torch.FloatTensor(state).unsqueeze(0)
                    action = policy_net(state_tensor).argmax().item()
            
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            memory.push(state, action, reward, next_state, done)
            state = next_state
            
            if len(memory) > batch_size:
                s, a, r, ns, d = memory.sample(batch_size)
                s = torch.FloatTensor(s)
                a = torch.LongTensor(a).unsqueeze(1)
                r = torch.FloatTensor(r).unsqueeze(1)
                ns = torch.FloatTensor(ns)
                d = torch.FloatTensor(d).unsqueeze(1)
                
                current_q = policy_net(s).gather(1, a)
                max_next_q = target_net(ns).max(1)[0].unsqueeze(1)
                expected_q = r + (gamma * max_next_q * (1 - d))
                
                loss = nn.MSELoss()(current_q, expected_q)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
        epsilon = max(0.01, epsilon * epsilon_decay)
        
        if episode % 200 == 0:
            print(f"Episode {episode} | Epsilon: {epsilon:.2f}")

    torch.save(policy_net.state_dict(), "dqn_model.pth")
    print("Training complete. Model saved to dqn_model.pth")

if __name__ == "__main__":
    train()