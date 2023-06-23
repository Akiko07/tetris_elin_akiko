import pygame
import random

pygame.init()

colors = [
    (0,0,0),
    (204,236,238), # 4 in einer Reihe
    (117,137,191), # Reverse L
    (253,202,162), # L
    (255,250,129), # Block
    (224,240,118), # S
    (193,179,215), # T
    (247,140,182) # Reverse S
]

SoundBackground = pygame.mixer.Sound("Sounds\\Sounds_music.ogg")

SoundRotate = pygame.mixer.Sound("Sounds\\Sounds_rotate.ogg")

SoundClear = pygame.mixer.Sound("Sounds\\Sounds_clear.ogg")

icon = pygame.image.load("icon2.png")
pygame.display.set_icon(icon)

class Figure:
    x = 0
    y = 0

    Figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # 4 in einer Reihe
        [[0, 4, 5, 6], [1, 2, 5, 9], [1, 5, 9, 8], [4, 5, 6, 10]],  # Reverse L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
        [[1, 2, 5, 6]],  # Block
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
        [[4, 5, 9, 10], [2, 6, 5, 9]]  # Rrverse S
    ]

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.type = random.randint(0, len(self.Figures)-1)
        self.color = colors[self.type+1]
        self.rotation = 0

    def image(self):
        return self.Figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.Figures[self.type])

class Tetris:
    height = 0
    width = 0
    field = []
    score = 0
    state = "start"
    Figure = None

    def __init__(self, _height, _width):
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)
        self.new_figure()
        self.high_score = 0
        self.high_score = self.load_high_score()

    def new_figure(self):
        self.Figure = Figure(3, 0)

    def go_down(self):
        self.Figure.y += 1
        if self.intersects():
            self.Figure.y -= 1
            self.freeze()

    def side(self, dx):
        old_x = self.Figure
        edge = False
        for i in range (4):
            for j in range (4):
                p = i * 4 + j
                if p in self.Figure.image():
                    if j + self.Figure.x + dx > self.width -1 or \
                        j + self.Figure.x + dx < 0:
                        edge = True
        if not edge:
            self.Figure.x += dx
        if self.intersects():
            self.Figure.x = old_x

    def left(self):
        self.side(-1)

    def right(self):
        self.side(1)

    def down(self):
        while not self.intersects():
            self.Figure.y += 1
        self.Figure.y -= 1
        self.freeze()

    def rotate(self):
        old_rotation = self.Figure.rotation
        self.Figure.rotate()
        if self.intersects():
            self.Figure.rotation = old_rotation

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    if i + self.Figure.y > self.height - 1 or \
                        i + self.Figure.y < 0 or \
                        self.field[i + self.Figure.y][j + self.Figure.x] > 0:
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if  p in self.Figure.image():
                    self.field[i + self.Figure.y][j + self.Figure.x] = self.Figure.type+1
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"



    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i2 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i2][j] = self.field[i2 - 1][j]
        self.score += lines ** 2

        if lines > 0:
            SoundClear.set_volume(1)
            pygame.mixer.Sound.play(SoundClear)

            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))



pygame.init()
screen = pygame.display.set_mode((700, 670))
pygame.display.set_caption("Tetris")

done = False
fps = 2.5
clock = pygame.time.Clock()
counter = 0
zoom = 30

game = Tetris(20, 10)
pressing_down = False
pressing_left = False
pressing_right = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

while not done:
    if game.state == "start":
        game.go_down()

    pygame.mixer.Sound.play(SoundBackground)
    SoundBackground.set_volume(0.5)
    SoundBackground.play(-1)



    SoundBackground.set_volume(2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game.state == "gameover":
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_pos):
                    game = Tetris(20, 10)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
                pygame.mixer.Sound.play(SoundRotate)
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                pressing_left = True
            if event.key == pygame.K_RIGHT:
                pressing_right = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False

        if pressing_down:
            game.down()
        if pressing_left:
            game.left()
        if pressing_right:
            game.right()


    screen.fill(color = WHITE)
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] == 0:
                color = GRAY
                just_border = 1
            else:
                color = colors[game.field[i][j]]
                just_border = 0
            pygame.draw.rect(screen, color, [30+j*zoom, 30+i*zoom, zoom, zoom], just_border)


    if game.Figure is not None:
        for i in range(4):
            for j in range(4):
                p= i * 4 + j
                if p in game.Figure.image():
                    pygame.draw.rect(screen, game.Figure.color,
                                     [30+(j + game.Figure.x)* zoom, 30+(i + game.Figure.y) * zoom, zoom, zoom])

    if game.state == "gameover":
        # Displaying the "Restart" button
        restart_button_rect = pygame.Rect(450, 500, 100, 100)
        pygame.draw.rect(screen, (0, 0, 0), restart_button_rect)

        font = pygame.font.SysFont('Calibri', 21)
        text = font.render("Neu starten", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = restart_button_rect.center
        screen.blit(text, text_rect)

        # Checking for user interaction
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    game = Tetris(20, 10)

    gameover_font = pygame.font.SysFont('Calibri', 65, True, False)
    text_gameover = gameover_font.render("Game Over!", True, (0, 0, 0))

    if game.state == "gameover":
        SoundBackground.stop()
        screen.blit(text_gameover, [20, 250])

    score_font = pygame.font.SysFont('Calibri', 25, True, False)
    text_score = gameover_font.render("Score: " + str(game.score), True, (0, 0, 0))
    screen.blit(text_score, [400, 100])

    high_score_font = pygame.font.SysFont('Calibri', 25, True, False)
    text_high_score = high_score_font.render("High Score: " + str(game.high_score), True, (0, 0, 0))
    screen.blit(text_high_score, [400, 200])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
