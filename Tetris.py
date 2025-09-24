import pygame
from Game import Game



WIDTH = 800
HEIGHT = 800

BLACK = (0,0,0)
WHITE = (255, 255,255)

pygame.init()
pygame.font.init()
title_font = pygame.font.Font(None,40)

 
score_surface = title_font.render("Score", True , WHITE)
score_rect = pygame.Rect(510,150 , 170 ,60)
next_surface = title_font.render("Next" , True , WHITE)
next_rec = pygame.Rect(510,350 , 170, 250)
game_over_sur = title_font.render("Game Over" , True , WHITE)


pygame.display.set_caption("TetrisAI")
clock = pygame.time.Clock()


screen = pygame.display.set_mode((WIDTH,HEIGHT))

game = Game()

game.printgrid()

updater = pygame.USEREVENT
pygame.time.set_timer(updater , 200)
last_down_time = -9999
DOUBLE_TAP_MS = 200
"""
game_grid.grid[2][0] = 5
game_grid.grid[3][5] = 4
game_grid.grid[17][8] = 7
"""

"""
print("rows attr:", game.grid.num_rows)
print("cols attr:", game.grid.num_columns)

actual_rows = len(game.grid.grid)
actual_cols = len(game.grid.grid[0]) if actual_rows else 0
print(f"rows x cols from grid data: {actual_rows} x {actual_cols}")

# Sanity check
assert game.grid.num_rows == actual_rows, "Grid.rows != len(grid)"
assert game.grid.num_columns == actual_cols, "Grid.cols != len(grid[0])"
"""


while True:
 

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
            
        
        if event.type == pygame.KEYDOWN:
            if  game.game_over :
                game.game_over = False
                game.reset()
                
                
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
            if event.key == pygame.K_DOWN and game.game_over == False:
                now = pygame.time.get_ticks()
                if now - last_down_time <= DOUBLE_TAP_MS:
                    game.hard_drop()
                else:
                    game.move_down()
                last_down_time = now
        if event.type == updater and game.game_over == False:
            game.move_down()   
            game.update_score(0,1)     
                

        
    score_value_surface = title_font.render(str(game.score),True , WHITE)

    
    screen.fill(BLACK)
    screen.blit(score_surface, (550, 100 ,50 , 50))
    pygame.draw.rect(screen, (244,179,194) , score_rect , 0 , 10)
    screen.blit(score_value_surface,score_value_surface.get_rect(centerx = score_rect.centerx,centery = score_rect.centery))
    screen.blit(next_surface, (560, 300 ,50 , 50))
    pygame.draw.rect(screen,(244,179,194),next_rec,0,10)
    game.draw(screen)
    
    
    if game.game_over == True:       
        screen.blit(game_over_sur, (125, 360 ,50 , 50))
        
        
    clock.tick(60)

    
    pygame.display.update()





            
        