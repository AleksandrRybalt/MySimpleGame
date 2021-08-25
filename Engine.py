import Maps
import Service
import os
import Objects

all_obj_without_hero = [Objects.Skeleton, Objects.SkeletonShaman, Objects.Spearman, Objects.Archer,
                        Objects.DarkKnight, Objects.Dragon, Objects.Sword, Objects.Armor, Objects.Boot]


class Engine:
    def __init__(self, hero, game_window_size, interface_size, info_size, log_size):
        self.working = True
        self.hero = hero
        self.game_window_size = game_window_size
        self.map = None
        self.map_number = -1
        self.objects = all_obj_without_hero

        self.interface = Service.Interface(interface_size, self.hero)
        self.info = Service.Info(info_size, self.hero)
        self.log = Service.Log(log_size)
        self.subscribers = {self.log}

        self.start()

    def start(self):
        self.create_images()
        self.next_map()
        self.draw_map = Service.DrawMap(self.map, self.hero, self.game_window_size)
        self.hero.pos = [self.map.hero_start[0], self.map.hero_start[1]]
        self.interface.draw_interface()
        self.info.draw_info()

    def create_images(self):
        for obj in self.objects:
            obj.sprite = Service.create_sprite(os.path.join(obj.directory, obj.file_name), obj.size)

    def next_map(self):
        self.map_number += 1
        self.map = Maps.MapFactory('Maps/' + Maps.maps_list[self.map_number])
        self.hero.pos = [self.map.hero_start[0], self.map.hero_start[1]]
        self.draw_map = Service.DrawMap(self.map, self.hero, self.game_window_size)
        self.notify('Hero moved to the next map')

    def game_window_plus(self):
        if self.draw_map.size >= 140:
            return
        self.draw_map.size += 20
        for obj in self.objects:
            obj.size = self.draw_map.size
        self.create_images()
        self.draw_map.draw_map()

    def game_window_minus(self):
        if self.draw_map.size <= 20:
            return
        self.draw_map.size -= 20
        for obj in self.objects:
            obj.size = self.draw_map.size
        self.create_images()
        self.draw_map.draw_map()

    def move_up(self):
        if [self.hero.pos[0] - 1, self.hero.pos[1] - 2] in self.map.objects['trees'] or self.hero.pos[1] == 1:
            return
        action_result = self.action([0, -1])
        if action_result:
            self.hero.pos[1] -= 1
            self.draw_map.draw_map()

    def move_down(self):
        if [self.hero.pos[0] - 1, self.hero.pos[1]] in self.map.objects['trees'] or \
                self.hero.pos[1] + 1 == self.map.map_size[1]:
            return
        action_result = self.action([0, 1])
        if action_result:
            self.hero.pos[1] += 1
            self.draw_map.draw_map()

    def move_left(self):
        if [self.hero.pos[0] - 2, self.hero.pos[1] - 1] in self.map.objects['trees'] or self.hero.pos[0] == 1:
            return
        action_result = self.action([-1, 0])
        if action_result:
            self.hero.pos[0] -= 1
            self.draw_map.draw_map()

    def move_right(self):
        if [self.hero.pos[0], self.hero.pos[1] - 1] in self.map.objects['trees'] or \
                self.hero.pos[0] + 1 == self.map.map_size[0]:
            return
        action_result = self.action([1, 0])
        if action_result:
            self.hero.pos[0] += 1
            self.draw_map.draw_map()

    def action(self, correction):
        for obj in self.map.enemies:
            if [self.hero.pos[0] + correction[0], self.hero.pos[1] + correction[1]] == obj.pos:
                self.action_enemies(obj)
                return False
        for coord in self.map.objects["doors"]:
            if [self.hero.pos[0] + correction[0], self.hero.pos[1] + correction[1]] == coord:
                self.action_doors()
                return False
        for obj in self.map.items:
            if [self.hero.pos[0] + correction[0], self.hero.pos[1] + correction[1]] == obj.pos:
                self.action_items(obj)
        self.interface.draw_interface(), self.info.draw_info()
        return True

    def action_enemies(self, obj):
        answer = obj.interact(self.hero, self.map.enemies)
        if answer == 0:
            self.working = False
        else:
            for message in answer:
                self.notify(message)
        self.draw_map.draw_map(), self.interface.draw_interface(), self.info.draw_info()

    def action_doors(self):
        self.next_map(), self.interface.draw_interface(), self.info.draw_info()

    def action_items(self, obj):
        answer = obj.interact(self.hero, self.map.items)
        for message in answer:
            self.notify(message)

    def notify(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)
