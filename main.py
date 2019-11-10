'''
TODO :
Store the score of the player along with name
Display the top 5 high scores in the high_score() function
Increase the speed of the game as time progresses
'''


import random
import pygame
import time


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 0
        self.dirny = 1
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.body.append(cube((10, 9)))
        self.body.append(cube((10, 8)))
        self.body.append(cube((10, 7)))
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and self.dirnx != 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT] and self.dirnx != -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP] and self.dirny != 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN] and self.dirny != -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_p]:
                    global pause, last_pause
                    millis = int(round(time.time() * 1000))
                    if millis - last_pause >=1000:
                        last_pause = millis
                        pause = True
                        paused()

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.body.append(cube((10, 9)))
        self.body.append(cube((10, 8)))
        self.body.append(cube((10, 7)))
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


pause = False
last_pause = 0

def unpause():
    global pause
    pause = False


def paused():
    global width, win, pause, clock, button_color, button_color_light

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.fill((0, 0, 0))

        largeText = pygame.font.Font('Fonts/Roboto/Roboto-Thin.ttf', 60)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((width / 2), (width / 2))
        win.blit(TextSurf, TextRect)

        button("Continue", width // 3 // 2 - 60, width * 3 // 4, 120, 50, button_color, button_color_light, unpause)
        button("Quit", width * 2 // 3 + width // 3 // 2 - 40, width * 3 // 4, 80, 50, button_color, button_color_light,
               quit_game)


        pygame.display.update()
        clock.tick(15)


width = 500
rows = 20
win = pygame.display.set_mode((width, width))
clock = pygame.time.Clock()


def main():
    global width, rows, s, snack, win, clock
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                high_score(len(s.body))
                s.reset((10,10))
                break

        redrawWindow(win)
    pass


def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()


button_color = (0, 0, 128)
button_color_light = (0, 0, 80)


def button(msg, x, y, w, h, ic, ac, action=None):
    global win
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(win, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(win, ic, (x, y, w, h))

    pygame.init()
    smallText = pygame.font.Font("Fonts/Roboto/Roboto-Regular.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    win.blit(textSurf, textRect)
    return x + w > mouse[0] > x and y + h > mouse[1] > y and click[0] == 1


def quit_game():
    pygame.quit()
    quit()


def high_score(sc):
    global width, win, pause, clock, button_color, button_color_light
    high_score_mode = True
    while high_score_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.fill((0, 0, 0))

        largeText = pygame.font.Font('Fonts/Roboto/Roboto-Thin.ttf', 60)
        TextSurf, TextRect = text_objects("Your score : " + str(sc), largeText)
        TextRect.center = ((width / 2), (width / 2))
        win.blit(TextSurf, TextRect)

        high_score_mode = not button("Retry", width // 3 // 2 - 60, width * 3 // 4, 120, 50, button_color, button_color_light)
        button("Quit", width * 2 // 3 + width // 3 // 2 - 40, width * 3 // 4, 80, 50, button_color, button_color_light,
               quit_game)


        pygame.display.update()
        clock.tick(15)

def game_intro():
    global win, width, button_color, button_color_light
    # gameDisplay = win
    intro = True
    clock = pygame.time.Clock()

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.fill((0, 0, 0))
        largeText = pygame.font.Font('Fonts/Roboto/Roboto-Thin.ttf', 60)
        TextSurf, TextRect = text_objects("Snake Game", largeText)
        TextRect.center = ((width / 2), (width / 2))
        win.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()

        # print(mouse)

        def play_game():
            intro = False
            main()

        button("Play", width // 3 // 2 - 40, width * 3 // 4, 80, 50, button_color, button_color_light, play_game)

        # Not built yet
        button("AI mode", width // 3 + width // 3 // 2 - 40, width * 3 // 4, 80, 50, button_color, button_color_light)

        button("Quit", width * 2 // 3 + width // 3 // 2 - 40, width * 3 // 4, 80, 50, button_color, button_color_light,
               quit_game)

        pygame.display.update()
        clock.tick(15)


pygame.init()
game_intro()
# main()
