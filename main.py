import pygame
from random import randrange

SCREEN_WIDTH = 10
SCREEN_HEIGHT = 24

BLOCK_SIZE = 30

COLORS = ["#272727", "#65afff", "#ffc100", "#820933", "#139a43",
          "#b20d30", "#2b50aa", "#f75c03", "#8d909b"]
MOVE_SPEED = 10
SHAPES = (
    [[' ', ' ', ' ', ' '],  # ____
     ['1', '1', '1', '1'],
     [' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ']],
    [['7', ' ', ' '],  # |__
     ['7', '7', '7'],
     [' ', ' ', ' ']],
    [[' ', ' ', '6'],  # __|
     ['6', '6', '6'],
     [' ', ' ', ' ']],
    [['2', '2'],
     ['2', '2']],
    [[' ', '4', '4'],
     ['4', '4', ' '],
     [' ', ' ', ' ']],
    [[' ', '3', ' '],
     ['3', '3', '3'],
     [' ', ' ', ' ']],
    [['5', '5', ' '],
     [' ', '5', '5'],
     [' ', ' ', ' ']]

)

BG_COLOR = COLORS[0]
FPS = 60

game_over = 0
score = 0
level = 0
level_counter = 0

candidate = SHAPES[randrange(len(SHAPES))]

victory = 1
game_loop = 0
speed = 48
one_row = []
for x in range(SCREEN_WIDTH + 2):
    if x == 0 or x == SCREEN_WIDTH + 1:
        one_row.append('8')
        continue
    one_row.append(' ')
# Creating bounds of space
clear_map = []
for y in range(SCREEN_HEIGHT + 2):
    row = []
    if y == SCREEN_HEIGHT + 1:
        row = ['8' for i in range(SCREEN_WIDTH + 2)]
        clear_map.append(row)
        continue

    clear_map.append(one_row.copy())
b_map = clear_map.copy()


def move_one_row(matrix, y):
    new_matrix = [one_row.copy()]
    new_matrix.extend(matrix[:y])
    new_matrix.extend(matrix[y + 1:])
    return new_matrix


def add(b_map, matrix, offest):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == ' ':
                continue
            b_map[y + offest[1]][x + offest[0]] = matrix[y][x]


