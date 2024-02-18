import curses
import os
import time
import random

print('\033[?25l', end="")

stdscr = curses.initscr()

def clear_screen():
    os.system('clear')
    
def print_char(x, y, char):
    print("\033["+str(y)+";"+str(x)+"H"+char)

width = 50
height = 15
score = 0

def print_borders():
    for i in range(2, width):
        print_char(i, 1, '-')
        
    for i in range(2, width):
        print_char(i, height, '-')

    for i in range(2, height):
        print_char(1, i, '|')
        
    for i in range(2, height):
        print_char(width, i, '|')

def print_score():
    print_char(1, height+1, " Score: " + str(score))

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        print_char(self.x, self.y, '*')

class Snake:
    def __init__(self):
        self.head_pos = [2, 2]
        self.dir = [1, 0]
        self.tales = [[self.head_pos[0] - self.dir[0], self.head_pos[1] - self.dir[1]]]
        self.need_to_grow = False

    def draw(self):
        print_char(self.head_pos[0], self.head_pos[1], '@')
        for x in self.tales:   
            print_char(x[0], x[1], 'O')

    def grow_up(self):
        self.need_to_grow = True
    
    def is_head_touching_tail(self):
        for tale in self.tales:
            if tale == self.head_pos:
                return True
        return False
    
    def is_point_on_snake(self, p):
        if p == self.head_pos:
            return True
        for tale in self.tales:
            if tale == p:
                return True
        return False

    def tick(self):
        self.tales.insert(0, self.head_pos.copy())
        if self.need_to_grow:
            self.need_to_grow = False
        else:
            del self.tales[-1]

        self.head_pos[0] += self.dir[0]
        self.head_pos[1] += self.dir[1]

s = Snake()


foods = []
def spawn_food():
    is_point_on_snake = True
    while is_point_on_snake:
        rand_x = random.randint(2, width-1)
        rand_y = random.randint(2, height-1)
        is_point_on_snake = s.is_point_on_snake([rand_x, rand_y])
    
    foods.append(Food(rand_x, rand_y))

def is_food_eaten():
    global score
    for food in foods:
        if food.x == s.head_pos[0] and food.y == s.head_pos[1]:
            score = score + 1
            s.grow_up()
            foods.remove(food)
            
            spawn_food()
            break

def pressed_up():
    if s.dir == [0, 1]: return
    s.dir = [0, -1]
    
def pressed_down():
    if s.dir == [0, -1]: return
    s.dir = [0, 1]
    
def pressed_left():
    if s.dir == [1, 0]: return
    s.dir = [-1, 0]
    
def pressed_right():
    if s.dir == [-1, 0]: return
    s.dir = [1, 0]

def redraw_all(win):
    clear_screen()
    print_borders()
    print_score()
    s.draw()
    for food in foods:
        food.draw()

def main(win):
    win.nodelay(True)
    key = ""
    print_borders()
    print_score()          
    spawn_food()
    while True:
        while True:
            try:                 
                key = win.getkey()
                if key == os.linesep:
                    break
                elif key.lower() == 'w':
                    pressed_up()
                elif key.lower() == 'a':
                    pressed_left()
                elif key.lower() == 's':
                    pressed_down()
                elif key.lower() == 'd':
                    pressed_right()
                            
            except Exception as e:
                break       

        s.tick()
        is_food_eaten()
        
        if s.head_pos[0] >= width or s.head_pos[1] >= height or s.head_pos[0] <= 1 or s.head_pos[1] <= 1:
            break
        if s.is_head_touching_tail():
            break

        redraw_all(win)
        time.sleep(0.5 / (1 + 0.13 * score))
     
    print_score()
    print_char(1, height+2, " Game over. Press enter to exit...")
    while True:
        try:                 
            key = win.getkey()
            if key == os.linesep:
                break
        except Exception as e:
            pass

curses.wrapper(main)