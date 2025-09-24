# train_visual.py
import pygame, time
import numpy as np
from Game import Game
from TetrisEnv import TetrisEnv, A_LEFT, A_RIGHT, A_ROTATE, A_DOWN, A_NONE  
from DQN import DQNAgent  

WIDTH, HEIGHT = 800, 800

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock  = pygame.time.Clock()
    font   = pygame.font.Font(None, 28)

    game = Game()
    env  = TetrisEnv(game)
    state = env.reset()

    agent = DQNAgent(state_size=len(state), action_size=5)

    
    render     = True
    paused     = False
    speed_idx  = 0
    speeds     = [1, 4, 10]  
    target_sync_every = 10 
    episode = 0
    ep_reward = 0.0
    ep_steps  = 0

    if episode % 50 == 0:
        agent.update_target()
        agent.save("checkpoints/dqn_latest.pt")

    def overlay(surface):
        lines = [
            f"Episode: {episode}",
            f"EpReward: {ep_reward:.1f}",
            f"Epsilon: {agent.eps:.2f}",
            f"Steps: {ep_steps}",
            f"Speed: x{speeds[speed_idx]}",
            f"Render: {'ON' if render else 'OFF'}  Pause: {'YES' if paused else 'NO'}",
        ]
        y = 10
        for txt in lines:
            t = font.render(txt, True, (255,255,255))
            surface.blit(t, (10, y))
            y += 22

    running = True
    while running:
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: running = False
                elif e.key == pygame.K_r: render = not render
                elif e.key == pygame.K_p: paused = not paused
                elif e.key == pygame.K_f: speed_idx = (speed_idx + 1) % len(speeds)
                elif e.key == pygame.K_s:
                    agent.save("checkpoints/dqn_latest.pt")
                elif e.key == pygame.K_l:
                    try:
                        agent.load("checkpoints/dqn_latest.pt")
                    except FileNotFoundError:
                        print("No checkpoint found at checkpoints/dqn_latest.pt")
                elif e.key == pygame.K_e:
                    # toggle eval mode (epsilon=0 while held, or toggle)
                    agent.eps = 0.0 if agent.eps > 0.0 else 0.1  

                
                
                
                elif e.key == pygame.K_n and paused:
                   
                    act = agent.act(state)
                    state, reward, done, _ = env.step(act)
                    agent.remember(state, act, reward, state, done)  
                    loss = agent.replay()
                    ep_reward += reward; ep_steps += 1
                    if done:
                        episode += 1
                        if episode % target_sync_every == 0: agent.update_target()
                        state = env.reset(); ep_reward = 0.0; ep_steps = 0

        
        if not paused:
            for _ in range(speeds[speed_idx]):
                act = agent.act(state)
                next_state, reward, done, _ = env.step(act)
                agent.remember(state, act, reward, next_state, float(done))
                loss = agent.replay()
                state = next_state
                ep_reward += reward
                ep_steps  += 1
                if done:
                    episode += 1
                    if episode % target_sync_every == 0: agent.update_target()
                    state = env.reset(); ep_reward = 0.0; ep_steps = 0
                    break

        
        if render:
            env.render(screen, overlay=overlay)
            clock.tick(60)   
        else:
            pass

    pygame.quit()

if __name__ == "__main__":
    main()
