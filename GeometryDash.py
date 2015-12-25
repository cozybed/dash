# coding=utf-8
__author__ = 'lzt'

import pygame
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2
import math
import Cube
import Obstacle
import sqlite3

pygame.init()

screen_width = 930
screen_height = 523
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

input = pygame.image.load("./image/input.png").convert_alpha()
save = pygame.image.load("./image/save.png").convert_alpha()
back = pygame.image.load("./image/back.png").convert_alpha()
board = pygame.image.load("./image/board.jpg").convert_alpha()
restart = pygame.image.load("./image/restart.png").convert_alpha()
background = pygame.image.load("./image/background.png").convert()
background.set_alpha(200)
cube_image1 = pygame.image.load("./image/cube.png").convert_alpha()
cube_image2 = pygame.image.load("./image/bird.png").convert_alpha()
cube_image3 = pygame.image.load("./image/arrow.png").convert_alpha()
welcome = pygame.image.load("./image/welcome.png").convert_alpha()
left_arrow = pygame.image.load("./image/left.png").convert_alpha()
right_arrow = pygame.image.load("./image/right.png").convert_alpha()
floor = pygame.image.load("./image/floor.png").convert_alpha()
block1 = pygame.image.load("./image/block1.png").convert_alpha()
block2 = pygame.image.load("./image/block2.png").convert_alpha()
block3 = pygame.image.load("./image/block3.png").convert_alpha()
triangle1 = pygame.image.load("./image/triangle1.png").convert_alpha()
triangle2 = pygame.image.load("./image/triangle2.png").convert_alpha()
triangle3 = pygame.image.load("./image/triangle3.png").convert_alpha()
triangle4 = pygame.image.load("./image/triangle4.png").convert_alpha()
jump = pygame.image.load("./image/jump.png").convert_alpha()
end = pygame.image.load("./image/flag7.png").convert_alpha()
createmap = pygame.image.load("./image/xinjianditu.png").convert_alpha()
door1 = pygame.image.load("./image/flag5.png").convert_alpha()
door2 = pygame.image.load("./image/flag2.png").convert_alpha()
door3 = pygame.image.load("./image/flag3.png").convert_alpha()
obs_image = [floor, block1, block2, block3, triangle1, triangle2, triangle3, triangle4, jump, end, door1, door2, door3]

cube = Cube.Cube(Vector2(320, 367.9), cube_image1)

my_font = pygame.font.SysFont("arial.ttf", 40)
my_font2 = pygame.font.SysFont("arial.ttf", 60)
my_font3 = pygame.font.SysFont("arial.ttf", 35)

background_speed = 50
obstacle_speed = 400

music = ["bgm.mp3", "bgm.mp3", "bgm.mp3"]
clock = pygame.time.Clock()
maxcapther = 2
name = ""
score = 0

def insertRecord(name, score):
    conn = sqlite3.connect('identifier.sqlite')
    cursor = conn.cursor()
    newData = [
        (name, score),
    ]
    try:
        for t in newData:
            cursor.execute('INSERT INTO ScoreBoard VALUES (?, ?)', t)
        conn.commit()
        conn.close()
    except:
        cursor.execute('UPDATE ScoreBoard SET score = ? WHERE name = ?', (score, name))
        conn.commit()
        conn.close()
