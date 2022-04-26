import game
import config
import pygame
import datetime


class Header(game.Entity):

    def __init__(self, headline="", title=[]):
        self.headline = headline
        self.title = []
        super(Header, self).__init__((config.WIDTH, config.HEIGHT))
        self.rect[0] = 4
        self._date = None

    def update(self, *args, **kwargs):
        super(Header, self).update(*args, **kwargs)

    def render(self, *args, **kwargs):
        new_date = datetime.datetime.now().strftime("%d.%m.%y.%H:%M:%S") #need to be moved to footer and under the data and maps section
        if new_date != self._date:
            self.image.fill((0, 0, 0))
            pygame.draw.line(self.image, config.TINTCOLOUR, (5, 15), (5, 35), 2)
            #pygame.draw.line(self.image, (95, 255, 177), (5, 15), (config.WIDTH - 154, 15), 2)
            pygame.draw.line(self.image, config.TINTCOLOUR, (config.WIDTH - 148, 15), (config.WIDTH - 13, 15), 2)
            pygame.draw.line(self.image, config.TINTCOLOUR, (config.WIDTH - 13, 15), (config.WIDTH - 13, 35), 2)


            text = config.FONTS[14].render(self._date, True, config.TINTCOLOUR, (0, 0, 0))
            self.image.blit(text, ((config.WIDTH - 141), 19))
            headerposcount = 146
            for section in self.title:
                headerposcount = headerposcount + 8
                headerposcount_old = headerposcount
                text = config.FONTS[14].render(section, True, config.TINTCOLOUR, (0, 0, 0))
                pygame.draw.line(self.image, config.TINTCOLOUR, (config.WIDTH - headerposcount, 15), (config.WIDTH - headerposcount, 35), 2)	#End of title Verticle bar
                headerposcount = headerposcount + text.get_width() + 5
                self.image.blit(text, (config.WIDTH - headerposcount, 19))
                pygame.draw.line(self.image, config.TINTCOLOUR, (config.WIDTH - headerposcount, 15), (config.WIDTH - headerposcount_old, 15), 2) # Horizontal Bar
            pygame.draw.line(self.image, config.TINTCOLOUR, (5, 15), (config.WIDTH - headerposcount, 15), 2) # Horizontal Bar
            text = config.FONTS[14].render("  %s  " % self.headline, True, config.TINTCOLOUR, (0, 0, 0))
            self.image.blit(text, (26, 8))
            self._date = new_date
            



        super(Header, self).update(*args, **kwargs)


class Footer(game.Entity):

    def __init__(self):
        self.menu = []
        super(Footer, self).__init__((config.WIDTH, config.HEIGHT))
        self.rect[0] = 4
        self.rect[1] = config.HEIGHT - 40

    def update(self, *args, **kwargs):
        super(Footer, self).update(*args, **kwargs)

    def select(self, module):
        #self.dirty = 1
        self.selected = module
        self.image.fill((0, 0, 0))
        pygame.draw.line(self.image, (config.TINTCOLOUR), (5, 2), (5, 20), 2)
        pygame.draw.line(self.image, (config.TINTCOLOUR), (5, 20), (config.WIDTH - 13, 20), 2)
        pygame.draw.line(self.image, (config.TINTCOLOUR), (config.WIDTH - 13, 2), (config.WIDTH - 13, 20), 2)

        offset = 20
        for m in self.menu:
            padding = 1
            text_width = 0
            while text_width < 54:
                spaces = " ".join([" " for x in range(padding)])
                text = config.FONTS[12].render("%s%s%s" % (spaces, m, spaces), True, config.TINTCOLOUR, (0, 0, 0))
                text_width = text.get_size()[0]
                padding += 1
            #print(m+" : "+str(text.get_size()))
            if m == self.selected:
                pygame.draw.rect(self.image, (config.TINTCOLOUR), (offset - 2, 6, (text_width + 3), 26), 2)
            self.image.blit(text, (offset, 12))

            offset = offset + 120 + (text_width - 100)


