
import pygame
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

width, height = 400, 400
rows, cols = 4, 4
square_size = width // cols
screen = pygame.display.set_mode((width, height))

grid = [[random.randint(1, 4) for _ in range(cols)] for _ in range(rows)]
player_pos = [0, 0]

score = 0

def time_step():
    screen.fill((0, 0, 0))
    draw_grid()
    pygame.display.flip()

def get_world_size():
    time_step()
    return (rows, cols)

def get_player_position():
    time_step()
    return tuple(player_pos)

def get_pos_x():
    return player_pos[1]

def get_pos_y():
    return player_pos[0]

def measure(dir=None):
    row, col = player_pos
    time_step()
    if dir is None:
        return grid[row][col]
    elif dir == "North":
        if player_pos[0] < rows - 1:
            return grid[row+1][col]
        else:
            return grid[row][col]
    elif dir == "West":
        if player_pos[1] > 0:
            return grid[row][col-1]
        else:
            return grid[row][col]
    elif dir == "South":
        if player_pos[0] > 0:
            return grid[row-1][col]
        else:
            return grid[row][col]
    elif dir == "East":
        if player_pos[1] < cols - 1:
            return grid[row][col+1]
        else:
            return grid[row][col]

def draw_grid():
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * square_size, (rows - 1 - row) * square_size, square_size, square_size)
            color = (255, 255, 255)
            if [row, col] == player_pos:
                color = (0, 255, 0)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            num = grid[row][col]
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(num), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 0, 255))
    screen.blit(score_text, (10, 10))

def move(direction):
    # print("Move, ", direction)
    if direction == 'North':
        if player_pos[0] < rows - 1:
            player_pos[0] += 1
        else:
            player_pos[0] = 0
    elif direction == 'South':
        if player_pos[0] > 0:
            player_pos[0] -= 1
        else:
            player_pos[0] = rows-1
    elif direction == 'West':
        if player_pos[1] > 0:
            player_pos[1] -= 1
        else:
            player_pos[1] = cols-1
    elif direction == 'East':
        if player_pos[1] < cols - 1:
            player_pos[1] += 1
        else:
            player_pos[1] = 0
    time_step()
    # pygame.time.delay(500)

def swap(direction):
    #print("Swap, ", direction)
    row, col = player_pos
    if direction == 'North' and row < rows - 1:
        grid[row][col], grid[row+1][col] = grid[row+1][col], grid[row][col]
    elif direction == 'South' and row > 0:
        grid[row][col], grid[row-1][col] = grid[row-1][col], grid[row][col]
    elif direction == 'West' and col > 0:
        grid[row][col], grid[row][col-1] = grid[row][col-1], grid[row][col]
    elif direction == 'East' and col < cols - 1:
        grid[row][col], grid[row][col+1] = grid[row][col+1], grid[row][col]
    # time_step()

def check_map():
    rows, cols = get_world_size()
    for row in range(rows):
        for col in range(cols):
            num = grid[row][col]
            if row > 0:
                if grid[row-1][col] > num:
                    print(f"At {(row, col)} ({num}) is smaller than {(row-1, col)} ({grid[row-1][col]}) to the South")
                    return False, (row, col)
            if col > 0:
                if grid[row][col-1] > num:
                    print(f"At {(row, col)} ({num}) is smaller than {(row, col-1)} ({grid[row][col-1]}) to the West")
                    return False, (row, col)
            if row < rows-1:
                if grid[row+1][col] < num:
                    print(f"At {(row, col)} ({num}) is greater than {(row+1, col)} ({grid[row+1][col]}) to the North")
                    return False, (row, col)
            if col < cols-1:
                if grid[row][col+1] < num:
                    print(f"At {(row, col)} ({num}) is greater than {(row, col+1)} ({grid[row][col+1]}) to the East")
                    return False, (row, col)
    return True, None

def reset_game():
    global player_pos, grid
    player_pos = [0, 0]
    grid = [[random.randint(1, 4) for _ in range(cols)] for _ in range(rows)]

def show_win_message():
    global score
    root = tk.Tk()
    root.withdraw()
    # messagebox.showinfo("Congratulations!", "You won!")
    root.destroy()
    reset_game()
    score += 1

def show_fail_message(row, col):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Check Failed", f"Check failed at square ({row}, {col})")
    root.destroy()


def player_code():
    # Code goes here and returns win condition
    return None
          
running = True
script_run = False
while running:
    screen.fill((0, 0, 0))
    draw_grid()
    pygame.display.flip()

    while script_run == False:
        win = player_code()
        print("Win ", win)
        if win == True:
            show_win_message()
        if win == None:
            script_run = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # key check
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #         move('North')
        #     if event.key == pygame.K_DOWN:
        #         move('South')
        #     if event.key == pygame.K_LEFT:
        #         move('West')
        #     if event.key == pygame.K_RIGHT:
        #         move('East')
        #     if event.key == pygame.K_w:
        #         swap('North')
        #     if event.key == pygame.K_s:
        #         swap('South')
        #     if event.key == pygame.K_a:
        #         swap('West')
        #     if event.key == pygame.K_d:
        #         swap('East')
        #     if event.key == pygame.K_RETURN:
        #         success, failed_square = check_map()
        #         if success:
        #             show_win_message()
        #         else:
        #             row, col = failed_square
        #             show_fail_message(row, col)

pygame.quit()
