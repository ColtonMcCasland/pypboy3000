import pygame
import game
import config
import pypboy.ui
from enum import Enum

if config.GPIO_AVAILABLE:
    import RPi.GPIO as GPIO


class GameState(Enum):
    RADIO = -3
    MAP = -2
    DATA = -1
    inv = 0
    STATS = 1


class BaseModule(game.EntityGroup):
    submodules = []
    currentSubmodule = 0

    def __init__(self, boy, *args, **kwargs):
        super(BaseModule, self).__init__()


        self.pypboy = boy
        self.position = (0, 40)

        self.footer = pypboy.ui.Footer()
        self.footer.menu = []
        for mod in self.submodules:
            self.footer.menu.append(mod.label)
        self.footer.selected = self.footer.menu[0]
        self.footer.position = (0, config.HEIGHT - 53)  # 80
        self.add(self.footer)

        self.switch_submodule(0)

        self.action_handlers = {
            "pause": self.handle_pause,
            "resume": self.handle_resume
        }
        if config.SOUND_ENABLED:
            self.module_change_sfx = pygame.mixer.Sound('sounds/module_change.ogg')

    def move(self, x, y):
        super(BaseModule, self).move(x, y)
        if hasattr(self, 'active'):
            self.active.move(x, y)

    def switch_submodule(self, module):
        print("Changing submodules")
        if hasattr(self, 'active') and self.active:
            self.active.handle_action("pause")
            self.remove(self.active)
        if len(self.submodules) > module:
            self.active = self.submodules[module]
            self.active.parent = self
            self.active.handle_action("resume")
            self.footer.select(self.footer.menu[module])
            self.add(self.active)
        else:
            print("No submodule at %d" % module)

    def render(self, interval):
        self.active.render(interval)
        super(BaseModule, self).render(interval)

    def button_callback(channel):
        print("Button was pushed!")

    def handle_action(self, action, value=0):
        if action.startswith("knob_"):
            if config.GPIO_AVAILABLE:
                # NEEDS TWEAKING: GLITCHY INTERFACE EXPERIENCE WITH KNOB
                if action.startswith("knob_"):
                    if action == "knob_down":
                        self.currentSubmodule -= 1
                        if self.currentSubmodule < 0:
                            self.currentSubmodule = 0
                    if action == "knob_up":
                        if self.currentSubmodule > self.submodules.__len__():
                            self.currentSubmodule = self.submodules.__len__()
                        else:
                            self.currentSubmodule += 1
                    self.switch_submodule(self.currentSubmodule)
            else:
                num = int(action[-1])
                self.switch_submodule(num - 1)
        elif action in self.action_handlers:
            self.action_handlers[action]()
        else:
            if hasattr(self, 'active') and self.active:
                self.active.handle_action(action, value)

    def handle_event(self, event):
        if hasattr(self, 'active') and self.active:
            self.active.handle_event(event)

    def handle_pause(self):
        self.paused = True
        self.currentSubmodule = 0
        self.switch_submodule(0)
        # if config.GPIO_AVAILABLE:
        # GPIO.output(self.GPIO_LED_ID, False)

    def handle_resume(self):
        self.paused = False
        self.currentSubmodule = 0
        self.switch_submodule(0)
        # if config.GPIO_AVAILABLE:
        #     GPIO.output(self.GPIO_LED_ID, True)
        if config.SOUND_ENABLED:
            self.module_change_sfx.play()

    def handle_swipe(self, swipe):
        print("Handle Swipe " + str(swipe))
        if swipe == 2:
            self.currentSubmodule -= 1
            if self.currentSubmodule < 0:
                self.currentSubmodule = self.submodules.__len__() - 1
            self.switch_submodule(self.currentSubmodule)
        elif swipe == 1:
            self.currentSubmodule += 1
            if self.currentSubmodule >= self.submodules.__len__():
                self.currentSubmodule = 0
            self.switch_submodule(self.currentSubmodule)
        else:
            self.active.handle_tap()


class SubModule(game.EntityGroup):

    def __init__(self, parent, *args, **kwargs):
        super(SubModule, self).__init__()
        self.parent = parent

        self.action_handlers = {
            "pause": self.handle_pause,
            "resume": self.handle_resume
        }

        if config.SOUND_ENABLED:
            self.submodule_change_sfx = pygame.mixer.Sound('sounds/submodule_change.ogg')

    def handle_action(self, action, value=0):
        if action.startswith("dial_"):
            if hasattr(self, "menu"):
                self.menu.handle_action(action)
        elif action in self.action_handlers:
            self.action_handlers[action]()

    def handle_event(self, event):
        pass

    def handle_pause(self):
        self.paused = True

    def handle_resume(self):
        self.paused = False
        if config.SOUND_ENABLED:
            self.submodule_change_sfx.play()

    def handle_tap(self):
        pass