class Menu(game.Entity):

    def __init__(self, width, items=[], callbacks=[], selected=0, xoffset=5):
        super(Menu, self).__init__((width, config.HEIGHT - 80))
        self.items = items
        self.callbacks = callbacks
        self.menuXVal = xoffset
        self.selected = 0
        self.select(selected)

        if config.SOUND_ENABLED:
            self.dial_move_sfx = pygame.mixer.Sound('sounds/dial_move.ogg')

    def select(self, item):
        self.selected = item
        self.redraw()
        if len(self.callbacks) > item and self.callbacks[item]:
            self.callbacks[item]()

    def handle_action(self, action):

        if config.GPIO_AVAILABLE:

            if action == "dial_up":
                print('up')
                if self.selected > 0:
                    if config.SOUND_ENABLED:
                        self.dial_move_sfx.play()
                    self.select(self.selected - 1)
            if action == "dial_down":
                print('down')
                if self.selected < len(self.items) - 1:
                    if config.SOUND_ENABLED:
                        self.dial_move_sfx.play()
                    self.select(self.selected + 1)

        else:
            if action == "dial_up":
                if self.selected > 0:
                    if config.SOUND_ENABLED:
                        self.dial_move_sfx.play()
                    self.select(self.selected - 1)
            if action == "dial_down":
                if self.selected < len(self.items) - 1:
                    if config.SOUND_ENABLED:
                        self.dial_move_sfx.play()
                    self.select(self.selected + 1)


    def redraw(self):
        self.image.fill((0, 0, 0))
        offset = 5
        for i in range(len(self.items)):
            text = config.FONTS[14].render(" %s " % self.items[i], True, config.TINTCOLOUR, (0, 0, 0))
            if i == self.selected:
                selected_rect = (self.menuXVal, offset - 2, text.get_size()[0] + 10, text.get_size()[1] + 3)
                pygame.draw.rect(self.image, (config.TINTCOLOUR), selected_rect, 2)
            self.image.blit(text, (self.menuXVal + 5, offset))
            offset += text.get_size()[1] + 6
        
    def handle_tap(self):
        print("Handle Tap")
        if config.RADIO_PLAYING:
            config.RADIO_PLAYING = False
        else:
            config.RADIO_PLAYING = True

        x,y = pygame.mouse.get_pos()
        offset = 5 + self.rect[1]
        print("X: " + str(x) + " Y: " + str(y))
        for i in range(len(self.items)):
            text = config.FONTS[14].render(" %s " % self.items[i], True, config.TINTCOLOUR, (0, 0, 0))
            menuRect = (self.menuXVal, offset - 2, text.get_size()[0] + 10, text.get_size()[1] + 3)
            print (menuRect)
            if x >= menuRect[0] and x < (menuRect[0] + menuRect[2]) and y >= menuRect[1] and y < (menuRect[1] + menuRect[3]) and i != self.selected:
                self.select(i)
                return True
            offset += text.get_size()[1] + 6
        return False


class Scanlines(game.Entity):

    def __init__(self, width, height, gap, speed, colours, full_push=False):
        super(Scanlines, self).__init__((width, height))
        self.width = width
        self.height = height
        self.move = gap * len(colours)
        self.gap = gap
        self.colours = colours
        self.rect[1] = 0
        self.top = 0.0
        self.speed = speed
        self.full_push =full_push
        colour = 0
        area = pygame.Rect(0, self.rect[1] * self.speed, self.width, self.gap)
        while area.top <= self.height - self.gap:
            self.image.fill(self.colours[colour], area)
            area.move_ip(0, (self.gap))
            colour += 1
            if colour >= len(self.colours):
                colour = 0

    def render(self, interval, *args, **kwargs):
        self.top += self.speed * interval
        self.rect[1] = self.top
        self.dirty = 1
        if self.full_push:
            if self.top >= self.height:
                self.top = 0
        else:
            if (self.top * self.speed) >= self.move:
                self.top = 0
        super(Scanlines, self).render(self, *args, **kwargs)


class Overlay(game.Entity):
    def __init__(self):
        self.image = pygame.image.load('images/overlay.png')
        super(Overlay, self).__init__((config.WIDTH, config.HEIGHT))
        self.blit_alpha(self, self.image, (0, 0), 128)

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert_alpha()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)


class Border(game.Entity):
    def __init__(self):
        super(Border, self).__init__()
        self.image = pygame.image.load('images/border.png')
        self.rect = self.image.get_rect()