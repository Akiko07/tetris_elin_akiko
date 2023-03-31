import pygame



pygame.init()
screen = pygame.display.set_mode([400,500])
pygame.display.set_caption("Tetris")

done = False
fps = 25
clock = pygame.time.Clock()
counter = 0

game = Tetris()
pressing_down = False
pressing_left = False
pressing_right = False

BLACK = (0,0,0)
WHITE = (255,255,255)



while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
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

    screen.fill(color=)





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
pygame.quit()

