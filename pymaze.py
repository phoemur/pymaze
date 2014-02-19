#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Written by phoemur - dec/2013
# Thanks to Joe Wingbermuehle whoose maze generator ( https://raw.github.com/joewing/maze ) i was based on
#
 
import random, curses, sys
 
 
# The size of the maze (must be odd).
width = 39
height = 23
 
# The maze.
maze = dict()
 
# Initialize the maze.
def init_maze():
   for x in range(0, width):
      maze[x] = dict()
      for y in range(0, height):
         maze[x][y] = 1
 
# Carve the maze starting at x, y.
def carve_maze(x, y):
   dir = random.randint(0, 3)
   count = 0
   while count < 4:
      dx = 0
      dy = 0
      if dir == 0:
         dx = 1
      elif dir == 1:
         dy = 1
      elif dir == 2:
         dx = -1
      else:
         dy = -1
      x1 = x + dx
      y1 = y + dy
      x2 = x1 + dx
      y2 = y1 + dy
      if x2 > 0 and x2 < width and y2 > 0 and y2 < height:
         if maze[x1][y1] == 1 and maze[x2][y2] == 1:
            maze[x1][y1] = 0
            maze[x2][y2] = 0
            carve_maze(x2, y2)
      count = count + 1
      dir = (dir + 1) % 4
 
# Generate the maze.
def generate_maze():
   random.seed()
   maze[1][1] = 0
   carve_maze(1, 1)
   maze[1][0] = 0
   maze[width - 2][height - 1] = 0
 
# Display the maze.
def display_maze():
   stdscr.clear()
   stdscr.move(0,0)
   for y in range(0, height):
      for x in range(0, width):
         if maze[x][y] == 0:
            stdscr.addstr("  ", curses.color_pair(1))
         else:
            stdscr.addstr("[]", curses.color_pair(1))
      stdscr.addstr("\n", curses.color_pair(1))
      stdscr.refresh()
 
# Position Info
def display_info(a, b, counter):
   stdscr.addstr(height+1, 0, 'X Coordinate: {}'.format(str(b).zfill(4)), curses.A_BOLD)
   stdscr.addstr(height+2, 0, 'Y Coordinate: {}'.format(str(a).zfill(4)), curses.A_BOLD)
   stdscr.addstr(height+3, 0, 'Moves: {}'.format(str(counter).zfill(5)), curses.A_BOLD)
   stdscr.refresh()
 
# Display the Ball
def display_ball(y, x):
    stdscr.addstr(y,x, "OO", curses.color_pair(2))
    stdscr.refresh()
 
# Winner Funcion
def winner(counter):
    stdscr.clear()
    stdscr.addstr('Congratulations!!!\nYou won with {} moves\n\nPress any key for the next fase or Q to exit'.format(counter), curses.A_BOLD)
    stdscr.refresh()
    c = stdscr.getch()
    if chr(c).upper() == 'Q':
        sys.exit(0)
 
# Mainloop
def mainloop():
    #Movement Variables
    x = 1
    y = 0
    m = 2 # Wrapper for x position, as it has 2 spaces
    counter = 0 # Count movements
 
 
    # Initial position
    display_maze()
    display_info(y, x, counter)
    display_ball(y, m)
 
    #Loop
    entry = int()
    while True:
        entry = stdscr.getch()
 
        # Erase former position
        stdscr.addstr(y, m, "  ", curses.color_pair(2))
 
        try:
            if entry == curses.KEY_LEFT or entry == ord('a'):
                if maze[x-1][y] != 0:
                    pass
                else:
                    x -= 1
                    m -= 2
                    counter += 1
 
            if entry == curses.KEY_RIGHT or entry == ord('d'):
                if maze[x+1][y] != 0:
                    pass
                else:
                    x += 1
                    m += 2
                    counter += 1
 
            if entry == curses.KEY_UP or entry == ord('w'):
                if maze[x][y-1] != 0:
                    pass
                else:
                    y -= 1
                    counter += 1
 
            if entry == curses.KEY_DOWN or entry == ord('s'):
                if maze[x][y+1] != 0:
                    pass
                else:
                    y += 1
                    counter += 1
 
        except KeyError:
            pass
 
        if entry == ord('q'):
            sys.exit(0)
 
        display_info(y, x, counter)
        display_ball(y, m)
 
        # Tests if we have a winner
        if y == height - 1:
            winner(counter)
            break
 
 
def begin(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
 
    init_maze()
    generate_maze()
    mainloop()
 
if __name__ == '__main__':
    # Initializing the program
    curses.setupterm()
    stdscr = curses.initscr()
    curses.curs_set(False)
    stdscr.keypad(True)
 
    while width < curses.tigetnum('cols') and height+5 < curses.tigetnum('lines'):
        curses.wrapper(begin)
        width += 10
        height += 6
 
    curses.endwin()
    print("\nCongratulations, your screen is smaller than your skill\n\rFind a bigger screen to continue\n")