def draw_block(x, y, char):
    if char != ' ':
        rect1 = pygame.Rect((x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1),
                            (BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        rect2 = pygame.Rect((x * BLOCK_SIZE, y * BLOCK_SIZE),
                            (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, COLORS[0], rect2)
        pygame.draw.rect(screen, COLORS[int(char)], rect1)


def draw_map(b_map, offest):
    for y in range(len(b_map)):
        for x in range(len(b_map[y])):
            draw_block(x + offest[0], y + offest[1], b_map[y][x])


class Tetromino:
    """It's just... tetromino!"""

    def __init__(self, position):
        global candidate
        self.matrix = candidate
        candidate = SHAPES[randrange(len(SHAPES))]
        self.position = list(position)

        self.fall_tick = 0
        self.move_tick = 0
        self.blocked_up = 0
        self.blocked_down = 0
        self.blocked_right = 0
        self.blocked_left = 0
        self.type = self.matrix[1][1]

    def draw(self, screen, is_key, b_map):
        global candidate
        self.blocked_right = self.blocked_left = self.blocked_up = self.blocked_down = 0
        self.fall_tick += 1
        self.move_tick -= bool(self.move_tick)
        max_tick = speed
        key = pygame.key.get_pressed()
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x] == ' ':
                    continue
                x_pos = self.position[0] + x
                y_pos = self.position[1] + y

                if b_map[y_pos][x_pos - 1] != ' ':
                    self.blocked_left += 1 + \
                        (self.type == '5' or self.type == '4')
                if b_map[y_pos][x_pos + 1] != ' ':
                    self.blocked_right += 1 + \
                        (self.type == '5' or self.type == '4')
                if b_map[y_pos - 1][x_pos] != ' ':
                    self.blocked_up = 1
                if b_map[y_pos + 1][x_pos] != ' ':
                    self.blocked_down = 1

        if key[pygame.K_RIGHT] and not self.blocked_right and not self.move_tick:
            self.position[0] += 1
            self.move_tick = MOVE_SPEED
        if key[pygame.K_LEFT] and not self.blocked_left and not self.move_tick:
            self.position[0] -= 1
            self.move_tick = MOVE_SPEED
        if key[pygame.K_DOWN]:
            max_tick = int(max_tick / 10)
        if key[pygame.K_z] and is_key and \
                not self.blocked_up and \
                not self.blocked_down and \
                not self.blocked_left > 2 and\
                not self.blocked_right > 2:
            self.rotate(0)

            if self.type == '1' and self.position[0] == SCREEN_WIDTH - 2 and self.matrix[1][3] != self.matrix[2][3] != ' ':
                self.position[0] -= 1
        if key[pygame.K_x] and is_key and \
                not self.blocked_up and \
                not self.blocked_down and \
                not self.blocked_left > 2 and\
                not self.blocked_right > 2:
            self.rotate(1)
            if self.type == '1' and self.position[0] == SCREEN_WIDTH - 2 and self.matrix[1][3] != self.matrix[2][3] != ' ':
                self.position[0] -= 1
        if self.fall_tick >= max_tick:
            if self.blocked_down:
                if self.position[1] == 0:
                    global game_over
                    game_over = 1

                add(b_map, self.matrix, self.position)
                self.matrix = candidate
                candidate = SHAPES[randrange(len(SHAPES))]
                self.position = [4, 0]

                self.fall_tick = 0
                self.move_tick = 0
                self.blocked_up = 0
                self.blocked_down = 0
                self.blocked_right = 0
                self.blocked_left = 0
                self.blocked_down = 0
                self.type = self.matrix[1][1]
                return
            self.fall_tick = 0
            self.position[1] += 1
        draw_map(self.matrix, self.position)

    def rotate(self, direction):
        if direction:
            self.matrix = list(zip(*self.matrix[::-1]))
        else:
            self.matrix = list(zip(*self.matrix))[::-1]


tetr = Tetromino((4, 0))


pygame.init()
screen = pygame.display.set_mode(
    ((SCREEN_WIDTH + 10) * BLOCK_SIZE, (SCREEN_HEIGHT + 2) * BLOCK_SIZE))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

tick = 0
indexes_to_remove = []

font = pygame.font.SysFont('mallana.ttf', 36)

rect1 = pygame.Rect(14 * BLOCK_SIZE, 2 * BLOCK_SIZE,
                    4 * BLOCK_SIZE, 2 * BLOCK_SIZE)
rect2 = pygame.Rect(15 * BLOCK_SIZE, 6 * BLOCK_SIZE,
                    2 * BLOCK_SIZE, 2 * BLOCK_SIZE)
rect3 = pygame.Rect(13 * BLOCK_SIZE, 10 * BLOCK_SIZE,
                    6 * BLOCK_SIZE, 5 * BLOCK_SIZE)

running = True


def main():
    if game_over:
        return False
    global b_map
    global tick
    global indexes_to_remove
    global speed
    global score
    global level_counter
    global level
    is_key = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            return False
        elif event.type == pygame.KEYDOWN:
            is_key = True

    screen.fill(BG_COLOR)
    tetr.draw(screen, is_key, b_map)
    text1 = font.render(str(score), True, COLORS[0])
    text2 = font.render(str(level), True, COLORS[0])
    text3 = font.render('Next:', True, COLORS[0])

    pygame.draw.rect(screen, COLORS[-1], rect1)
    screen.blit(text1, (14 * BLOCK_SIZE + 10, 2 * BLOCK_SIZE + 20))
    pygame.draw.rect(screen, COLORS[-1], rect2)
    screen.blit(text2, (15 * BLOCK_SIZE + 22, 6 * BLOCK_SIZE + 20))
    pygame.draw.rect(screen, COLORS[-1], rect3)
    screen.blit(text3, (14 * BLOCK_SIZE + 20, 10 * BLOCK_SIZE + 5))
    draw_map(candidate, (14, 12))

    for y in b_map[:-1]:
        is_filled = 1
        for x in y:
            if x == ' ':
                is_filled = 0

        if is_filled:
            index = b_map.index(y)
            indexes_to_remove.append(index)
            b_map[index] = one_row.copy()
            tick = 15
    tick -= bool(tick)
    if tick == 1:
        for index in indexes_to_remove:
            b_map = move_one_row(b_map, index)
        level_counter += len(indexes_to_remove)
        if level_counter % 10 == 0:
            level += 1
            speed -= 1
        if level == 12:
            victory = 1
            return False
        if len(indexes_to_remove) == 1:
            score += 40 * (level + 1)
            print('YEY!')
        if len(indexes_to_remove) == 2:
            score += 100 * (level + 1)
            print("Double!")
        if len(indexes_to_remove) == 3:
            score += 300 * (level + 1)
            print("Triple!")
        if len(indexes_to_remove) == 4:
            score += 1200 * (level + 1)
            print('TETRIS!!!')
        indexes_to_remove = []

    draw_map(b_map, (0, 0))
    pygame.display.flip()
    pygame.display.set_caption('Tetris, FPS: %i' % clock.get_fps())
    clock.tick(FPS)
    return True


while main():
    pass

pygame.quit()
