import pygame
import os
import sys
import random


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((1, 1))
        image.set_colorkey(color_key)
    return image


pygame.init()
screen_size = (900, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 50
finX = -1
finY = -1
a = ''
b = 'для хода нажмите на кубик ,для движениея используйте стрелочки'
whose_turn = 1
dog_surf = load_image('6.png', -1)
dice = dog_surf.get_rect(bottomright=(800, 300))
trap_pos = list()

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'fin': load_image('f.png'),
    '1': load_image('1.png'),
    '2': load_image('2.png'),
    '3': load_image('3.png'),
    '4': load_image('4.png'),
    '5': load_image('5.png'),
    '6': load_image('6.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 300)


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        global N
        N -= 1
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])

    def glimpse(self):
        self.pos = (0, 0)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])

player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    global a, b
    intro_text = [a]
    intro_text+= b.split(',')

    fon = pygame.transform.scale(load_image('fon.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 25
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                a = ''
                b = ''
                return
            
        pygame.display.flip()
        clock.tick(FPS)

def fin_screen():
    intro_text = [a]

    fon = pygame.transform.scale(load_image('fon.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 25
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)

def craps():
    global N, dog_surf
    N = random.randint(1, 6)
    dog_surf = tile_images[str(N)]
    screen.blit(dog_surf, dice)
    


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '1')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                Tile('empty', x, y)
            elif level[y][x] == '2':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = "1"
            elif level[y][x] == '#':
                global finX, finY
                finX = x
                finY = y
                Tile('fin', x, y)
                level[y][x] = "1"
            elif level[y][x] == '*':
                global trap_pos
                Tile('empty', x, y)
                level[y][x] = "1"
                trap_pos.append([x, y])
    return new_player, x, y

def trap(x, y):
    global trap_pos, N
    if [x, y] in trap_pos and N == 1:
        N -= 1
        hero.glimpse()
    else:
        return True


def move(hero, movement):
    x, y = hero.pos
    #print(level_map[x][y - 1])
    #print(level_map[x][y + 1])
    #print(level_map[x - 1][y])
    #print(level_map[x][y + 1])
    #print()
    if x == finX and y == finY:
        global a, b
        a = 'YOU WIN'
        b = 'Правила те же, но теперь на карте спрятаны ловушки'
        return
    if movement == "up"  and N > 0:
        if y > 0 and level_map[y - 1][x] == "1":
            if trap(x, y - 1):
                hero.move(x, y - 1)
    elif movement == "down" and N > 0:
        if y < max_y  and level_map[y + 1][x] == "1":
            if trap(x, y + 1):
                hero.move(x, y + 1)
    elif movement == "left" and N > 0:
        if x > 0 and level_map[y][x - 1] == "1":
            if trap(x - 1, y):
                hero.move(x - 1, y)
    elif movement == "right" and N > 0:
        if x < max_x  and level_map[y][x + 1] == "1":
            if trap(x + 1, y):
                hero.move(x + 1, y)

N = 0
start_screen()
level_map = load_level("map1.txt")
hero, max_x, max_y = generate_level(level_map)
game = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            running = False
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, "up")
            elif event.key == pygame.K_DOWN:
                move(hero, "down")
            elif event.key == pygame.K_LEFT:
                move(hero, "left")
            elif event.key == pygame.K_RIGHT:
                move(hero, "right")
        elif event.type == pygame.MOUSEBUTTONDOWN and N == 0:
            x, y = event.pos
            if x >= 600 and x <= 800:
                if y >= 100 and y <= 300:
                    whose_turn = (whose_turn + 1)%2
                    craps()
    screen.fill(pygame.Color("white"))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    screen.blit(dog_surf, dice)
    clock.tick(FPS)
    pygame.display.flip()
    if a !='':
        start_screen()
        running = False
        
    #pygame.display.flip()
player = None
running = game
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
N = 0
level_map = load_level("map2.txt")
hero, max_x, max_y = generate_level(level_map)
screen.fill(pygame.Color("white"))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, "up")
            elif event.key == pygame.K_DOWN:
                move(hero, "down")
            elif event.key == pygame.K_LEFT:
                move(hero, "left")
            elif event.key == pygame.K_RIGHT:
                move(hero, "right")
        elif event.type == pygame.MOUSEBUTTONDOWN and N == 0:
            x, y = event.pos
            if x >= 600 and x <= 800:
                if y >= 100 and y <= 300:
                    whose_turn = (whose_turn + 1)%2
                    craps()
    screen.fill(pygame.Color("white"))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    screen.blit(dog_surf, dice)
    clock.tick(FPS)
    pygame.display.flip()
    if a !='':
        fin_screen()
