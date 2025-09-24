import pygame
from Colors import Colors


class Grid:

    
    def __init__(self):
        self.num_rows = 20
        self.num_columns = 10
        self.cell_size = 40
        
        self.grid = [[0 for j in range (self.num_columns)]for i in range (self.num_rows)]
        
        self.colors = Colors.get_cell_colors()
        
        
    def printGrid(self):
        for row in range (self.num_rows):
            for column in range(self.num_columns):
                print(self.grid[row][column], end = " ")
            print()
            
            
    def is_inside(self,row,columns):
        if row >= 0 and row < self.num_rows and columns >= 0 and columns < self.num_columns:
            return True
        else:
            return False

    def __str__(self):
        # numbers; '.' for 0
        lines = []
        for r in range(self.num_rows):
            line = ''.join(f'{cell if cell else "." :>2}' for cell in self.grid[r])
            lines.append(line)
        return '\n'.join(lines)
    
    def draw(self , screen):
        
        for row in range (self.num_rows):  #20 rows  , 10 columns 
            for column in range (self.num_columns):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size + 1,row*self.cell_size + 1, self.cell_size -1 ,self.cell_size-1 )
                pygame.draw.rect(screen,self.colors[cell_value],cell_rect)
                
    def is_empty(self,row,column):
        if self.grid[row][column] == 0:
            return True
        return False
        
    
    
    def full_check(self,row):
        for columns in range (self.num_columns):
            if self.grid[row][columns] == 0:
                return False
        return True
    
    def row_clear(self,row):
        for column in range(self.num_columns):
            self.grid[row][column] = 0

    def move_row_down(self,row,num_rows):
        for column in range(self.num_columns):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0
    
    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows - 1, 0 , -1):
            if self.full_check(row):
                completed += 1
            elif completed > 0:
                self.move_row_down(row,completed)
        return completed
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                self.grid[row][column] = 0