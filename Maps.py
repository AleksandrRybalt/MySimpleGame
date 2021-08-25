import json
import Objects

maps_list = ['Map1.json', 'Map2.json']


class MapFactory:
    def __init__(self, file):
        self.file = file
        self.map_size = None
        self.hero_start = None
        self.objects, self.enemies, self.items = self.get_objects()

    def get_objects(self):
        objects = {}
        with open(self.file, 'r') as file:
            data = dict(json.loads(file.read()))
        self.map_size = data['map_size']
        self.hero_start = data['hero']
        if 'doors' in data:
            objects['doors'] = data['doors']
        objects['trees'] = self.trees(data['trees'])
        enemies = self.create_enemies(data['enemies'])
        items = self.create_items(data['items'])
        return objects, enemies, items

    @staticmethod
    def doors(data):
        doors = []
        for i in data:
            doors.append([i[0], i[1]])
        return doors

    @staticmethod
    def trees(data):
        trees = []
        for y in data:
            for x in data[y]:
                if isinstance(x, int):
                    trees.append([x-1, int(y)-1])
                else:
                    for x_x in range(x[0], x[1]+1):
                        trees.append([x_x-1, int(y)-1])
        return trees

    @staticmethod
    def create_enemies(data):
        enemies = []
        for enemy in data:
            if enemy == "Skeleton":
                enemies.extend([Objects.Skeleton.create_object(pos) for pos in data[enemy]])
            elif enemy == "SkeletonShaman":
                enemies.extend([Objects.SkeletonShaman.create_object(pos) for pos in data[enemy]])
            elif enemy == "Spearman":
                enemies.extend([Objects.Spearman.create_object(pos) for pos in data[enemy]])
            elif enemy == "Archer":
                enemies.extend([Objects.Archer.create_object(pos) for pos in data[enemy]])
            elif enemy == "DarkKnight":
                enemies.extend([Objects.DarkKnight.create_object(pos) for pos in data[enemy]])
            elif enemy == "Dragon":
                enemies.extend([Objects.Dragon.create_object(pos) for pos in data[enemy]])
        return enemies

    @staticmethod
    def create_items(data):
        items = []
        for item in data:
            if item == "Sword":
                items.extend([Objects.Sword.create_object(pos) for pos in data[item]])
            elif item == "Armor":
                items.extend([Objects.Armor.create_object(pos) for pos in data[item]])
            elif item == "Boot":
                items.extend([Objects.Boot.create_object(pos) for pos in data[item]])
        return items
