import curses
import os
import time
import random

width = 40
height = 15
score = 0
tick_time = 0.4

print('\033[?25l', end="")

stdscr = curses.initscr()

def clear_screen():
    os.system('clear')
    
def print_char(x, y, char):
    print("\033["+str(y)+";"+str(x)+"H"+char)
    #win.addstr(x, y, char)

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

snake = Snake()


class Foods:
    def __init__(self):
        self.foods = []
    
    def draw(self):
        for food in self.foods:
            print_char(food[0], food[1], '*')

    def spawn_food(self):
        is_point_on_snake = True
        rand_x = 0
        rand_y = 0
        while is_point_on_snake:
            rand_x = random.randint(2, width-1)
            rand_y = random.randint(2, height-1)
            is_point_on_snake = snake.is_point_on_snake([rand_x, rand_y])
        
        self.foods.append([rand_x, rand_y])

    def tick(self):
        self.process_eaten_food()

    def process_eaten_food(self):
        global score
        for food in self.foods:
            if food[0] == snake.head_pos[0] and food[1] == snake.head_pos[1]:
                score = score + 1
                snake.grow_up()
                self.foods.remove(food)
                self.spawn_food()

foods = Foods()


def pressed_up():
    if snake.dir != [0, 1]: snake.dir = [0, -1]
    
def pressed_down():
    if snake.dir != [0, -1]: snake.dir = [0, 1]
    
def pressed_left():
    if snake.dir != [1, 0]: snake.dir = [-1, 0]
    
def pressed_right():
    if snake.dir != [-1, 0]: snake.dir = [1, 0]

exit_pressed = False
def process_key_events(win):
    while True:
        try:                 
            key = win.getkey()
            if key == os.linesep:
                exit_pressed = True
                return 
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


def redraw_all():
    clear_screen()
    print_borders()
    print_score()
    snake.draw()
    foods.draw()


def show_exit(win):
    print_char(1, height+2, " Game over. Press enter to exit...")
    while True:
        try:                 
            key = win.getkey()
            if key == os.linesep:
                break
        except Exception as e:
            pass


def is_finish():
    if snake.head_pos[0] >= width or snake.head_pos[1] >= height or snake.head_pos[0] <= 1 or snake.head_pos[1] <= 1:
        return True
    if snake.is_head_touching_tail():
        return True
        
    return False


def init(win):
    win.nodelay(True)
    foods.spawn_food()
    redraw_all()

def sleep():
    speed_scale = (1 + 0.13 * score)
    time.sleep(tick_time / speed_scale)


def main(win):
    init(win)
    
    while True:
        process_key_events(win)
        if exit_pressed:
            break

        snake.tick()
        foods.tick()
        
        if is_finish():
            break

        redraw_all()
        sleep()

    show_exit(win)

curses.wrapper(main)