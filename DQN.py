# dqn.py
import random
import numpy as np
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
import os

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_size, 256), nn.ReLU(),
            nn.Linear(256, 256), nn.ReLU(),
            nn.Linear(256, action_size)
        )
    def forward(self, x): return self.net(x)

class DQNAgent:
    def __init__(self, state_size, action_size, lr=1e-3, gamma=0.99, eps=1.0, eps_min=0.05, eps_decay=0.995, mem=50000, batch=128):
        self.model = DQN(state_size, action_size)
        self.target = DQN(state_size, action_size)
        self.target.load_state_dict(self.model.state_dict())
        self.optim = optim.Adam(self.model.parameters(), lr=lr)
        self.gamma = gamma
        self.eps, self.eps_min, self.eps_decay = eps, eps_min, eps_decay
        self.memory = deque(maxlen=mem)
        self.batch = batch
        self.action_size = action_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device); self.target.to(self.device)

    def act(self, state):
        if random.random() < self.eps:
            return random.randrange(self.action_size)
        s = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
        with torch.no_grad():
            q = self.model(s)
        return int(torch.argmax(q, dim=1).item())

    def remember(self, s, a, r, s2, d):
        self.memory.append((s, a, r, s2, d))

    def replay(self):
        if len(self.memory) < self.batch: return 0.0
        batch = random.sample(self.memory, self.batch)
        s, a, r, s2, d = zip(*batch)
        s  = torch.tensor(np.array(s), dtype=torch.float32).to(self.device)
        a  = torch.tensor(a, dtype=torch.long).unsqueeze(1).to(self.device)
        r  = torch.tensor(r, dtype=torch.float32).to(self.device)
        s2 = torch.tensor(np.array(s2), dtype=torch.float32).to(self.device)
        d  = torch.tensor(d, dtype=torch.float32).to(self.device)

        q = self.model(s).gather(1, a).squeeze(1)
        with torch.no_grad():
            q2 = self.target(s2).max(1)[0]
            target = r + self.gamma * q2 * (1.0 - d)

        loss = nn.MSELoss()(q, target)
        self.optim.zero_grad(); loss.backward(); self.optim.step()
        
        if self.eps > self.eps_min: self.eps *= self.eps_decay
        return float(loss.item())

    def update_target(self):
        self.target.load_state_dict(self.model.state_dict())
        
        
        
    def save(self, path="checkpoint.pt"):
        ckpt = {
            "model": self.model.state_dict(),
            "target": self.target.state_dict(),
            "optim": self.optim.state_dict(),
            "eps": self.eps,
           
        }
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        torch.save(ckpt, path)
        print(f"[DQN] Saved checkpoint to {path}")

    def load(self, path="checkpoint.pt", strict=True):
        ckpt = torch.load(path, map_location=self.device)
        self.model.load_state_dict(ckpt["model"], strict=strict)
        self.target.load_state_dict(ckpt.get("target", ckpt["model"]), strict=strict)
        self.optim.load_state_dict(ckpt["optim"])
        self.eps = ckpt.get("eps", self.eps)
        
        print(f"[DQN] Loaded checkpoint from {path}")
