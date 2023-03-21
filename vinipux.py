import pygame
import random
from os import path
import time


img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 1200
HEIGHT = 800
FPS = 60
prs=False

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
timeend=0

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("птчк")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')
# графика
background = pygame.image.load(path.join('bg.jpg')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join( "pic1.jpg")).convert()
vrag_img = pygame.image.load(path.join( 'pic2.jpg')).convert()

background_rect = background.get_rect()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(vrag_img, (50, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.image.set_colorkey(WHITE)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (90, 60))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0


    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if keystate[pygame.K_w]:
            self.speedy = -4
        self.rect.y += self.speedy
        if keystate[pygame.K_s]:
            self.speedy = 4
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.top = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


font_name = pygame.font.match_font('arial')
label = pygame.font.Font('font.ttf', 40)
restart_label = label.render('restart',False,(115,132,148))
restart_label_rect = restart_label.get_rect(topleft=(180,200))
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(10):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Цикл игры
running = True
gameplay = True
while running:

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            prs = True
        if event.type == pygame.MOUSEBUTTONUP:
            prs = False
    if gameplay:


    # Рендеринг
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(background, (1280, 1024)), background_rect)
        all_sprites.draw(screen)
        hits = pygame.sprite.spritecollide(player, mobs, False)
        timeend += 167
        time = draw_text(screen, str(round((timeend/10000),3)), 40, WIDTH / 4, 2)


    else:
        screen.fill((0,0,0))
        pygame.time.Clock()
        draw_text(screen, str(timeend), 40, WIDTH / 4, 2)
        screen.blit(restart_label,restart_label_rect)
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and prs:
            gameplay = True
            for i in range(10):
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)

            # Обновление
    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        gameplay = False
        print(round((timeend/10000),3))
        timeend = 0
        player.rect.centerx = WIDTH / 2
        player.rect.bottom = HEIGHT - 10
        for m in mobs:
            m.kill()
            mobs.clear(screen, background)
            mobs.draw(screen)
 
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()


pygame.quit()
