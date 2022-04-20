import pypboy
import pygame
import game
import config
import pypboy.ui


class Module(pypboy.SubModule):

    label = "Status"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        health = Health()
        health.rect[0] = 4
        health.rect[1] = 40
        self.add(health)
        self.menu = pypboy.ui.Menu(100, ["CND", "RAD", "EFF"], [self.show_cnd, self.show_rad, self.show_eff], 0)
        self.menu.rect[0] = 4
        self.menu.rect[1] = 60
        self.add(self.menu)


    def show_cnd(self):
        print("CND")

    def show_rad(self):
        print("RAD")

    def show_eff(self):
        print("EFF")


class Health(game.Entity):

    def __init__(self):
        super(Health, self).__init__()

        self.image = pygame.image.load('images/pipboy.png').convert_alpha()
        self.image.fill((config.TINTCOLOUR), None, pygame.BLEND_RGB_MULT)
        # self.image.set_colorkey((255, 182, 66))

        self.rect = self.image.get_rect()
        self.image.blit(self.image, (0, -15))

        # self.image = self.image.set_colorkey((255,0,255))        # self.image = self.image.convert()
        # self.image.set_alpha(10)
        text = ("%s - LVL %s" % (config.PLAYERNAME, config.PLAYERLEVEL))
        text = config.FONTS[14].render(text, True, config.TINTCOLOUR, (0, 0, 0))

        text_width = text.get_size()[0]
        # self.image = self.image.blit(self.image, (0,  150))
        self.image.blit(text, (config.WIDTH / 2 - 8 - text_width / 2, config.HEIGHT - 90))
