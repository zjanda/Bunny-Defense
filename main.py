# Import library
import pygame
from pygame.locals import *
import math
import random

# 2 - Initialize the game
pygame.init()
width, height = 640, 400
screen = pygame.display.set_mode((width, height))

keys = [False, False, False, False]
powerUpPosition = [100, 400]
poweredUp = False
powerUpRemaining = 0
accuracy = [0, 0]
arrows = []
kills = 0

# Badger Variables
badTimer = 100
badTimer1 = 0
badTimerLimit = 85
badGuys = [[50, 0]]
badSpawnRate = 1

# Player Variables
playerPosition = [100, 100]
healthPoints = 194
maxHP = healthPoints
arrow_speed = 10
step_size = 5
enemyMovementSpeed = 1

# 3 - Load images
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass1.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badGuyImage1 = pygame.image.load("resources/images/badguy.png")
badGuyImage = badGuyImage1
healthBar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameOver = pygame.image.load("resources/images/gameover1.png")
youWin = pygame.image.load("resources/images/youwin1.png")
powerUp1 = pygame.image.load("resources/images/powerup1.png")
powerUp2 = pygame.image.load("resources/images/powerup2.png")
powerUp3 = pygame.image.load("resources/images/powerup3.png")
pygame.mixer.init()

# 3.0.1 Menu Images
menuBG = pygame.image.load("resources/images/menubg.png")

# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

running = 1
exitCode = 0

# Menu


# menu_running = True
# while menu_running:
#     screen.fill(0)
#     temp = width // menuBG.get_width() + 1
#     for x in range(width // menuBG.get_width() + 1):
#         for y in range(int(height / menuBG.get_height()) + 1):
#             screen.blit(menuBG, (x * 100, y * 100))