# insertRecord('sandy', 11)
def displayScoreBoard():
    conn = sqlite3.connect("identifier.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ScoreBoard')
    result = cursor.fetchall()
    result.sort(key = lambda score: score[1], reverse = True)
    return result

def InputName():
    global name
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key >= 97 and event.key <= 122 and len(name) < 7:
                name += chr(event.key)
            elif event.key >= 256 and event.key <= 265 and len(name) < 7:
                name += str(event.key - 256)
            elif event.key == 8 and len(name) > 0:
                name = name[:-1]
            elif (event.key == 13 or event.key == 271) and len(name) > 0:
                return MainInterface(1)

        screen.fill((0, 0, 255))
        screen.blit(background, Vector2(0, 0))
        screen.blit(pygame.transform.rotate(input, 90), Vector2(209, 200))
        text_surface = my_font.render("InputName:", True, (196, 131, 65))
        screen.blit(text_surface, Vector2(380, 235))
        screen.blit(pygame.transform.rotate(input, 90), Vector2(209, 290))
        name_surface = my_font.render(name, True, (30, 196, 5))
        screen.blit(name_surface, Vector2(410, 325))
        pygame.display.update()

def MainInterface(chapter):
    screen.fill((0, 0, 255))
    screen.blit(background, Vector2(0, 0))
    chapter_str = 'chapter:' + str(chapter)
    chapter_surface = my_font2.render(chapter_str, True, (153, 102, 51))
    screen.blit(welcome, Vector2(315, 150))
    screen.blit(left_arrow, Vector2(20, 241))
    screen.blit(right_arrow, Vector2(832, 241))
    screen.blit(chapter_surface, Vector2(370, 80))
    screen.blit(createmap, Vector2(700, 400))
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
                    return MainInterface(chapter - 1)
                elif x in range(315, 615) and y in range(150, 450):
                    return GameStart(chapter)
                elif x in range(700, 800) and y in range(400, 500):
                    return MapEdit()

def GameStart(chapter):
    global score, obstacle_speed
    def judge(p1, p2, p3, p4):
        if p1.x != p2.x and p3.x == p4.x:
            k1 = (p1.y - p2.y) / (p1.x - p2.x)
            b1 = (p1.x * p2.y - p1.y * p2.x) / (p1.x - p2.x)
            x = p3.x
            y = k1 * x + b1
        elif p1.x == p2.x and p3.x != p4.x:
            k2 = (p3.y - p4.y) / (p3.x - p4.x)
            b2 = (p3.x * p4.y - p3.y * p4.x) / (p3.x - p4.x)
            x = p1.x
            y = k2 * x + b2
        elif p1.x != p2.x and p3.x != p4.x:
            k1 = (p1.y - p2.y) / (p1.x - p2.x)
            k2 = (p3.y - p4.y) / (p3.x - p4.x)
            if k1 == k2:
                return 0
            b1 = (p1.x * p2.y - p1.y * p2.x) / (p1.x - p2.x)
            b2 = (p3.x * p4.y - p3.y * p4.x) / (p3.x - p4.x)
            x = (b2 - b1) / (k1 - k2)
            y = k1 * x + b1
        else:
            return 0
        if x >= min(p1.x, p2.x) and x <= max(p1.x, p2.x) and y >= min(p1.y, p2.y) and y <= max(p1.y, p2.y) and x >= min(p3.x, p4.x) and x <= max(p3.x, p4.x) and y >= min(p3.y, p4.y) - 0.1 and y <= max(p3.y, p4.y) + 0.1:
            return 1
        else:
            return 0
    #pygame.mixer.init()
    #pygame.time.delay(1000)

    map = open("./map/map" + str(chapter) + ".txt", "r")
    result1 = map.read().split('\n')
    result = [i for i in result1 if i != '']
    obs1 = []
    for x in result:
        line = x.split(" ")
        obs1.append([int(line[0]), int(line[1]), int(line[2])])

    map.close()
    obs = []
    for ob in obs1:
        if ob[0] < screen_width:
            obs.append(Obstacle.Obstacle(Vector2(ob[0], ob[1]), obs_image[ob[2]], ob[2]))
            obs1.remove(ob)

    score = 0
    offset = 0
    clock.tick()
    background_color = 0
    background_pos = Vector2(0, 0)
    cube.cube_image = cube_image1
    cube.initall()
    pygame.mixer.music.load(music[chapter - 1])
    pygame.mixer.music.play()
    over = 0
    start = pygame.time.get_ticks()
    c = cube.position.y

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if cube.state == 0:
                        cube.state = 1
                        c = cube.position.y
                        start = pygame.time.get_ticks()
                    for ob in obs:
                        if ob.style == 8 and cube.position.x > ob.points[0].x and cube.position.x < ob.points[1].x and cube.position.y > ob.points[0].y and cube.position.y < ob.points[2].y:
                            cube.state = 1
                            c = cube.position.y
                            start = pygame.time.get_ticks()
                    if cube.role == 1:
                        cube.state = 1
                        c = cube.position.y
                        start = pygame.time.get_ticks()
                    if cube.role == 2:
                        print 1
                        cube.up = 1
                        c = cube.position.y
                        start = pygame.time.get_ticks()
            elif event.type == KEYUP:
                if cube.up == 1:
                    cube.up = 0
                    c = cube.position.y
                    start = pygame.time.get_ticks()

        if cube.role == 0:
            screen.fill((0, 0, background_color))
        elif cube.role == 1:
            screen.fill((0, background_color, 0))
        elif cube.role == 2:
            screen.fill((background_color, 0, 0))
        screen.blit(background, background_pos)

        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0
        offset += time_passed_seconds * obstacle_speed
        background_color = offset / 5 % 512
        if background_color >= 256:
            background_color = 511 - background_color

        for ob in obs1:
            if ob[0] < screen_width + offset:
                obs.append(Obstacle.Obstacle(Vector2(ob[0] - offset, ob[1]), obs_image[ob[2]], ob[2]))
                obs1.remove(ob)
        score += time_passed_seconds * 10
        text_surface = my_font.render("Score " + str(score), True, (60, 0, 245))

        cube.update(c, (pygame.time.get_ticks() - start) / 1000.0 * obstacle_speed)
        rotated_sprite = pygame.transform.rotate(cube.cube_image, cube.rotation)
        w, h = rotated_sprite.get_size()
        screen.blit(rotated_sprite, (cube.position.x - w / 2, cube.position.y - h / 2))

        if cube.points[0].y < 0 or cube.points[2].y > screen_height:
            over = 1
        for ob in obs:
            if ob.style == 4:
                distance = cube.position - ob.position - Vector2(20, 25)
                if math.sqrt(distance.x * distance.x + distance.y * distance.y) < 35:
                    over = 1
            elif ob.style == 5:
                distance = cube.position - ob.position - Vector2(15, 20)
                if math.sqrt(distance.x * distance.x + distance.y * distance.y) < 35:
                    over = 1
            elif ob.style == 6:
                distance = cube.position - ob.position - Vector2(20, 15)
                if math.sqrt(distance.x * distance.x + distance.y * distance.y) < 35:
                    over = 1
            elif ob.style == 7:
                distance = cube.position - ob.position - Vector2(25, 20)
                if math.sqrt(distance.x * distance.x + distance.y * distance.y) < 35:
                    over = 1
            elif ob.style == 8:
                pass
            elif ob.style == 9:
                if cube.points[1].x > ob.points[0].x:
                    return gamecomplete()
            elif ob.style == 11:
                if cube.points[1].x > ob.points[0].x:
                    cube.role = 1
                    cube.cube_image = cube_image2
            elif ob.style == 12:
                if cube.points[1].x > ob.points[0].x and cube.role != 2:
                    cube.role = 2
                    cube.cube_image = cube_image3
                    obstacle_speed = 500
                    c = cube.position.y
                    start = pygame.time.get_ticks()
            elif not (ob.points[0].x > cube.points[1].x or ob.points[1] < cube.points[0].x):
                if cube.state != 0:
                    p1 = judge(cube.points[1], cube.points[2], ob.points[0], ob.points[1])
                    p2 = judge(cube.points[1], cube.points[2], ob.points[0], ob.points[3])
                    x = pygame.time.get_ticks() - start
                    if p1 == 1 and p2 == 1:
                        if cube.position.x + 20> ob.position.x and (x > 100 or cube.state == 2):
                            cube.initposition()
                            c = ob.points[0].y - 20.1
                        else:
                            over = 1
                    if p1 == 1 and p2 == 0 and (x > 100 or cube.state == 2):
                        cube.initposition()
                        c = ob.points[0].y - 20.1
                    if p1 == 0 and p2 == 1:
                        over = 1
                    if cube.state == 1 and judge(cube.points[0], cube.points[1], ob.points[2], ob.points[3]):
                        over = 1
                else:
                    if abs(cube.position.x + 20 - ob.position.x) < 1:
                        if cube.points[2].y > ob.points[0].y and cube.points[0].y < ob.points[2].y:
                            over = 1
                    if cube.position.x > ob.points[1].x and cube.points[0].x < ob.points[1].x:
                        cube.state = 2
                        c = cube.position.y
                        start = pygame.time.get_ticks()
            screen.blit(ob.image, ob.position)
            ob.Move(Vector2(-1, 0), time_passed_seconds * obstacle_speed)
            if ob.position.x + ob.width < 0:
                obs.remove(ob)
        pygame.draw.line(screen, (255, 0, 0), (0, 0), (930, 0), 5)
        pygame.draw.line(screen, (255, 0, 0), (0, 523), (930, 523), 5)
        screen.blit(text_surface, Vector2(750, 50))
        background_pos.x -= time_passed_seconds * background_speed
        if background_pos.x < -screen_width:
            background_pos.x += screen_width
        if over:
            return GameOver(chapter)
        pygame.display.update()

def showscore(chapter):
    global score
    scorelist = displayScoreBoard()
    screen.blit(board, Vector2(200, 66))
    for i in range(min(5, len(scorelist))):
        player = str(i + 1) + '. '+ scorelist[i][0]
        player_score = str(scorelist[i][1])
        player_surface = my_font3.render(player, True, (255, 0, 0))
        score_surface = my_font3.render(player_score, True, (255, 0, 0))
        screen.blit(player_surface, Vector2(230, 130 + 40 * i))
        screen.blit(score_surface, Vector2(370, 130 + 40 * i))
    for i in range(5, min(10, len(scorelist))):
        player = str(i + 1) + '. '+ scorelist[i][0]
        player_score = str(scorelist[i][1])
        player_surface = my_font3.render(player, True, (255, 0, 0))
        score_surface = my_font3.render(player_score, True, (255, 0, 0))
        screen.blit(player_surface, Vector2(500, 130 + 40 * (i - 5)))
        screen.blit(score_surface, Vector2(640, 130 + 40 * (i - 5)))
    screen.blit(back, Vector2(300, 340))
    screen.blit(restart, Vector2(570, 340))
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
                x, y = event.pos
                if x in range(300, 360) and y in range(340, 400):
                    pygame.mixer.music.stop()
                    return MainInterface(1)
                if x in range(570, 630) and y in range(340, 400):
                    return GameStart(chapter)

def GameOver(chapter):
    #displayScoreBoard()
    death_str = "You Are Dead!"
    death_surface = my_font2.render(death_str, True, (255, 0, 0))
    screen.blit(death_surface, Vector2(340, 200))
    pygame.display.update()
    pygame.time.delay(1000)
    showscore(chapter)

def gamecomplete():
    global name, score
    insertRecord(name, score)

def MapEdit():
    def drawbase():
        screen.fill((0, 0, 255))
        screen.blit(background, Vector2(0, 0))
        for x in map:
            ob = Obstacle.Obstacle(Vector2(int(x[0]), int(x[1])), obs_image[int(x[2])], int(x[2]))
            screen.blit(ob.image, ob.position)
        for i in range(1, 10):
            screen.blit(obs_image[i], Vector2(i * 80, 428))
        for i in range(10, 13):
            screen.blit(obs_image[i], Vector2(i * 40 + 360, 428))
        screen.blit(left_arrow, Vector2(20, 241))
        screen.blit(right_arrow, Vector2(832, 241))
        screen.blit(back, Vector2(20, 20))
        screen.blit(save, Vector2(850, 20))

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
                elif x in range(850, 910) and y in range(20, 80):
                    global maxcapther
                    maxcapther += 1
                    out = open("./map/map" + str(maxcapther) + ".txt", "w")
                    for ob in map:
                        out.write(str(ob[0] + offset) + ' ' + str(ob[1]) + ' ' + str(ob[2]) + '\n')
                    out.close()
                    return MainInterface(1)
                #                                                                                                   返回
                elif x in range(20, 80) and y in range(20, 80):
                    MainInterface(1)
                else:
                    #                                                                                           选择方块
                    if select == 0:
                        if y in range(428, 468) and x in range(80, 760) and x % 80 < 40:
                            select =  x / 80
                        if y in range(428, 468) and x in range(760, 880):
                            select =  (x - 760) / 40 + 10
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

InputName()