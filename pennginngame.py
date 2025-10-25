import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 1024, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 背景と地面
background = pygame.image.load("haikeikoori.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

ground_img = pygame.image.load("zimennkoori2.png").convert_alpha()
ground_img = pygame.transform.scale(ground_img, (1030, 170))
ground_img2 = pygame.image.load("zimenn2.png").convert_alpha()
ground_img2 = pygame.transform.scale(ground_img2, (1030, 170))
ground_rect = pygame.Rect(0, 700, 1030, 170)
ground_x = 0

# プレイヤー
player = pygame.Rect(105, 630, 50, 65)
player_speed_y = 0
gravity = 0.2
jump_power = -8
on_ground = True

player_img1 = pygame.image.load("pennginn1.png").convert_alpha()
player_img1 = pygame.transform.scale(player_img1, (80, 80))
player_img2 = pygame.image.load("pennginn1.png").convert_alpha()
player_img2 = pygame.transform.scale(player_img2, (80, 80))
walk_count = 0
walk_switch = False
flip_switch = False

# 敵（クマ）
enemy_img1 = pygame.image.load("tekikuma1.png").convert_alpha()
enemy_img1 = pygame.transform.scale(enemy_img1, (80, 80))
enemy_img2 = pygame.image.load("tekikuma2.png").convert_alpha()
enemy_img2 = pygame.transform.scale(enemy_img2, (80, 80))

enemy_x = None
enemy_y = None
enemy_dir = 0
enemy_timer = 0

# ゴールと結果画像
goal_img = pygame.image.load("go-ru.png").convert_alpha()
goal_img = pygame.transform.scale(goal_img, (250, 300))

gameover_img = pygame.image.load("gameover.png").convert_alpha()
gameover_img = pygame.transform.scale(gameover_img, (600, 300))
clear_img = pygame.image.load("clear.png").convert_alpha()
clear_img = pygame.transform.scale(clear_img, (600, 180))

game_over = False
game_clear = False

LEFT_LIMIT = 200
RIGHT_LIMIT = WIDTH - 700 - player.width
MOVE_SPEED = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    # プレイヤーの移動とアニメーション
    if not game_over and not game_clear:
        move_x = 0
        if keys[pygame.K_a] and (player.x > LEFT_LIMIT or ground_x < 0):
            move_x = 0
        if keys[pygame.K_d]:
            move_x = 0

        # アニメーション制御
        if move_x != 0:
            walk_count += 1
            if walk_count % 10 == 0:
                walk_switch = not walk_switch
        else:
            walk_count = 0
            walk_switch = False

        if move_x < 0:
            flip_switch = True
        elif move_x > 0:
            flip_switch = False

        # キャラ or 背景を移動
        if (move_x < 0 and player.x > LEFT_LIMIT) or (move_x > 0 and player.x < RIGHT_LIMIT):
            player.x += move_x
        else:
            ground_x -= move_x

        if keys[pygame.K_SPACE] and on_ground:
            
            on_ground = False

        screen.blit(background, (0, 0))
        enemy_rect = None
        for i in range(5):
            x_offset = ground_rect.x + ground_x + i * ground_rect.width
            if i % 2 == 0:
                screen.blit(ground_img, (x_offset, ground_rect.y))
            else:
                screen.blit(ground_img2, (x_offset, ground_rect.y))

            if i == 2:
                if enemy_x is None or enemy_y is None:
                    enemy_x = x_offset + ground_rect.width - enemy_img1.get_width()
                    enemy_y = ground_rect.y - enemy_img1.get_height() + 15

                enemy_timer += 1
                if enemy_timer >= 30:
                    enemy_dir = random.choice([-1, 0, 1])
                    enemy_timer = 0

                enemy_x += enemy_dir * 10
                enemy_x = max(x_offset, min(enemy_x, x_offset + ground_rect.width - 80))
                enemy_img = enemy_img2 if enemy_dir != 0 else enemy_img1

                screen.blit(enemy_img, (enemy_x, enemy_y))
                enemy_rect = pygame.Rect(enemy_x + 5, enemy_y + 5, 70, 70)

        # ゴール
        goal_x = ground_rect.x + ground_x + 4 * ground_rect.width + ground_rect.width - goal_img.get_width() // 2 - 50
        goal_y = ground_rect.y - goal_img.get_height()
        screen.blit(goal_img, (goal_x, goal_y))
        goal_rect = pygame.Rect(goal_x, goal_y, goal_img.get_width(), goal_img.get_height())

        # 重力とジャンプ
        player_speed_y += gravity
        player.y += player_speed_y
        on_ground = False

        for i in range(0, 5, 2):
            rect = ground_rect.move(ground_x + i * ground_rect.width, 0)
            if player.colliderect(rect) and player_speed_y >= 0:
                player.y = rect.y - player.height
                player_speed_y = 0
                on_ground = True

        for i in range(1, 5, 2):
            x = ground_rect.x + ground_x + i * ground_rect.width
            rect_left = pygame.Rect(x, ground_rect.y, 650, ground_rect.height)
            rect_right = pygame.Rect(x + 900, ground_rect.y, 130, ground_rect.height)
            for rect in [rect_left, rect_right]:
                if player.colliderect(rect) and player_speed_y >= 0:
                    player.y = rect.y - player.height
                    player_speed_y = 0
                    on_ground = True

        if player.y > HEIGHT:
            game_over = True
        if player.colliderect(goal_rect):
            game_clear = True
        if enemy_rect and player.colliderect(enemy_rect):
            game_over = True

        if walk_switch:
            if not flip_switch:
                screen.blit(player_img2, (player.x - 5, player.y - 10))
            else:
                screen.blit(pygame.transform.flip(player_img2, True, False), (player.x - 5, player.y - 10))
        else:
            if not flip_switch:
                screen.blit(player_img1, (player.x - 5, player.y - 10))
            else:
                screen.blit(pygame.transform.flip(player_img1, True, False), (player.x - 5, player.y - 10))

    else:
        screen.blit(background, (0, 0))
        for i in range(5):
            x_offset = ground_rect.x + ground_x + i * ground_rect.width
            screen.blit(ground_img if i % 2 == 0 else ground_img2, (x_offset, ground_rect.y))
            if i == 2 and enemy_x is not None and enemy_y is not None:
                screen.blit(enemy_img, (enemy_x, enemy_y))
        screen.blit(goal_img, (goal_x, goal_y))
        if game_over:
            screen.blit(gameover_img, gameover_img.get_rect(center=(WIDTH//2, HEIGHT//2)))
        else:
            screen.blit(clear_img, clear_img.get_rect(center=(WIDTH//2, HEIGHT//2)))
        if keys[pygame.K_r]:
            player.x, player.y = 105, 630
            player_speed_y = 0
            ground_x = 0
            enemy_x = None
            enemy_y = None
            enemy_dir = 0
            enemy_timer = 0
            game_over = False
            game_clear = False

    pygame.display.update()
    clock.tick(60)