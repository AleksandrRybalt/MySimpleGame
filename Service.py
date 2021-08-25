import pygame
import os
import math


def create_sprite(img, size, colorkey=None):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (size, size))
    sprite = pygame.Surface((size, size))
    sprite.blit(icon, (0, 0))
    sprite.set_colorkey((0, 0, 0))
    return sprite


class DrawMap:
    def __init__(self, map, hero, game_window_size):
        self.size = 60
        self.map = map
        self.game_window_size = game_window_size
        self.hero = hero
        self.game_window = None
        self.map_size = None
        self.map_screen = pygame.Surface((self.map.map_size[0] * 60, self.map.map_size[1] * 60))
        self.draw_map()

    def draw_map(self):
        self.map_size = [self.map.map_size[0] * self.size, self.map.map_size[1] * self.size]
        self.map_screen = pygame.Surface((self.map_size[0], self.map_size[1]))
        self.draw_ground(self.map_screen, self.map_size)
        self.draw_trees(self.map.objects['trees'], self.map_screen)
        self.draw_doors(self.map.objects['doors'], self.map_screen)
        self.draw_enemies(self.map_screen)
        self.draw_items(self.map_screen)
        self.draw_hero()
        self.draw_game_window()
        self.game_window.blit(self.map_screen, self.determine_map_pos())

    def draw_game_window(self):
        self.game_window = pygame.Surface((self.game_window_size[0], self.game_window_size[1]))
        self.draw_ground(self.game_window, self.game_window_size)
        self.draw_trees('all', self.game_window, self.game_window_size)

    def draw_hero(self):
        self.hero.sprite = create_sprite(os.path.join("texture", "hero.png"), self.size)
        self.map_screen.blit(self.hero.sprite, ((self.hero.pos[0]-1) * self.size, (self.hero.pos[1]-1) * self.size))

    def draw_ground(self, work_surface, surface_size):
        ground = create_sprite(os.path.join("texture", "ground.png"), self.size)
        for coord_x in range(0, math.ceil(surface_size[0] + 1), self.size):
            for coord_y in range(0, math.ceil(surface_size[1] + 1), self.size):
                work_surface.blit(ground, (coord_x, coord_y))

    def draw_trees(self, obj_coords, work_surface, surface_size=None):
        tree = create_sprite(os.path.join("texture", "tree.png"), self.size)
        if obj_coords != 'all':
            for coord in obj_coords:
                work_surface.blit(tree, (coord[0] * self.size, coord[1] * self.size))
        else:
            for coord_x in range(0, math.ceil(surface_size[0] + 1), self.size):
                for coord_y in range(0, math.ceil(surface_size[1] + 1), self.size):
                    work_surface.blit(tree, (coord_x, coord_y))

    def draw_doors(self, obj_coords, work_surface):
        door = create_sprite(os.path.join("texture", "door.png"), self.size)
        for coord in obj_coords:
            work_surface.blit(door, ((coord[0] - 1) * self.size, (coord[1] - 1) * self.size))

    def determine_map_pos(self):
        if self.hero.pos[0] * self.size < (self.game_window_size[0] / 2 - self.size / 2):
            if self.hero.pos[1] * self.size < (self.game_window_size[1] / 2 - self.size / 2):
                map_pos = (0, 0)
            elif self.map_size[1] - self.hero.pos[1] * self.size < (self.game_window_size[1] / 2 - self.size / 2):
                map_pos = (0, self.game_window_size[1] - self.map_size[1])
            else:
                map_pos = (0, (self.game_window_size[1] / 2 - self.size / 2) - self.hero.pos[1] * self.size)
        elif self.map_size[0] - (self.hero.pos[0] + 1) * self.size < (self.game_window_size[0] / 2 - self.size / 2):
            if self.hero.pos[1] * self.size < (self.game_window_size[1] / 2 - self.size / 2):
                map_pos = (self.game_window_size[0] - self.map_size[0], 0)
            elif self.map_size[1] - self.hero.pos[1] * self.size < (self.game_window_size[1] / 2 - self.size / 2):
                map_pos = (self.game_window_size[0] - self.map_size[0], self.game_window_size[1] - self.map_size[1])
            else:
                map_pos = (self.game_window_size[0] - self.map_size[0],
                           (self.game_window_size[1] / 2) - self.hero.pos[1] * self.size)
        elif self.hero.pos[1] * self.size < (self.game_window_size[1] / 2 - self.size / 2):
            map_pos = ((self.game_window_size[0] / 2 - self.size / 2) - self.hero.pos[0] * self.size, 0)
        elif self.map_size[1] - (self.hero.pos[1] + 1) * self.size < (self.game_window_size[1] / 2 - self.size / 2):
            map_pos = ((self.game_window_size[0] / 2 - self.size / 2) - self.hero.pos[0] * self.size,
                       self.game_window_size[1] - self.map_size[1])
        else:
            map_pos = ((self.game_window_size[0] / 2 - self.size / 2) - self.hero.pos[0] * self.size,
                       (self.game_window_size[1] / 2 - self.size / 2) - self.hero.pos[1] * self.size,)
        return map_pos

    def draw_enemies(self, work_surface):
        for enemy in self.map.enemies:
            work_surface.blit(type(enemy).sprite, ((enemy.pos[0] - 1) * self.size, (enemy.pos[1] - 1) * self.size))

    def draw_items(self, work_surface):
        for item in self.map.items:
            work_surface.blit(type(item).sprite, ((item.pos[0] - 1) * self.size, (item.pos[1] - 1) * self.size))


