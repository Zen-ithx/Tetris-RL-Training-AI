# TetrisEnv.py
import numpy as np
import pygame
from Game import Game


A_LEFT, A_RIGHT, A_ROTATE, A_DOWN, A_NONE = range(5)

class TetrisEnv:
    def __init__(self, game: Game):
        self.game = game
        self.action_space_n = 5
        self.obs_size = self.game.grid.num_rows * self.game.grid.num_columns

      
        self._prev_holes = 0
        self._prev_max_h = 0

  
    def reset(self):
        
        self.game.reset()
        
        self.game.last_cleared = 0

        # snapshot initial stats for shaping
        stats = self._snapshot_board_stats()
        self._prev_holes = stats["holes"]
        self._prev_max_h = stats["max_h"]
        return self._get_state()

    def step(self, action: int):
        
        if action == A_LEFT:    self.game.move_left()
        elif action == A_RIGHT: self.game.move_right()
        elif action == A_ROTATE:self.game.rotate()
        elif action == A_DOWN:  self.game.move_down()
        

        
        self.game.move_down()

       
        reward = 10.0 * getattr(self.game, "last_cleared", 0) - 0.05

        # shaping: penalize increases in holes and max height
        stats = self._snapshot_board_stats()
        d_holes = max(0, stats["holes"] - self._prev_holes)
        d_max_h = max(0, stats["max_h"] - self._prev_max_h)
        reward += -0.5 * d_holes
        reward += -0.1 * d_max_h

    
        self._prev_holes = stats["holes"]
        self._prev_max_h = stats["max_h"]

        
        self.game.last_cleared = 0

        done = bool(getattr(self.game, "game_over", False))
        state = self._get_state()
        return state, reward, done, {}

    def render(self, screen, overlay=None):
        screen.fill((0, 0, 0))
        self.game.draw(screen)
        if overlay: overlay(screen)
        pygame.display.flip()

  
    def _get_state(self):
        
        g = self.game.grid.grid
        arr = np.array(g, dtype=np.float32)
        return (arr / 7.0).ravel()

    def _column_heights(self):
        g = self.game.grid.grid
        R, C = len(g), len(g[0])
        H = [0] * C
        for c in range(C):
            for r in range(R):
                if g[r][c] != 0:
                    H[c] = R - r  
                    break
        return H

    def _count_holes(self, heights):
        g = self.game.grid.grid
        R, C = len(g), len(g[0])
        holes = 0
        for c in range(C):
            top = R - heights[c]
            if top < 0: top = 0
            for r in range(top, R):
                if g[r][c] == 0:
                    holes += 1
        return holes

    def _snapshot_board_stats(self):
        H = self._column_heights()
        return {
            "holes": self._count_holes(H),
            "max_h": max(H) if H else 0,
        }
