from abc import ABC, abstractmethod
import Service
import os


class Hero:
    def __init__(self, icon=None):
        self.sprite = icon
        self.level = 1
        self.exp = 0
        self.strength = 5
        self.endurance = 5
        self.hp = self.endurance * 2
        self.pos = []
        self.weapon = None
        self.armor = None
        self.boot = None


class ObjectsFactory(ABC):
    @classmethod
    def create_object(cls, pos):
        return cls(pos)

    @classmethod
    def change_sprite_size(cls, size):
        cls.size = size
        cls.sprite = Service.create_sprite(os.path.join(cls.directory, cls.file_name), cls.size)

    @abstractmethod
    def interact(self, hero, obj):
        pass


class Enemy(ObjectsFactory):
    def interact(self, hero, enemies):
        self.hp -= hero.strength
        hero.hp -= self.strength
        if hero.hp <= 0:
            return 0
        answer = []
        if self.hp <= 0:
            hero.exp += self.exp
            enemies.remove(self)
            answer.append('Hero killed ' + self.__class__.__name__)
            while hero.exp >= 10 * hero.level:
                hero.exp -= 10 * hero.level
                hero.level += 1
                answer.append('Hero level increased!')
                hero.strength += 2
                hero.endurance += 2
                hero.hp = hero.endurance * 2
        return answer


class Skeleton(Enemy):
    size = 60
    directory = "texture/enemies"
    file_name = "skeleton.png"
    sprite = None

    def __init__(self, pos):
        self.hp = 4
        self.pos = pos
        self.strength = 2
        self.exp = 6


class SkeletonShaman(Enemy):
    size = 60
    directory = "texture/enemies"
    file_name = "skeleton_shaman.png"
    sprite = None

    def __init__(self, pos):
        self.hp = 3
        self.pos = pos
        self.strength = 3
        self.exp = 8


class Spearman(Enemy):
    size = 60
    directory = "texture/enemies"
    file_name = "spearman.png"
    sprite = None

    def __init__(self, pos):
        self.hp = 5
        self.pos = pos
        self.strength = 1
        self.exp = 5


class Archer(Enemy):
    size = 60
    directory = "texture/enemies"
    file_name = "archer.png"
    sprite = None

    def __init__(self, pos):
        self.hp = 4
        self.pos = pos
        self.strength = 4
        self.exp = 9


class DarkKnight(Enemy):
    size = 60
    directory = "texture/enemies"
    file_name = "dark_knight.png"
    sprite = None

    def __init__(self, pos):
        self.hp = 20
        self.pos = pos
        self.strength = 10
        self.exp = 30


class Dragon(Enemy):
    size = 60
    directory = "texture/enemies"
    file_name = "dragon.png"
    sprite = None

    def __init__(self, pos):
        self.hp = 50
        self.pos = pos
        self.strength = 20
        self.exp = 80


class Sword(ObjectsFactory):
    size = 60
    directory = "texture/items"
    file_name = "sword.png"
    sprite = None

    def __init__(self, pos):
        self.pos = pos
        self.strength = 5

    def interact(self, hero, items):
        hero.strength += self.strength
        hero.weapon = self.__class__.__name__
        items.remove(self)
        answer = ['Hero get ' + self.__class__.__name__]
        return answer


class Armor(ObjectsFactory):
    size = 60
    directory = "texture/items"
    file_name = "armor.png"
    sprite = None

    def __init__(self, pos):
        self.pos = pos
        self.strength = 7

    def interact(self, hero, items):
        hero.strength += self.strength
        hero.armor = self.__class__.__name__
        items.remove(self)
        answer = ['Hero get ' + self.__class__.__name__]
        return answer


class Boot(ObjectsFactory):
    size = 60
    directory = "texture/items"
    file_name = "boot.png"
    sprite = None

    def __init__(self, pos):
        self.pos = pos
        self.endurance = 7

    def interact(self, hero, items):
        hero.endurance += self.endurance
        hero.hp += self.endurance * 2
        hero.boot = self.__class__.__name__
        items.remove(self)
        answer = ['Hero get ' + self.__class__.__name__]
        return answer