class Info:
    def __init__(self, size, hero):
        self.size = size
        self.hero = hero
        self.info_window = None
        self.draw_info()

    def draw_info(self):
        self.info_window = pygame.Surface(self.size)
        self.info_window.fill((255, 193, 100))
        font = pygame.font.SysFont("courier", 25, True)
        self.info_window.blit(font.render('Strength: '+str(self.hero.strength), True, (0, 0, 0)), (50, 20))
        self.info_window.blit(font.render('Endurance: ' + str(self.hero.endurance), True, (0, 0, 0)), (50, 70))
        self.info_window.blit(font.render('Level: ' + str(self.hero.level), True, (0, 0, 0)), (50, 120))
        self.info_window.blit(font.render('Weapon: ' + str(self.hero.weapon), True, (0, 0, 0)), (50, 170))
        self.info_window.blit(font.render('Armor: ' + str(self.hero.armor), True, (0, 0, 0)), (50, 220))
        self.info_window.blit(font.render('Boot: ' + str(self.hero.boot), True, (0, 0, 0)), (50, 270))


class Interface:
    def __init__(self, size, hero):
        self.size = size
        self.hero = hero
        self.interface_window = None
        self.draw_interface()

    def draw_interface(self):
        self.interface_window = pygame.Surface(self.size)
        self.interface_window.fill((255, 193, 115))
        self.draw_text(self.interface_window)
        self.draw_rect(self.interface_window)

    def draw_text(self, work_surface):
        font = pygame.font.SysFont("arial", 65, True)
        work_surface.blit(font.render('HP:', True, (0, 0, 0)), (50, 50))
        work_surface.blit(font.render('EXP:', True, (0, 0, 0)), (50, 175))
        work_surface.blit(font.render(str(self.hero.hp)+'/'+str(self.hero.endurance*2), True, (0, 0, 0)), (1000, 50))
        work_surface.blit(font.render(str(self.hero.exp)+'/'+str(self.hero.level*10), True, (0, 0, 0)), (1000, 175))

    def draw_rect(self, work_surface):
        pygame.draw.rect(work_surface, (255, 0, 0), (250, 50, 700*self.hero.hp/(self.hero.endurance*2), 65))
        pygame.draw.rect(work_surface, (0, 0, 255), (250, 175, 700*self.hero.exp/(self.hero.level*10), 65))


class Log:
    def __init__(self, size):
        self.size = size
        self.log_window = None
        self.log_list = []
        self.draw_log()

    def draw_log(self):
        self.log_window = pygame.Surface(self.size)
        self.log_window.fill((255, 180, 100))
        font = pygame.font.SysFont("courier", 20, True, True)
        counter = 20
        for message in self.log_list:
            self.log_window.blit(font.render(message, True, (0, 0, 0)), (50, counter))
            counter += 40

    def update(self, message):
        if len(self.log_list) <= 10:
            self.log_list.append(message)
        else:
            self.log_list.pop(0)
            self.log_list.append(message)
        self.draw_log()
