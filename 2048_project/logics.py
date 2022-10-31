import random
import copy
import os

def pretty_print(mas):
    for row in mas:
        print(*row)

def get_number_from_index(i, j):
    return i * 4 + j + 1

def is_zero_in_mas(mas):
    for row in mas:
        if 0 in row:
            return True
    return False

def get_index_from_number(num):
    num -= 1
    x, y = num // 4, num % 4
    return x, y

def insert_2_of_4(mas, x, y):
    if random.random() <= 0.75:
        mas[x][y] = 2
    else:
        mas[x][y] = 4
    return mas    

def get_empty_list(mas):
    empty = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                num = get_number_from_index(i, j)
                empty.append(num)
    return empty

def move_left(mas: list):
    origin = copy.deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if mas[i][j] == mas[i][j+1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j+1)
                mas[i].append(0)
    return mas, delta, not origin == mas

def move_right(mas):
    origin = copy.deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if mas[i][j] == mas[i][j - 1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j-1)
                mas[i].insert(0, 0)
    return mas, delta, not origin == mas

def trans(m):
    res = []
    for i in range(len(m[0])):
        buf = []
        for row in m:
            buf.append(row[i])
        res.append(buf)
    return res

def move_up(mas):
    mas = trans(mas)
    mas, delta, origin = move_left(mas)
    mas = trans(mas)
    return mas, delta, origin

def move_down(mas):
    mas = trans(mas)
    mas, delta, origin = move_right(mas)
    mas = trans(mas)
    return mas, delta, origin

def can_move(mas):
    for i in range(3):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] or mas[i][j] == mas[i + 1][j]:
                return True
    for i in range(1, 4):
        for j in range(1, 4):
            if mas[i][j] == mas[i - 1][j] or mas[i][j] == mas[i][j - 1]:
                return True
    return False