from game.core import Entity
import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

    label = "S.P.E.C.I.A.L."

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

        self.stat = Stat('images/special_strength.png')
        self.stat.rect[0] = 4
        self.stat.rect[1] = 40
        self.add(self.stat)

        self.menu = pypboy.ui.Menu(240, [
            "Strength               4", 
            "Perception             7", 
            "Endurance              5", 
            "Charisma               6", 
            "Intelligence           9", 
            "Agility                4", 
            "Luck                   6"], [self.show_str, self.show_per, self.show_end, self.show_cha, self.show_int, self.show_agi, self.show_luc], 0)
        self.menu.rect[0] = 4
        self.menu.rect[1] = 60
        self.add(self.menu)

    def changeStat(self, imageUrl):
        self.stat.image = pygame.image.load(imageUrl)
        self.stat.rect = self.stat.image.get_rect()
        self.stat.rect[0] = 100
        self.stat.rect[1] = 0
        self.stat.image = self.stat.image.convert_alpha()

    def show_str(self):
        self.changeStat('images/special_strength.png')
        print("Strength")

    def show_per(self):
        self.changeStat('images/special_perception.png')
        print("Perception")

    def show_end(self):
        self.changeStat('images/special_endurance.png')
        print("Endurance")

    def show_cha(self):
        self.changeStat('images/special_charisma.png')
        print("Charisma")

    def show_int(self):
        self.changeStat('images/special_intelligence.png')
        print("Intelligence")

    def show_agi(self):
        self.changeStat('images/special_agility.png')
        print("Agility")

    def show_luc(self):
        self.changeStat('images/special_luck.png')
        print("Luck")

class Stat(game.Entity):
    def __init__(self, imageUrl):
        super(Stat, self).__init__()
        self.image = pygame.image.load(imageUrl)
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
