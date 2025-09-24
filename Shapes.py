from Colors import Colors
import pygame
from Position import Position
class Shapes:
    def __init__(self,id):
        self.id = id
        self.cells = {}
        self.cell_size = 40
        self.rotation_state = 0
        self.move_hor = 0
        self.move_ver = 0
        self.colors = Colors.get_cell_colors()
        
        
        
    def draw(self, screen , offset_x,offest_y):
        tiles = self.get_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column*self.cell_size  , offest_y + tile.row*self.cell_size ,self.cell_size - 1,self.cell_size -1 )
            pygame.draw.rect(screen, self.colors[self.id],tile_rect)
            
    def move(self,rows,columns):
        self.move_hor += rows
        self.move_ver += columns
        
        
    def get_positions(self):
        tiles = self.cells[self.rotation_state]
        movedtiles = []
        for position in tiles:
            position = Position(position.row + self.move_hor , position.column + self.move_ver)
            movedtiles.append(position)
        return  movedtiles
    
    
    def rotate(self):
        self.rotation_state = (self.rotation_state + 1) % len(self.cells)
            
            
    def rotation_inside(self):
        self.rotation_state = (self.rotation_state - 1) % len(self.cells)