import pygame
import pypboy
import config

from pypboy.modules.data import entities


class Module(pypboy.SubModule):
    label = "World Map"
    title = "Jefferson City"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        if config.LOAD_CACHED_MAP:
            mapgrid = entities.Map(480, pygame.Rect(0, 0, config.WIDTH - 8, config.HEIGHT - 80), "Loading cached map")
            mapgrid.load_map(config.MAP_FOCUS, config.WORLD_MAP_FOCUS, True)
        else:
            mapgrid = entities.Map(480, pygame.Rect(0, 0, config.WIDTH - 8, config.HEIGHT - 80), "Fetching cached map")
            mapgrid.fetch_map(config.MAP_FOCUS, config.WORLD_MAP_FOCUS, True)
        self.add(mapgrid)
        mapgrid.rect[0] = 4
        mapgrid.rect[1] = 40

    def handle_resume(self):
        self.parent.pypboy.header.headline = "DATA"
        self.parent.pypboy.header.title = [self.title]
        super(Module, self).handle_resume()