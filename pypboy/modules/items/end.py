import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

    label = "next"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self.active.handle_action("module_change_next")