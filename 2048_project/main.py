import sys
import pygame
from logics import *
from database import *

GAMERS_DB = get_best()

def init_const():
    global mas, score
    mas = [ [0] * 4 for i in range(4) ]
    score = 0
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    mas = insert_2_of_4(mas, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    mas = insert_2_of_4(mas, x2, y2)

def draw_top_gamers():
    font_top = pygame.font.SysFont('simsun', 30)
    font_gamer = pygame.font.SysFont('simsun', 24)
    text_head = font_top.render('Best tries: ', True, COLOR_TEXT)
    screen.blit(text_head, (250, 5))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f'{index + 1}. {name} - {score}'
        text_gamer = font_gamer.render(s, True, COLOR_TEXT)
        screen.blit(text_gamer, (250, 30 + 30 * index))

def draw_interface(score, delta = 0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)  
    font = pygame.font.SysFont('stxingkai', 70)
    font_score = pygame.font.SysFont('simsun', 42)
    font_delta = pygame.font.SysFont('simsun', 30)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_score_value = font_score.render(f'{score}', True, COLOR_TEXT)
    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (175, 35))
    if delta > 0:
        text_delta = font_delta.render(f' + {delta}', True, COLOR_TEXT)
        screen.blit(text_delta, (135, 75))
    pretty_print(mas)
    draw_top_gamers()
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * SIZE_BLOCK + (column + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))

mas = None

COLOR_TEXT = (255, 127, 0)
COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 128, 255),
    32: (255, 0, 255),
    64: (255, 0, 128),
    128: (255, 0, 0),
    256: (128, 255, 255),
    512: (128, 255, 128),
    1024: (128, 255, 0),
    2048: (128, 128, 255)
}

USERNAME = None
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
BLACK = (0, 0, 0)
BLOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGTH = WIDTH + 110
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)
score = None
init_const()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption('2048')

def draw_intro():
    img2028 = pygame.image.load('2048_project\\dog.jpg')
    font = pygame.font.SysFont('stxingkai', 72)
    text_welcome = font.render('Welcome!', True, WHITE)
    name = 'Введите имя'
    is_find_name = False
    while not is_find_name:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Введите имя':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    if name == 'Введите имя':
                        name = ''
                    else:
                        name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    global USERNAME
                    if len(name) > 2 and name != 'Введите имя':
                        USERNAME = name
                        is_find_name = True
                        break
                    else:
                        USERNAME = 'Чмо'
                        is_find_name = True
                        break
        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2028, (200, 250)), (10, 10))
        screen.blit(text_welcome, (235, 120))
        screen.blit(text_name, rect_name)
        pygame.display.update()

def game_loop():
    global score, mas
    draw_interface(score)
    pygame.display.update()

    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta = move_down(mas)
                if is_zero_in_mas(mas):
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    mas = insert_2_of_4(mas, x, y)
                    print(f'Мы заполнили элемент под номером {random_num}')
                score += delta
                draw_interface(score, delta)
                pygame.display.update()
    screen.fill(BLACK)

def draw_game_over():
    global USERNAME, mas
    img2028 = pygame.image.load('2048_project\\dog.jpg')
    font = pygame.font.SysFont('stxingkai', 65)
    text_game_over = font.render('Game over!', True, WHITE)
    text_score = font.render(f'Вы набрали {score}', True, WHITE)
    text = 'Рекорд побит'
    text_record = font.render(text, True, WHITE)
    best_score = GAMERS_DB[0][1]
    if score > best_score:
        text = 'Рекорд побит'
    else:
        text = f'Рекорд {best_score}'
    text_record = font.render(text, True, WHITE)
    insert_result(USERNAME, score)
    make_disicion = False
    while not make_disicion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_disicion = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    USERNAME = None
                    make_disicion = True
                    init_const()
        screen.blit(text_game_over, (220, 120))
        screen.blit(text_score, (55, 300))
        screen.blit(text_record, (55, 350))
        screen.blit(pygame.transform.scale(img2028, (200, 250)), (10, 10))
        pygame.display.update()
    screen.fill(BLACK)

while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_game_over()