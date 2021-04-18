import pygame
import random

background_img = pygame.image.load('sprites/fone.png')
wooden_background_img = pygame.image.load('sprites/wooden_fone.jpg')
cookie_img = pygame.image.load('sprites/cookie.png')


class Cookie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 250
        self.height = 250

        self.animation_state = 0

    def draw(self):
        if self.animation_state > 0:
            cookie_img_scaled = pygame.transform.scale(cookie_img, (int(0.9 * self.length), int(0.9 * self.height)))
            screen.blit(cookie_img_scaled, (cookie_img_scaled.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))))
            self.animation_state -= 1
        else:
            screen.blit(cookie_img, (cookie_img.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))))

    def collidepoint(self, cursor_pos):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(cursor_pos)


class Score:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 100
        self.length = 100

    def draw(self):
        font = pygame.font.SysFont("Calibri", 20)
        current_score = font.render(str(player.score) + ' cookies', True, WHITE)
        cookie_per_sec = font.render(str(player.cookie_per_sec) + ' per second', True, WHITE)
        screen.blit(current_score, current_score.get_rect(center=(int(self.x + self.length), int(self.y + self.height))))
        screen.blit(cookie_per_sec, cookie_per_sec.get_rect(center=(int(self.x + self.length), int(self.y + self.height) + 20)))


class Buildings:
    def __init__(self, img, per_sec, cost, posx, posy):
        self.img = pygame.image.load(img)
        self.per_sec = per_sec
        self.cost = cost
        self.lvl = 0
        self.posx = posx
        self.posy = posy
        self.length = 432
        self.height = 100

    def draw(self):
        font = pygame.font.SysFont("Calibri", 20)
        screen.blit(self.img, (self.posx, self.posy))
        per_sec = font.render('+' + str(self.per_sec) + ' per sec', True, BLACK)
        screen.blit(per_sec,
                    per_sec.get_rect(center=(int(self.posx + self.length / 2), int(self.posy + self.height / 1.2))))
        cost = font.render(str(self.cost) + ' cookies', True, BLACK)
        screen.blit(cost,
                    cost.get_rect(center=(int(self.posx + self.length / 2), int(self.posy + self.height / 5))))
        lvl = font.render(str(self.lvl), True, BLACK)
        screen.blit(lvl,
                    lvl.get_rect(center=(int(self.posx + self.length / 1.1), int(self.posy + self.height / 2))))

    def collidepoint(self, cursor_pos):
        return pygame.Rect(self.posx, self.posy, self.length, self.height).collidepoint(cursor_pos)


buildings = [Buildings('sprites/1_grandma.png', per_sec=1, cost=100, posx=568, posy=100),
             Buildings('sprites/2_farm.png', per_sec=8, cost=1100, posx=568, posy=200),
             Buildings('sprites/3_mine.png', per_sec=47, cost=12000, posx=568, posy=300),
             Buildings('sprites/4_factory.png', per_sec=260, cost=130000, posx=568, posy=400),
             Buildings('sprites/5_bank.png', per_sec=1400, cost=1.4 * 10**6, posx=568, posy=500),
             Buildings('sprites/6_temple.png', per_sec=7800, cost=20 * 10**6, posx=568, posy=600),
             ]


class Player:
    def __init__(self):
        self.score = 0
        self.click_multi = 1
        self.cookie_per_sec = 0


WIDTH = 1000
HEIGHT = 600
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cookie clicker")
clock = pygame.time.Clock()

cookie = Cookie(568 / 2 - 125, 600 / 2 - 125)
score = Score(600 / 2 - 125, 0)
player = Player()


def draw():
    screen.blit(background_img, (0, 0))
    screen.blit(wooden_background_img, (568, 0))
    font = pygame.font.SysFont("Calibri", 40)
    font_for_name = pygame.font.SysFont("Calibri", 30)
    font_for_hints = pygame.font.SysFont("Calibri", 20)
    hints = font_for_hints.render("Mouse += 1 cookie and Space += 1000 cookie", True, RED)
    screen.blit(hints, hints.get_rect(center=(568 / 2, 50)))
    idx = 0
    build_lvl = font_for_name.render("CURRENT BUILDINGS LEVELS", True, GREEN)
    screen.blit(build_lvl, build_lvl.get_rect(center=(568 + (1000 - 568) / 2, 20)))
    for build in buildings:
        build_lvl = font.render(str(build.lvl), True, GREEN)
        screen.blit(build_lvl,
                    build_lvl.get_rect(center=(int(580 + 75 * idx), int(60))))
        if build.posy >= 100:
            build.draw()
        idx += 1

    cookie.draw()
    score.draw()
     
    pygame.display.update()


timer_per_sec = pygame.time.get_ticks()
running = True
while running:
    pygame.time.delay(10)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if cookie.collidepoint(mouse_pos):
                player.score += 1
                cookie.animation_state = 1

            for build in buildings:
                if build.collidepoint(mouse_pos) and player.score >= build.cost:
                    player.score -= build.cost
                    player.cookie_per_sec += build.per_sec
                    player.cookie_per_sec = round(player.cookie_per_sec, 2)
                    build.lvl += 1
                    build.cost *= 1.1
                    build.cost = round(build.cost, 2)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.score += 1000
                cookie.animation_state = 1

    if pygame.mouse.get_pos()[0] > 568:
        if pygame.mouse.get_pos()[1] > 575 and buildings[0].posy < 100:
            for build in buildings:
                build.posy += 10
        if pygame.mouse.get_pos()[1] < 125 and buildings[-1].posy > 500:
            for build in buildings:
                build.posy -= 10
    seconds = (pygame.time.get_ticks() - timer_per_sec) / 100
    if seconds >= 1:
        player.score += player.cookie_per_sec * 0.1
        player.score = round(player.score, 2)
        timer_per_sec = pygame.time.get_ticks()
    draw()
    pygame.display.flip()
pygame.quit()
