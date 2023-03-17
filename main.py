import pygame
import random

# initialize pygame
pygame.init()

# set up the screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Blaster")

# set up the game clock
clock = pygame.time.Clock()

# set up the game variables
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 5
player_size = 50
player_bullet_speed = 10
player_bullets = []
enemy_speed = 5
enemy_size = 50
enemies = []
enemy_bullet_speed = 5
enemy_bullets = []
score = 0
game_over = False

# set up the fonts
font = pygame.font.Font(None, 36)

# load the images
player_image = pygame.Surface((player_size, player_size))
player_image.fill((0, 255, 0))
enemy_image = pygame.Surface((enemy_size, enemy_size))
enemy_image.fill((255, 0, 0))
bullet_image = pygame.Surface((5, 10))
bullet_image.fill((255, 255, 255))


# game loop
while not game_over:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_bullets.append([player_x + player_size // 2, player_y])

    # update the player position
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # update the player bullets
    for bullet in player_bullets:
        bullet[1] -= player_bullet_speed
        if bullet[1] < 0:
            player_bullets.remove(bullet)
        else:
            for enemy in enemies:
                if bullet[0] > enemy[0] and bullet[0] < enemy[0] + enemy_size and bullet[1] > enemy[1] and bullet[1] < enemy[1] + enemy_size:
                    enemies.remove(enemy)
                    player_bullets.remove(bullet)
                    score += 10

    # update the enemies
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)
        else:
            if random.randint(1, 50) == 1:
                enemy_bullets.append([enemy[0] + enemy_size // 2, enemy[1] + enemy_size])

    # update the enemy bullets
    for bullet in enemy_bullets:
        bullet[1] += enemy_bullet_speed
        if bullet[1] > HEIGHT:
            enemy_bullets.remove(bullet)
        elif bullet[0] > player_x and bullet[0] < player_x + player_size and bullet[1] > player_y and bullet[1] < player_y + player_size:
            game_over = True

    # spawn a new enemy if necessary
    if len(enemies) < 5:
        enemies.append([random.randint(0, WIDTH - enemy_size), -enemy_size])

    # draw everything
    screen.fill((0, 0, 0))
    for bullet in player_bullets:
        pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], 5, 10))
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], 5, 10))
    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))
    screen.blit(player_image, (player_x, player_y))
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # update the display
    pygame.display.update()

    # tick the clock
    clock.tick(60)

# quit pygame
pygame.quit()
