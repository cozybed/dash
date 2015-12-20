__author__ = 'lzt'

import pygame
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2
import math
import Cube
import Obstacle

pygame.init()
screen_width = 930
screen_height = 523
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

background = pygame.image.load("background.png").convert()
background.set_alpha(200)
background_pos = Vector2(0, 0)
cube = Cube.Cube(Vector2(320, 368), pygame.image.load("cube.png").convert_alpha())
welcome = pygame.image.load("welcome.png").convert_alpha()
left_arrow = pygame.image.load("left.png").convert_alpha()
right_arrow = pygame.image.load("right.png").convert_alpha()
floor = pygame.image.load("floor.png").convert_alpha()
block1 = pygame.image.load("block1.png").convert_alpha()
block2 = pygame.image.load("block2.png").convert_alpha()
block3 = pygame.image.load("block3.png").convert_alpha()
triangle = pygame.image.load("triangle.png").convert_alpha()
obs_image = [floor, block1, block2, block3, triangle]

my_font = pygame.font.SysFont("arial.ttf", 40)
my_font2 = pygame.font.SysFont("arial.ttf", 60)

background_speed = 50
obstacle_speed = 400

track = pygame.mixer.music.load("bgm.mp3")

maxcapther = 2
state = 1
chapter = 1
wait = 0

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == MOUSEMOTION:
            pressed_array = pygame.mouse.get_pressed()
            if pressed_array[0]:
                if state == 4:
                    state = 2
                    wait = 0
                if state == 5 and wait == 1:
                    if x > 300 and x < 340 and y > 428 and y < 468:
                        mouseclick = 1
                        wait = 0

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if state == 4:
                    state = 2
                    wait = 0
                elif state == 3 and cube.state == 0:
                    cube.state = 1

    if state == 1:
        if pygame.mouse.get_pressed()[0]:
             x, y = pygame.mouse.get_pos()
                if x > 832 and x < 912 and y > 241 and y < 321 and chapter < maxcapther:
                     chapter += 1
                     wait = 0
                elif x < 100 and x > 20 and y > 241 and y < 321 and chapter > 1:
                    chapter -= 1
                    wait = 0
                elif x > 315 and x < 615 and y > 150 and y < 450:
                    mouseclick = 0
                    state = 5
        if wait == 1:
            continue
        screen.fill((0, 0, 255))
        screen.blit(background, background_pos)
        chapter_str = 'chapter:' + str(chapter)
        chapter_surface = my_font2.render(chapter_str, True, (153, 102, 51))
        screen.blit(welcome, Vector2(315, 150))
        screen.blit(left_arrow, Vector2(20, 241))
        screen.blit(right_arrow, Vector2(832, 241))
        screen.blit(chapter_surface, Vector2(370, 80))

        wait = 1

    if state == 2:
        file = open("map" + str(chapter) + ".txt", "r")
        result1 = file.read().split('\n')
        result = [i for i in result1 if i != '']
        obs = []
        for x in result:
            line = x.split(" ")
            obs.append(Obstacle.Obstacle(Vector2(int(line[0]), int(line[1])), obs_image[int(line[2])], int(line[2])))
        file.close()

        score = 0
        flag = 0
        clock.tick()
        background_pos = Vector2(0, 0)
        cube.position = Vector2(320, 368)
        cube.state = 0
        pygame.mixer.music.play()
        state = 3

    if state == 3:
        screen.fill((0, 0, 255))
        screen.blit(background, background_pos)

        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0

        cube.update_position(time_passed_seconds * cube.speed, time_passed_seconds * cube.rotation_speed)
        score += time_passed_seconds * 10
        text_surface = my_font.render("Score " + str(score), True, (60, 0, 245))
        rotated_sprite = pygame.transform.rotate(cube.cube_image, cube.rotation)
        w, h = rotated_sprite.get_size()
        screen.blit(rotated_sprite, (cube.position.x - w/2, cube.position.y - h/2))

        for ob in obs:
            if ob.style != 4:
                if abs(cube.position.y + h / 2 - ob.position.y) < 1 and cube.state != 1:
                    if cube.position.x > ob.position.x + ob.width and  cube.position.x < ob.position.x + ob.width + 20 and cube.state == 0:
                        cube.state = -1
                        #print ob.position
                    if cube.position.x > ob.position.x - w / 2 and cube.position.x < ob.position.x + ob.width:
                        cube.state = 0
                        cube.position.y = ob.position.y - 20
                        #cube.position.y = ob.position.y - 19.8

                if abs(cube.position.y - 20 - ob.position.y - ob.height) < 1 and cube.state == 1:
                    if cube.position.x > ob.position.x - 20 and cube.position.x < ob.position.x + ob.width + 20:
                        state = 4

                if abs(cube.position.x + 20 - ob.position.x) < 1:
                    if cube.position.y > ob.position.y - h / 3 and cube.position.y < ob.position.y + ob.height + h / 3:
                        state = 4
            else:
                distance = cube.position - ob.position - Vector2(20, 25)
                if math.sqrt(distance.x * distance.x + distance.y * distance.y) < 35:
                    state = 4

            screen.blit(ob.image, ob.position)
            ob.Move(Vector2(-1, 0), time_passed_seconds * obstacle_speed)
            if ob.position.x + ob.width < 0:
                obs.remove(ob)
            #print len(obs)

        screen.blit(text_surface, Vector2(750, 50))
        #pygame.draw.line(screen, (0, 0, 255), (0, 388), (100, 388))
        #pygame.draw.line(screen, (0, 0, 255), (0, 348), (100, 348))
        background_pos.x -= time_passed_seconds * background_speed
        if background_pos.x < -screen_width:
            background_pos.x += screen_width

    if state == 4:
        death_str = "You Are Dead!"
        death_surface = my_font2.render(death_str, True, (255, 0, 0))
        screen.blit(death_surface, Vector2(340, 200))
        wait = 1

    if state == 5:
        screen.fill((0, 0, 255))
        screen.blit(background, background_pos)

        map = [[0, 388, 0]]
        for x in map:
            ob = Obstacle.Obstacle(Vector2(int(x[0]), int(x[1])), obs_image[int(x[2])], int(x[2]))
            screen.blit(ob.image, ob.position)

        screen.blit(block1, Vector2(300, 428))

        if mouseclick != 0:
            for i in range(28, 389, 40):
                for j in range(0, screen_width, 10):
                    pygame.draw.line(screen, (255, 255, 255), (j, i), (j + 5, i), 2)
            for i in range(40, screen_width, 40):
                for j in range(0, 388, 10):
                    pygame.draw.line(screen, (255, 255, 255), (i, j), (i, j + 5), 2)
            x, y = pygame.mouse.get_pos()
            x = x / 40 * 40
            y = (y - 28) / 40 * 40 + 28
            screen.blit(obs_image[mouseclick], Vector2(x, y))
        else:
            wait = 1

    pygame.display.update()