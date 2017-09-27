

import tkinter
from tkinter import *
import random
import ctypes
import sys


def quit_game():
    top.destroy()
    sys.exit()


def is_valid_location(x, y):
    if x >= 0 and x < columns and y >= 0 and y < rows:
        return True
    return False


def is_open(x, y):
    return mine_map[x][y] > 0


def open_pad(x, y):
    if not is_valid_location(x, y):
        return

    if is_open(x, y):
        return

    mine_map[x][y] *= -1
    button = table[x][y]
    if mine_map[x][y] == MINE:
        button['bg'] = 'red'
        button['text'] = ''
        button['activebackground'] = 'red'
        ctypes.windll.user32.MessageBoxW(0, "You opened a mine pad",
                                         "You lost", 0)
        top.destroy()
    elif mine_map[x][y] == EMPTY_PAD:
        button['text'] = ' '
        button['bg'] = 'white'
        button['state'] = 'disable'
        if is_valid_location(x - 1, y) and mine_map[x - 1][y] != -MINE:
            open_pad(x - 1, y)
        if is_valid_location(x + 1, y) and mine_map[x + 1][y] != -MINE:
            open_pad(x + 1, y)
        if is_valid_location(x, y - 1) and mine_map[x][y - 1] != -MINE:
            open_pad(x, y - 1)
        if is_valid_location(x, y + 1) and mine_map[x][y + 1] != -MINE:
            open_pad(x, y + 1)
    else:
        button['text'] = mine_map[x][y]
        button['fg'] = "black"
        button['activebackground'] = 'black'


def generate_map(w, h, mine_probability=0.1):
    result_map = [[-EMPTY_PAD for x in range(columns)] for y in range(rows)]
    mine_locations = random.sample(range(w * h), int(0.1 * w * h))
    for i in mine_locations:
        result_map[i // w][i % w] = -MINE

    for x in range(0, w):
        for y in range(0, h):
            if result_map[x][y] != -MINE:
                count = 0
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if not is_valid_location(i, j) or (i == x and j == y):
                            continue
                        if result_map[i][j] == -MINE:
                            count += 1
                if count > 0:
                    result_map[x][y] = -count
                else:
                    result_map[x][y] = -EMPTY_PAD

    return result_map


# Constants
MINE = 9
EMPTY_PAD = 10

pad_width = 50
pad_height = 50
columns = 10
rows = 10

while True:
    mine_map = generate_map(columns, rows)

    top = tkinter.Tk()
    top.protocol('WM_DELETE_WINDOW', quit_game)
    top.geometry(str(columns * pad_width) + 'x' + str(rows * pad_height))
    top.title("MineSweeper")

    table = [[0 for x in range(columns)] for y in range(rows)]
    for i in range(0, columns * pad_width, pad_width):
        for j in range(0, rows * pad_height, pad_height):
            x = i // pad_width
            y = j // pad_height
            button = Button(top, bg='grey', width=6, height=3)
            button.configure(command=lambda x=x, y=y: open_pad(x, y))
            button.place(x=i, y=j)
            table[x][y] = button

    top.mainloop()
