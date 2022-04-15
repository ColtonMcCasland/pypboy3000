import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

    label = "General"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)