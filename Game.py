from grid import Grid
from Block import *
import random
from Shapes import Shapes

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.currentblock = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.last_cleared = 0      

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def draw (self,screen):
        self.grid.draw(screen)
        self.currentblock.draw(screen,1,1)
        if self.next_block.id == 2:
            self.next_block.draw(screen,395,450)
        elif self.next_block.id == 7:
            self.next_block.draw(screen,395,450)
        else:
            self.next_block.draw(screen,410,450)

    def move_left(self):
        self.currentblock.move(0,-1)
        if self.block_inside() == False or self.block_fits() == False:
            self.currentblock.move(0,1)

    def move_right(self):
        self.currentblock.move(0,1)
        if self.block_inside() == False or self.block_fits() == False:
            self.currentblock.move(0,-1)

    def move_up(self):
        self.currentblock.rotate()
        self.currentblock.move(-1,0)
        if self.block_inside() == False:
            self.currentblock.move(1,0)

    def move_down(self):
        self.currentblock.move(1,0)
        if self.block_inside() == False or self.block_fits() == False:
            self.currentblock.move(-1,0)
            self.lock_block()

    def block_inside(self):
        tiles = self.currentblock.get_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row , tile.column) == False:
                return False
        return True

    def block_fits(self):
        tiles = self.currentblock.get_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row,tile.column) == False:
                return False
        return True

    def lock_block(self):
        tiles = self.currentblock.get_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.currentblock.id
        self.currentblock = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.last_cleared = rows_cleared   
        self.update_score(rows_cleared,0)
        if self.block_fits() == False:
            self.game_over = True

    def rotate(self):
        self.currentblock.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.currentblock.rotation_inside()

    def printgrid(self):
        print(str(self.grid))

    def reset(self):
        self.grid.reset()
        self.score = 0
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.currentblock = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False      
        self.last_cleared = 0       

    def update_score(self,lines_cleared,move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 5:
            self.score += 500
        self.score += move_down_points

    def can_move(self, dr, dc):
        for t in self.currentblock.get_positions():
            r, c = t.row + dr, t.column + dc
            if not self.grid.is_inside(r, c):
                return False
            if not self.grid.is_empty(r, c):
                return False
        return True

    def hard_drop(self):
        dropped = 0
        while self.can_move(1, 0):
            self.currentblock.move(1, 0)
            dropped += 1
        self.lock_block()
        try:
            self.update_score(0, 2*dropped)
        except AttributeError:
            pass
        return dropped
