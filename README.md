# TetrisAI — Pygame + Reinforcement Learning (DQN)

A playable **Tetris** built with **Pygame**, plus a **reinforcement learning (RL)** agent (DQN) you can train **visually**. Toggle rendering, change speed, and watch the agent learn in real time.



---

##  Features

- **Fully playable Tetris** (arrow keys) with clean drawing and scoring  
- **RL agent (DQN)** with a live training loop and on-screen overlay  
- **Reward shaping** (recommended):
  - `+` reward for **lines cleared**
  - small **per-step penalty** (discourages stalling)
  - `−` penalty for **increases in holes**
  - `−` penalty for **increases in max stack height**
- **Visual trainer controls** (pause, render toggle, speed control)  
- Modular code: game logic is isolated from the environment and the agent

---

##  Project Structure

```
.
├── Block.py          # Piece base / helpers
├── Blocks.py         # (If present) alternate piece definitions
├── Colors.py         # Color palette / utilities
├── DQN.py            # DQN network + agent (replay buffer, target net, epsilon-greedy)
├── Game.py           # Core Tetris logic (grid, spawn, move, rotate, lock, scoring)
├── grid.py           # Grid representation and drawing
├── Position.py       # Small (row, col) helper
├── Shapes.py         # Tetromino definitions + rotation handling
├── TetrisEnv.py      # Gym-like environment for per-key RL training
├── train_visual.py   # Visual training loop with overlays/controls
└── Tetris.py         # Human-playable game loop
```

> **Case-sensitive imports:** On Linux/macOS, import names must match file names exactly (e.g., `from TetrisEnv import TetrisEnv`, not `from tetris_env import ...`).

---

##  Quickstart

### 1) Set up & install

```bash
# Python 3.9+ recommended
python -m venv .venv

# Activate the venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install pygame torch numpy
```

### 2) Play the game (human)

```bash
python Tetris.py
```

**Controls (default):**
- **← / →** — move
- **↑** — rotate
- **↓** — soft drop
- **Esc** — quit

### 3) Train the RL agent (visual)

```bash
python train_visual.py
```

**Trainer hotkeys:**
- **R** — toggle **render** (OFF = much faster training)
- **P** — **pause / resume**
- **F** — cycle **speed** (1× / 4× / 10× steps per frame)
- **N** — single **step** while paused
- *(optional if enabled in code)* **S**/**L** — **save/load** checkpoints, **E** — toggle **eval** mode (ε=0)

---

##  How the RL Agent Works (current setup)

**Environment:** `TetrisEnv.py` (per-key control)

- **State:** flattened `20×10` board (values normalized to `[0, 1]`)
- **Actions:** `LEFT`, `RIGHT`, `ROTATE`, `DOWN`, `NONE`
- **Reward (per step):**
  - `+10 × (lines cleared this step)` (via `Game.last_cleared`)
  - `−0.05` step penalty
  - `−0.5 × max(0, Δholes)` (**only** penalize *increases* in holes)
  - `−0.1 × max(0, Δmax_height)` (**only** penalize *increases* in max column height)

**Agent:** `DQN.py` (Deep Q-Network)
- MLP with replay buffer, target network, epsilon-greedy exploration  
- (If enabled) **Double DQN** targets, **Huber loss**, **gradient clipping**, **soft** target updates

**Training tips**
- Train with **render OFF** and **high speed**; toggle ON occasionally to watch progress.
- Decay epsilon to ~**0.1** relatively quickly; keep a small exploration floor.
- Expect visible improvement ~**200–500 episodes**; “intermediate-ish” around **1k–2k** episodes with per-key control.
- For faster results, see **Roadmap**.

---

##  Saving & Loading (optional)

If you added `save()` / `load()` to `DQN.py` and bound hotkeys in `train_visual.py`:

- **S** → save to `checkpoints/dqn_latest.pt`  
- **L** → load from `checkpoints/dqn_latest.pt`  
- **E** → toggle **eval** (sets ε=0 to watch the current policy)

> If not wired yet, you can still call `agent.save()` / `agent.load()` directly in code.

---

##  Expected Learning Curve

With the **per-key** environment:

- **Visible improvement:** ~**200–500** episodes  
- **Intermediate-ish:** **1k–2k** episodes (clears lines more consistently)  
- **Advanced** often needs more training or an upgraded action space

To accelerate dramatically, switch to **placement-level actions** (one action = choose rotation+column then **hard-drop**). See **Roadmap**.


---

##  Roadmap (Next Steps)

- **Placement-level env:** one decision per piece → **5–10×** faster learning  
- **State channels:** add current/next piece one-hots; consider a tiny CNN over 20×10  
- **SRS wall kicks:** mirror kicks in both game and env for legal rotations in tight spots  
- **Advanced rewards:** bonuses for **Tetrises** / **T-Spins** (after detection is stable)  
- **Benchmarks:** moving-average lines cleared; periodic greedy (ε=0) eval; auto-checkpoints  
- **Heuristic baseline:** 1-ply search with classic features (holes, height, bumpiness) for comparison



---

##  Contributing

Issues and PRs welcome! Ideas: placement-level env, CNN state encoder, better reward shaping, and a heuristic baseline to compare against.

---

## Screenshots

## Human Version

<img width="801" height="835" alt="image" src="https://github.com/user-attachments/assets/00045fa3-68ed-4e95-992d-c179e2d955cb" />
<img width="793" height="832" alt="image" src="https://github.com/user-attachments/assets/555d4bae-8869-4b9d-a056-9fe9bc0a3697" />


## AI-PLayer


<img width="966" height="547" alt="image" src="https://github.com/user-attachments/assets/cf4e3b68-0dc0-4a70-b116-3ae12c9d82ab" />
<img width="966" height="544" alt="image" src="https://github.com/user-attachments/assets/448b747b-7b61-4bb0-8610-4b14af77b819" />




