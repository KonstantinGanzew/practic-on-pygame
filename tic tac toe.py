import pygame

pygame.init()


def check_win(field, sign: str):
    zeroes = 0
    for row in field:
        zeroes += row.count(0)
        if row.count(sign) == 3:
            return sign
    for col in range(3):
        if field[0][col] == sign and field[1][col] == sign and field[2][col] == sign:
            return sign
    if field[0][0] == sign and field[1][1] == sign and field[2][2] == sign:
        return sign

    if field[0][2] == sign and field[1][1] == sign and field[2][0] == sign:
        return sign
    if zeroes == 0:
        return 'Piece'
    return False


size_block = 100
margin = 15
width = height = size_block * 3 + margin * 4

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
mas = [[0] * 3 for i in range(3)]

size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Крестики-нолики')
query = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            column = x_mouse // (margin + size_block)
            row = y_mouse // (margin + size_block)
            if query % 2 == 0:
                mas[row][column] = 'x'
            else:
                mas[row][column] = 'o'
            query += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            game_over = False
            mas = [[0] * 3 for i in range(3)]
            query = 0
            screen.fill(BLACK)

    for col in range(3):
        for row in range(3):
            if mas[row][col] == 'x':
                color = RED
            elif mas[row][col] == 'o':
                color = GREEN
            else:
                color = WHITE
            x = col * size_block + (col + 1) * margin
            y = row * size_block + (row + 1) * margin
            pygame.draw.rect(screen, color, (x, y, size_block, size_block))
            if color == RED:
                pygame.draw.line(screen, WHITE, (x + 5, y + 5), (x + size_block - 5, y + size_block - 5), 3)
                pygame.draw.line(screen, WHITE, (x + size_block - 5, y + 5), (x + 5, y + size_block - 5), 3)
            elif color == GREEN:
                pygame.draw.circle(screen, WHITE, (x + size_block // 2, y + size_block // 2), size_block // 2 - 3, 3)

    if (query - 1) % 2 == 0:
        game_over = check_win(mas, 'x')
    else:
        game_over = check_win(mas, 'o')

    if game_over:
        screen.fill(BLACK)
        font = pygame.font.SysFont('stxingkai', 80)
        text1 = font.render(game_over, True, WHITE)
        text_rect = text1.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text1, [text_x, text_y])

    pygame.display.update()
