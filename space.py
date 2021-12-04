import pygame
import os
from pygame.constants import KEYDOWN

pygame.font.init()

WIDTH = 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # initialize game window
FPS = 60
SHIP_WIDTH = 80
SHIP_HEIGHT = 50
STEP = 5
BULLET_SPEED = 7
MAX_BULLETS = 3
LEFT_END = 20
RIGHT_END = WIDTH - 100
UPPER_END = 0
LOWER_END = HEIGHT - SHIP_HEIGHT
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
LIVES = 5
LIVES_FONT = pygame.font.SysFont("comicsans", 30)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
pygame.display.set_caption("SpaceShooter")  # name of the game at top of the window

LEFT_SHIP_IMG = pygame.image.load("ship_left.png")
LEFT_SHIP = pygame.transform.scale(LEFT_SHIP_IMG, (SHIP_WIDTH, SHIP_HEIGHT))

RIGHT_SHIP_IMG = pygame.image.load("ship_right.png")
RIGHT_SHIP = pygame.transform.scale(RIGHT_SHIP_IMG, (SHIP_WIDTH, SHIP_HEIGHT))

SPACE_BG_IMG = pygame.image.load("Space_bg.jpg")
SPACE_BG = pygame.transform.scale(SPACE_BG_IMG, (WIDTH, HEIGHT))

LEFT_HIT = pygame.USEREVENT + 1
RIGHT_HIT = pygame.USEREVENT + 2


def draw_window(left, right, bullets_left, bullets_right, left_health, right_health):
    WIN.blit(SPACE_BG, (0, 0))
    left_text = LIVES_FONT.render("Health: " + str(left_health), 1, (255, 255, 255))
    right_text = LIVES_FONT.render("Health: " + str(right_health), 1, (255, 255, 255))
    WIN.blit(left_text, (10, 10))
    WIN.blit(right_text, (WIDTH - right_text.get_width() - 10, 10))
    pygame.draw.rect(WIN, (0, 0, 0), BORDER)
    WIN.blit(LEFT_SHIP, (left.x, left.y))
    WIN.blit(RIGHT_SHIP, (right.x, right.y))

    for bullet in bullets_left:
        pygame.draw.rect(WIN, (255, 0, 0), bullet)
    for bullet in bullets_right:
        pygame.draw.rect(WIN, (255, 255, 0), bullet)

    pygame.display.update()


def handle_input_left(keys_pressed, left):
    if keys_pressed[pygame.K_w] and left.y - STEP >= UPPER_END:
        left.y -= STEP
    if keys_pressed[pygame.K_a] and left.x - STEP >= LEFT_END:
        left.x -= STEP
    if keys_pressed[pygame.K_s] and left.y + STEP <= LOWER_END:
        left.y += STEP
    if keys_pressed[pygame.K_d] and left.x + STEP + SHIP_WIDTH <= BORDER.x - 5:
        left.x += STEP


def handle_input_right(keys_pressed, right):
    if keys_pressed[pygame.K_UP] and right.y - STEP >= UPPER_END:
        right.y -= STEP
    if keys_pressed[pygame.K_LEFT] and right.x - STEP >= BORDER.x + 15:
        right.x -= STEP
    if keys_pressed[pygame.K_DOWN] and right.y + STEP <= LOWER_END:
        right.y += STEP
    if keys_pressed[pygame.K_RIGHT] and right.x + STEP <= RIGHT_END:
        right.x += STEP


def handle_bullets(bullets_left, bullets_right, left, right):
    for bullet in bullets_left:
        bullet.x += BULLET_SPEED
        if right.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RIGHT_HIT))
            bullets_left.remove(bullet)
        elif bullet.x >= WIDTH:
            bullets_left.remove(bullet)

    for bullet in bullets_right:
        bullet.x -= BULLET_SPEED
        if left.colliderect(bullet):
            pygame.event.post(pygame.event.Event(LEFT_HIT))
            bullets_right.remove(bullet)
        elif bullet.x <= 0:
            bullets_right.remove(bullet)


def handle_win(text):
    draw_text = WINNER_FONT.render(text, 1, (255, 255, 255))
    WIN.blit(
        draw_text,
        (
            WIDTH // 2 - draw_text.get_width() // 2,
            HEIGHT // 2 - draw_text.get_height() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    left = pygame.Rect(20, HEIGHT // 2, SHIP_WIDTH, SHIP_HEIGHT)
    right = pygame.Rect(WIDTH - 100, HEIGHT // 2, SHIP_WIDTH, SHIP_HEIGHT)
    winner = ""
    left_health = LIVES
    right_health = LIVES
    bullets_left = []
    bullets_right = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_q and len(bullets_left) < MAX_BULLETS:
                    bullet = pygame.Rect(left.x + left.width, left.y + 35, 10, 5)
                    bullets_left.append(bullet)
                if event.key == pygame.K_m and len(bullets_right) < MAX_BULLETS:
                    bullet = pygame.Rect(right.x, right.y + 35, 10, 5)
                    bullets_right.append(bullet)
            if event.type == LEFT_HIT:
                left_health -= 1
                if left_health <= 0:
                    winner = "Right Player Wins!"
            if event.type == RIGHT_HIT:
                right_health -= 1
                if right_health <= 0:
                    winner = "Left Player Wins!"

        keys_pressed = pygame.key.get_pressed()
        handle_input_left(keys_pressed, left)
        handle_input_right(keys_pressed, right)
        handle_bullets(bullets_left, bullets_right, left, right)
        draw_window(left, right, bullets_left, bullets_right, left_health, right_health)

        if winner != "":
            handle_win(winner)
            break

    main()


if __name__ == "__main__":
    main()
