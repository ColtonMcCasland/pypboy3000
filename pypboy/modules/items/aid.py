import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

    label = "Aid"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

        self.menu = pypboy.ui.Menu(200, config.AID, [], 0)
        self.menu.rect[0] = 4
        self.menu.rect[1] = 60
        self.add(self.menu)