# 4 - Keep looping through
while running:
    accuracy1 = round(accuracy[0] / accuracy[1] * 100, 2) if accuracy[1] != 0 else 0
    powerUpRateModifier = round(2 / (accuracy1 / 100) ** 4) if accuracy1 != 0 else 10

    badTimer -= 1
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    screen.blit(grass, (0, 0))

    numCastles = width // 100
    for i in range(numCastles):
        screen.blit(castle, (i * width / numCastles, height - 100))

    # 6.1 - Set player position and rotation
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (playerPosition[1] + 32),
                       position[0] - (playerPosition[0] + 26))
    playerRotate = pygame.transform.rotate(player, 360 - angle * 57.29)
    playerPosition1 = (playerPosition[0] - playerRotate.get_rect().width / 2,
                       playerPosition[1] - playerRotate.get_rect().height / 2)
    screen.blit(playerRotate, playerPosition1)

    # 6.2 - Draw arrows
    for bullet in arrows:
        index = 0

        vel_x = math.cos(bullet[0]) * arrow_speed
        vel_y = math.sin(bullet[0]) * arrow_speed
        bullet[1] += vel_x
        bullet[2] += vel_y

        # Left or Right
        # Top or Bottom
        if bullet[1] < 0 or bullet[1] > width or bullet[2] < 0 or bullet[2] > height:
            arrows.pop(index)

        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))

    # 6.3 - Draw badgers
    if badTimer == 0:
        badGuys.append([random.randint(50, width - 50), 0])  # screen position
        badTimer = 100 - round(badTimer1, 0)
        badTimer1 = badTimerLimit if badTimer1 >= badTimerLimit else badTimer1 + badSpawnRate

    index = 0
    for badGuy in badGuys:
        if badGuy[1] < -64:
            badGuys.pop(index)
        badGuy[1] += enemyMovementSpeed + 3 * badTimer1 / 100

        badRect = pygame.Rect(badGuyImage.get_rect())
        badRect.top = badGuy[1]
        badRect.left = badGuy[0]
        if badRect.top > height - 90:
            hit.play()
            healthPoints -= random.randint(5, 20)
            badGuys.pop(index)

        # 6.3.2 - Check for collisions
        index1 = 0
        for bullet in arrows:
            bullRect = pygame.Rect(arrow.get_rect())
            bullRect.left = bullet[1]
            bullRect.top = bullet[2]
            if badRect.colliderect(bullRect):
                kills += 1
                if healthPoints != maxHP:
                    healthPoints += 1
                enemy.play()
                accuracy[0] += 1
                badGuys.pop(index)
                arrows.pop(index1)

                if powerUpRateModifier != 0 and random.randint(0, 50) % powerUpRateModifier == 0:
                    poweredUp = True
                    powerUpRemaining = 3

            index1 += 1

        index += 1
    for badGuy in badGuys:
        screen.blit(badGuyImage, badGuy)

    # 6.4 - Draw clock
    font = pygame.font.Font(None, 24)
    survivedText = font.render("Time: " + str(round((90000 - pygame.time.get_ticks() / 1000) % 90, 2)).zfill(2), True,
                               (0, 0, 0))
    textRect = survivedText.get_rect()
    textRect.topright = [width, 5]
    screen.blit(survivedText, textRect)

    # 6.5 - Draw UI
    font = pygame.font.Font(None, 24)
    accuracyText = font.render("Accuracy: " + str(accuracy1), True, (0, 0, 0)) if accuracy[1] != 0 \
        else font.render("Accuracy: 0", True, (0, 0, 0))

    textRect = accuracyText.get_rect()
    textRect.topright = [width, 20]
    screen.blit(accuracyText, textRect)

    # Rate Display
    font = pygame.font.Font(None, 24)
    rateText = font.render("Rate: " + str(powerUpRateModifier), True, (0, 0, 0))
    textRect = rateText.get_rect()
    textRect.topright = [width, 35]
    screen.blit(rateText, textRect)

    # Kills Display
    font = pygame.font.Font(None, 24)
    killText = font.render("Kills: " + str(kills), True, (0, 0, 0))
    textRect = killText.get_rect()
    textRect.topright = [width, 50]
    screen.blit(killText, textRect)

    # Power Up Display
    powerUp_y = 20
    if True:
        if powerUpRemaining == 3:
            powerUpPosition = [0, powerUp_y]
            screen.blit(powerUp3, powerUpPosition)
        elif powerUpRemaining == 2:
            powerUpPosition = [0, powerUp_y + 30]
            screen.blit(powerUp2, powerUpPosition)
        elif powerUpRemaining == 1:
            powerUpPosition = [0, powerUp_y + 30]
            screen.blit(powerUp1, powerUpPosition)
    screen.blit(healthBar, (5, 5))

    # Health Display
    for health1 in range(healthPoints):
        screen.blit(health, (health1 + 8, 8))

    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button

        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            accuracy[1] += 1
            if poweredUp:
                accuracy[1] += 2
            arrows.append([math.atan2(position[1] - (playerPosition1[1] + 32), position[0] - (playerPosition1[0] + 26)),
                           playerPosition1[0] + 32, playerPosition1[1] + 32])
            if poweredUp:
                arrows.append(
                    [math.atan2(position[1] - (playerPosition1[1] + 32), position[0] - (playerPosition1[0] + 26)) + .2,
                     playerPosition1[0] + 32, playerPosition1[1] + 32])
                arrows.append(
                    [math.atan2(position[1] - (playerPosition1[1] + 32), position[0] - (playerPosition1[0] + 26)) - .2,
                     playerPosition1[0] + 32, playerPosition1[1] + 32])
                powerUpRemaining -= 1
                if powerUpRemaining == 0:
                    poweredUp = False

        # 9 - Move player
        if keys[0] and playerPosition[1] - step_size > 0:  # w is true and step is inside screen
            playerPosition[1] -= step_size
        elif keys[2] and playerPosition[1] + step_size < height:  # s is true and ''
            playerPosition[1] += step_size
        elif keys[1] and playerPosition[0] - step_size > 0:  # a is true and ''
            playerPosition[0] -= step_size
        elif keys[3] and playerPosition[0] + step_size < width:  # d is true and ''
            playerPosition[0] += step_size

    # 10 - Win/Lose check
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitCode = 1
    if healthPoints <= 0:
        running = 0
        exitCode = 0
    accuracy1 = accuracy[0] / accuracy[1] * 100 if accuracy[1] != 0 else 0

# 11 - Win/Lose display
pygame.font.init()
font = pygame.font.Font(None, 24)
color, outcome = ((255, 0, 0), gameOver) if exitCode == 0 else ((0, 255, 0), youWin)
text = font.render("Accuracy: " + str(round(accuracy1, 2)) + "%", True, color)
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 65

picture_width = outcome.get_width()
picture_height = outcome.get_height()
screen.blit(outcome, (width // 2 - picture_width // 2, height // 2 - picture_height // 2))
screen.blit(text, textRect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
