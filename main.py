import pygame
import time
import random as rnd


screenwidth = 500
width = 25
size = screenwidth // width

# initialise game
pygame.init()
screen = pygame.display.set_mode((screenwidth, screenwidth))
pygame.display.set_caption("Game window")


def draw_apple(x, y):
    r = rnd.randrange(100, 255)
    g = rnd.randrange(100, 255)
    b = rnd.randrange(100, 255)
    pygame.draw.rect(screen, (r, g, b), (x * width, y * width, width, width))


def draw_cube(x, y):
    pygame.draw.rect(screen, (255, 255, 255), (x * width, y * width, width, width))


def drawgrid(width):
    for i in range(screenwidth // width + 1):
        # draw horizontal lines
        pygame.draw.line(
            screen, (255, 255, 255), (0, i * width), (screenwidth, i * width)
        )
        # draw vertical lines
        pygame.draw.line(
            screen, (255, 255, 255), (i * width, 0), (i * width, screenwidth)
        )


def move_snake(L, R, U, D):
    global x, y
    if L:
        x -= 1
    if R:
        x += 1
    if U:
        y -= 1
    if D:
        y += 1


def apply_velocity(L, R, U, D, coords):
    x = coords[0]
    y = coords[1]
    if L:
        return (x - 1, y)
    if R:
        return (x + 1, y)

    if U:
        return (x, y - 1)

    if D:
        return (x, y + 1)


def get_position(size):
    x = rnd.randint(0, size - 1)
    y = rnd.randint(0, size - 1)
    return x, y


def check_eaten():
    global snake, apple_x, apple_y
    snakehead = snake[-1]
    return snakehead[0] == apple_x and snakehead[1] == apple_y


def cross_over():
    global snake
    for body in snake[:-1]:
        if body == snake[-1]:
            return False
    return True


def within_boundary():
    global snake
    x = snake[-1][0]
    y = snake[-1][1]
    return x >= 0 and x <= (size - 1) and y >= 0 and y <= (size - 1)


running = True

L = False
R = True
U = False
D = False


apple_x, apple_y = get_position(size)
x, y = get_position(size)
snake = [(x, y)]
snakelength = 1
applecount = 0
add_body = False


def update_snake():
    global snake, applecount, L, R, U, D, snakelength, add_body
    newsnake = snake[:]
    newhead = apply_velocity(L, R, U, D, snake[-1])
    newsnake.append(newhead)
    if add_body:
        add_body = False
    else:
        newsnake.pop(0)
    snake = newsnake


def draw_snake():
    global snake, screen
    for bodypart in snake:
        x = bodypart[0]
        y = bodypart[1]
        pygame.draw.rect(screen, (255, 255, 255), (x * width, y * width, width, width))


while running:
    # check if user closed the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if not U:
                    L = False
                    R = False
                    U = False
                    D = True
            if event.key == pygame.K_UP:
                if not D:
                    L = False
                    R = False
                    U = True
                    D = False
            if event.key == pygame.K_LEFT:
                if not R:
                    L = True
                    R = False
                    U = False
                    D = False
            if event.key == pygame.K_RIGHT:
                if not L:
                    L = False
                    R = True
                    U = False
                    D = False
    draw_cube(20, 20)
    # refresh screen
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 500, 500))
    # move_snake(L, R, U, D)
    draw_apple(apple_x, apple_y)
    update_snake()
    draw_snake()
    if check_eaten():
        applecount += 1
        add_body = True
        apple_x, apple_y = get_position(size)

    # update display
    time.sleep(0.05)
    if not within_boundary() or not cross_over():
        running = False
    pygame.display.flip()

pygame.quit()
