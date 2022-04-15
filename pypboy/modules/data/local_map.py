import pygame
import pypboy
import config

from pypboy.modules.data import entities

class Module(pypboy.SubModule):
    label = "Local Map"
    title = "Cosplacon"
    zoom = 0.003

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self.mapgrid = entities.Map(config.WIDTH, pygame.Rect(4, (config.WIDTH - config.HEIGHT) / 2, config.WIDTH - 8, config.HEIGHT - 80))
        if(config.LOAD_CACHED_MAP):
            print("Loading cached map")
            self.mapgrid = entities.Map(config.WIDTH, pygame.Rect(4, (config.WIDTH - config.HEIGHT) / 2, config.WIDTH - 8, config.HEIGHT - 80), "Loading cached map")
            self.mapgrid.load_map(config.MAP_FOCUS, self.zoom, False)
        else:
            print("Loading map from the internet")
            self.mapgrid = entities.Map(config.WIDTH, pygame.Rect(4, (config.WIDTH - config.HEIGHT) / 2, config.WIDTH - 8, config.HEIGHT - 80), "Loading map from the internet")
            self.mapgrid.fetch_map(config.MAP_FOCUS, self.zoom, False)
        self.add(self.mapgrid)
        self.mapgrid.rect[0] = 4
        self.mapgrid.rect[1] = 40
    
    def handle_action(self, action, value=0):
        if action == "zoom_in":
            self.zoomMap(-0.003)
        if action == "zoom_out":
            self.zoomMap(0.003)

    def handle_resume(self):
        self.parent.pypboy.header.headline = "DATA"
        self.parent.pypboy.header.title = [self.title]
        super(Module, self).handle_resume()

    def handle_tap(self):
        x,y = pygame.mouse.get_pos()
        if x < (config.WIDTH / 2):
            self.zoomMap(-0.003)
        if x > (config.WIDTH / 2):
            self.zoomMap(0.003)

    def zoomMap(self, zoomFactor):
        self.zoom = self.zoom + zoomFactor
        if config.LOAD_CACHED_MAP:
            print("Loading cached map")
            self.mapgrid.load_map(config.MAP_FOCUS, self.zoom, False)
        else:
            print("Loading map from the internet")
            self.mapgrid.fetch_map(config.MAP_FOCUS, self.zoom, False)
        
        self.add(self.mapgrid)
        self.mapgrid.rect[0] = 4
        self.mapgrid.rect[1] = 40
        self.parent.pypboy.header.headline = "DATA"
        self.parent.pypboy.header.title = [self.title]
    