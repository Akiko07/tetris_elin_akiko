import pygame

class Tetris:
    height = 0
    width = 0
    field = []
    score= 0
    state = "start"

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




pygame.init()
screen = pygame.display.set_mode([400,500])
pygame.display.set_caption("Tetris")

done = False
fps = 25
clock = pygame.time.Clock()
counter = 0

game = Tetris(20, 10)
pressing_down = False
pressing_left = False
pressing_right = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
EGGSHELL = (238, 238, 228)



while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F:
                game.rotate()
            if event.key == pygame.K_S:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                pressing_left = True
            if event.key == pygame.K_RIGHT:
                pressing_right = True

        if pressing_down:
            game.down()
        if pressing_left:
            game.left()
        if pressing_right:
            game.right()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False

    screen.fill(color=EGGSHELL)
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [])

    clock.tick(fps)





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
pygame.quit()

