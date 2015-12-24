# coding=utf-8
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

clock = pygame.time.Clock()

def MainInterface(chapter):
    screen.fill((0, 0, 255))
    screen.blit(background, Vector2(0, 0))
    chapter_str = 'chapter:' + str(chapter)
    chapter_surface = my_font2.render(chapter_str, True, (153, 102, 51))
    screen.blit(welcome, Vector2(315, 150))
    screen.blit(left_arrow, Vector2(20, 241))
    screen.blit(right_arrow, Vector2(832, 241))
    screen.blit(chapter_surface, Vector2(370, 80))
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if x in range(832, 912) and y in range(241, 321) and chapter < maxcapther:
                    return MainInterface(chapter + 1)
                elif x in range(20, 100) and y in range(241, 321) and chapter > 1:
                    return GameStart(chapter)
                    #return MainInterface(chapter - 1)
                elif x in range(315, 615) and y in range(150, 450):
                   # return GameStart(chapter)
                    return MapEdit()

def GameStart(chapter):
    map = open("map" + str(chapter) + ".txt", "r")
    result1 = map.read().split('\n')
    result = [i for i in result1 if i != '']
    obs = []
    for x in result:
        line = x.split(" ")
        obs.append(Obstacle.Obstacle(Vector2(int(line[0]), int(line[1])), obs_image[int(line[2])], int(line[2])))
    map.close()

    score = 0
    clock.tick()
    background_pos = Vector2(0, 0)
    cube.position = Vector2(320, 368)
    cube.state = 0
    pygame.mixer.music.play()
    over = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if cube.state == 0:
                        cube.state = 1

        screen.fill((0, 0, 255))
        screen.blit(background, background_pos)

        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0

        cube.update_position(time_passed_seconds * cube.speed, time_passed_seconds * cube.rotation_speed)
        score += time_passed_seconds * 10
        text_surface = my_font.render("Score " + str(score), True, (60, 0, 245))
        rotated_sprite = pygame.transform.rotate(cube.cube_image, cube.rotation)
        w, h = rotated_sprite.get_size()
        screen.blit(rotated_sprite, (cube.position.x - w / 2, cube.position.y - h / 2))

        for ob in obs:
            if ob.style != 4:
                if abs(cube.position.y + h / 2 - ob.position.y) < 1 and cube.state != 1:
                    if cube.position.x > ob.position.x + ob.width and cube.position.x < ob.position.x + ob.width + 20 and cube.state == 0:
                        cube.state = -1
                        # print ob.position
                    if cube.position.x > ob.position.x - w / 2 and cube.position.x < ob.position.x + ob.width:
                        cube.state = 0
                        cube.position.y = ob.position.y - 20
                        # cube.position.y = ob.position.y - 19.8

                if abs(cube.position.y - 20 - ob.position.y - ob.height) < 1 and cube.state == 1:
                    if cube.position.x > ob.position.x - 20 and cube.position.x < ob.position.x + ob.width + 20:
                        over = 1

                if abs(cube.position.x + 20 - ob.position.x) < 1:
                    if cube.position.y > ob.position.y - h / 3 and cube.position.y < ob.position.y + ob.height + h / 3:
                        over = 1
            else:
                distance = cube.position - ob.position - Vector2(20, 25)
                if math.sqrt(distance.x * distance.x + distance.y * distance.y) < 35:
                    over = 1

            screen.blit(ob.image, ob.position)
            ob.Move(Vector2(-1, 0), time_passed_seconds * obstacle_speed)
            if ob.position.x + ob.width < 0:
                obs.remove(ob)
                # print len(obs)

        screen.blit(text_surface, Vector2(750, 50))
        background_pos.x -= time_passed_seconds * background_speed
        if background_pos.x < -screen_width:
            background_pos.x += screen_width
        if over:
            return GameOver(chapter)
        pygame.display.update()

def GameOver(chapter):
    death_str = "You Are Dead!"
    death_surface = my_font2.render(death_str, True, (255, 0, 0))
    screen.blit(death_surface, Vector2(340, 200))
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                return GameStart(chapter)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                return GameStart(chapter)

def MapEdit():
    def drawbase():
        screen.fill((0, 0, 255))
        screen.blit(background, Vector2(0, 0))
        for x in map:
            ob = Obstacle.Obstacle(Vector2(int(x[0]), int(x[1])), obs_image[int(x[2])], int(x[2]))
            screen.blit(ob.image, ob.position)
        screen.blit(block1, Vector2(320, 428))
        screen.blit(block2, Vector2(400, 428))
        screen.blit(block3, Vector2(480, 428))
        screen.blit(triangle, Vector2(560, 428))
        screen.blit(left_arrow, Vector2(20, 241))
        screen.blit(right_arrow, Vector2(832, 241))

    def drawedit():
        drawbase()
        for i in range(28, 389, 40):
            for j in range(0, screen_width, 10):
                pygame.draw.line(screen, (255, 255, 255), (j, i), (j + 5, i), 2)
        for i in range(40, screen_width, 40):
            for j in range(0, 388, 10):
                pygame.draw.line(screen, (255, 255, 255), (i, j), (i, j + 5), 2)
        x, y = pygame.mouse.get_pos()
        x = x / 40 * 40
        y = (y - 28) / 40 * 40 + 28
        screen.blit(obs_image[select], Vector2(x, y))

    floornum = 1
    offset = 0
    map = [[0, 388, 0]]
    select = 0
    drawbase()
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            xx = x / 40 * 40
            yy = (y - 28) / 40 * 40 + 28
            if event.button == 1:
                #                                                                                                 右箭头
                if x in range(832, 912) and y in range(241, 321):
                    offset += 40
                    if offset + screen_width > floornum * 1024:
                        #print offset
                        map.append([floornum * 1024 - offset, 388, 0])
                        floornum += 1
                    for ob in map:
                        ob[0] -= 40
                    if select == 0:
                        drawbase()
                    else:
                        drawedit()
                    pygame.display.update()
                #                                                                                                 左箭头
                elif x in range(20, 100) and y in range(241, 321) and offset >= 40:
                    offset -= 40
                    for ob in map:
                        ob[0] += 40
                    if select == 0:
                        drawbase()
                    else:
                        drawedit()
                    pygame.display.update()
                #                                                                                               保存地图
                elif x in range(640, 680) and y in range(428, 468):
                    global maxcapther
                    maxcapther += 1
                    out = open("map" + str(maxcapther) + ".txt", "w")
                    for ob in map:
                        out.write(str(ob[0] + offset) + ' ' + str(ob[1]) + ' ' + str(ob[2]) + '\n')
                    out.close()
                    return MainInterface(1)
                else:
                    #                                                                                           选择方块
                    if select == 0:
                        if y in range(428, 468):
                            if x in range(320, 360):
                                select = 1
                            if x in range(400, 440):
                                select = 2
                            if x in range(480, 520):
                                select = 3
                            if x in range(560, 600):
                                select = 4
                        if select != 0:
                            drawedit()
                            pygame.display.update()
                    #                                                                                           添加方块
                    else:
                        if y < 388:
                            for pos in map:
                                if pos[0] == xx and pos[1] == yy:
                                    map.remove(pos)
                            map.append([xx, yy, select])
            elif event.button == 3:
                #                                                                                               删除方块
                if select != 0:
                    select = 0
                else:
                    for pos in map:
                        if pos[0] == xx and pos[1] == yy:
                            map.remove(pos)
                drawbase()
                pygame.display.update()
        elif event.type == MOUSEMOTION:
            if select != 0:
                drawedit()
                pygame.display.update()

MainInterface(1)