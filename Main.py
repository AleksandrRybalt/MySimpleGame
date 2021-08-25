import pygame
import Objects
import Engine

'''create game and window'''
pygame.init()
WIDTH = 1600
HEIGHT = 900
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MyFirstGame")
clock = pygame.time.Clock()


'''function to start a new game'''
def create_game():
    global HERO, ENGINE
    HERO = Objects.Hero()
    ENGINE = Engine.Engine(
        HERO, (WIDTH/4*3, HEIGHT/3*2), (WIDTH/4*3, HEIGHT/3), (WIDTH/4, HEIGHT/3), (WIDTH/4, HEIGHT/3*2)
                           )


'''function to draw the display'''
def draw_display():
    gameDisplay.blit(ENGINE.draw_map.game_window, (0, 0))
    gameDisplay.blit(ENGINE.interface.interface_window, (0, HEIGHT / 3 * 2))
    gameDisplay.blit(ENGINE.info.info_window, (WIDTH / 4 * 3, HEIGHT / 3 * 2))
    gameDisplay.blit(ENGINE.log.log_window, (WIDTH / 4 * 3, 0))


'''game loop'''
create_game()
running = True
while running:
    clock.tick(30)

    if ENGINE.working == False:
        create_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ENGINE.move_up()
            if event.key == pygame.K_DOWN:
                ENGINE.move_down()
            if event.key == pygame.K_LEFT:
                ENGINE.move_left()
            if event.key == pygame.K_RIGHT:
                ENGINE.move_right()
            if event.key == pygame.K_KP_PLUS:
                ENGINE.game_window_plus()
            if event.key == pygame.K_KP_MINUS:
                ENGINE.game_window_minus()

    draw_display()
    pygame.display.flip()

pygame.quit()
