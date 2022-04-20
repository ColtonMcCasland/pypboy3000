import pygame
import time

from pygame import KEYDOWN, MOUSEMOTION, MOUSEBUTTONDOWN, QUIT

import config
from pypboy.boot.cmdlinebootup import CmdLineClass


class Engine(object):

    EVENTS_UPDATE = pygame.USEREVENT + 1
    EVENTS_RENDER = pygame.USEREVENT + 2

    def __init__(self, title, width, height, *args, **kwargs):
        super(Engine, self).__init__(*args, **kwargs)
        pygame.init()
        pygame.display.init()


        self.rootParent = self

        # ------------------ Hard Code Screen Size ----------------------
        self.screenSize = (config.WIDTH, config.HEIGHT)
        self.canvasSize = (config.WIDTH, config.HEIGHT)
        # ---------------------------------------------------------------

        # self.window = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
        self.window = pygame.display.set_mode((width, height))
        self.screen = pygame.display.get_surface()
        pygame.display.set_mode(self.screenSize)


        # Block queuing for unused events:
        pygame.event.set_blocked(None)
        for ev in (QUIT, KEYDOWN):
            pygame.event.set_allowed(ev)


        pygame.display.set_caption(title)
        pygame.mouse.set_visible(False)

        self.groups = []
        self.root_children = EntityGroup()
        self.background = pygame.surface.Surface(self.screen.get_size()).convert_alpha()
        backAdd = 30
        self.background.fill((backAdd, backAdd, backAdd), None, pygame.BLEND_RGB_ADD)

        self.rescale = False
        self.last_render_time = 0

        # Scanlines:
        # self.scanline = pygame.image.load('images/pipboyscanlines.png'),
        self.lineCount = 80  # 48 60 80
        self.lineHeight = config.HEIGHT // self.lineCount
        scanline = pygame.transform.smoothscale(pygame.image.load('images/pipboyscanlines.png'), (config.WIDTH, self.lineHeight))

        self.scanLines = pygame.Surface(self.canvasSize)
        yPos = 0
        while yPos < config.HEIGHT:
            self.scanLines.blit(scanline, (0, yPos))
            yPos += self.lineHeight

        # Increase contrast, darken:
        self.scanLines.blit(self.scanLines, (0, 0), None, pygame.BLEND_RGB_MULT)

        # scanMult = 0.5
        scanMult = 0.7
        # scanMultColour = (scanMult * 255, scanMult * 255, scanMult * 255)
        self.scanLines = self.scanLines.convert_alpha()
        self.scanLines.fill(config.TINTCOLOUR, None, pygame.BLEND_RGB_MULT)

        # Start humming sound:
        if config.SOUND_ENABLED:
            self.humSound = pygame.mixer.Sound('sounds/pipboy_hum.wav')
            self.humSound.play(loops=-1)
            self.humVolume = self.humSound.get_volume()

            # Set up data for generating overlay frames

            self.distortLineHeight = (config.HEIGHT // 4)
            self.distortLine = pygame.transform.smoothscale(pygame.image.load('images/pipboydistorteffectmap.png'), (config.WIDTH, self.distortLineHeight))
            self.distortLine = self.distortLine.convert()
            self.distortY = -self.distortLineHeight
            self.distortSpeed = (config.HEIGHT / 40)
            self.overlayFrames = []

            print("START")

            cmdLine = CmdLineClass(self)

            bootPrintQueue = [
                "WELCOME TO ROBCO INDUSTRIES (TM) TERMLINK",
                ">SET TERMINAL/INQUIRE",
                "",
                "RIT-V300",
                "",
                ">SET FILE/PROTECTION=OWNER:RWED ACCOUNTS.F",
                ">SET HALT RESTART/MAINT",
                "",
                "Initializing Robco Industries(TM) MF Boot Agent v2.3.0",
                "RETROS BIOS",
                "RBIOS-4.02.08.00 52EE5.E7.E8",
                "Copyright 2201-2203 Robco Ind.",
                "Uppermem: 64 KB",
                "Root (5A8)",
                "Maintenance Mode",
                "",
                ">RUN DEBUG/ACCOUNTS.F",
                "**cls",
                "ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM",
                "COPYRIGHT 2075-2077 ROBCO INDUSTRIES",
                "",
            ]

            # Print Robco boot-up text, interleaving lines with overlay-frame generation:
            lineNum = 0
            canPrint = True
            genOverlays = True
            while (canPrint or genOverlays):
                willPrint = (lineNum < len(bootPrintQueue))
                if canPrint:
                    thisLine = bootPrintQueue[lineNum]
                    cmdLine.printText(thisLine)

                    lineNum += 1
                    canPrint = (lineNum < len(bootPrintQueue))

                # Generate overlays until all required frames are done:
                if genOverlays:
                    if (self.distortY < config.HEIGHT):
                        # Use scanlines as base:
                        thisFrame = self.scanLines.convert()

                        # Add animated distortion-line:
                        thisFrame.blit(self.distortLine, (0, self.distortY), None, pygame.BLEND_RGB_ADD)

                        # Tint screen:
                        thisFrame.fill(config.TINTCOLOUR, None, pygame.BLEND_RGB_MULT)

                        thisFrame = thisFrame.convert()
                        self.overlayFrames.append(thisFrame)

                        self.distortY += self.distortSpeed
                    else:
                        genOverlays = False

            self.animDelayFrames = len(self.overlayFrames)
            self.overlayFramesCount = (2 * self.animDelayFrames)
            self.frameNum = 0

            print("END GENERATE")

            # Initial map-downloads:
            cmdLine.printText(">MAPS.DOWNLOAD INIT")
            cmdLine.printText("\tDownloading Local map...")

            cmdLine.printText("\tDownloading World map...")
            if config.SOUND_ENABLED:
                pygame.mixer.Sound('sounds/start.wav').play()

            if config.SOUND_ENABLED:
                pygame.mixer.Sound('sounds/stop.wav').play()

            cmdLine.printText(">PIP-BOY.INIT")

            # Show Pip-Boy logo!
            if not config.QUICKLOAD:
                self.showBootLogo()

            if config.SOUND_ENABLED:
                pygame.mixer.Sound('sounds/start.wav').play()
            print("END INIT PROCESS")


    # Show bootup-logo, play sound:
    def showBootLogo(self):

        bootLogo = pygame.image.load('images/bootupLogo.png')
        self.focusInDraw(bootLogo)

        if config.SOUND_ENABLED:
            bootSound = pygame.mixer.Sound('sounds/falloutBootup.wav')
            bootSound.play()

        pygame.display.update()
        pygame.time.wait(4200)

    def focusInDraw(self, canvas):

        # Reset to first animation-frame:
        self.frameNum = 0

        def divRange(val):
            while val >= 1:
                yield val
                val //= 2

        # Do focusing-in effect by scaling canvas down/up:
        maxDiv = 2
        hicolCanvas = canvas.convert(24)
        for resDiv in divRange(maxDiv):

            blurImage = pygame.transform.smoothscale(hicolCanvas,
                                                     (self.canvasSize[0] // resDiv, self.canvasSize[1] // resDiv))
            blurImage = pygame.transform.smoothscale(blurImage,
                                                     (self.canvasSize[0] // resDiv, self.canvasSize[1] // resDiv))

            # Add faded sharp image:
            multVal = (255 // (1 * maxDiv))
            drawImage = canvas.convert()
            drawImage.fill((multVal, multVal, multVal), None, pygame.BLEND_RGB_MULT)

            # Add blurred image:
            drawImage.blit(blurImage, (multVal, multVal), None, pygame.BLEND_RGB_ADD)

            # Add background:
            if (self.background != None):
                drawImage.blit(self.background, (0, 0), None, pygame.BLEND_RGB_ADD)
                self.background = pygame.transform.smoothscale(self.background, self.canvasSize)
                self.background = self.background.convert_alpha()
                self.background.fill(config.TINTCOLOUR, None, pygame.BLEND_RGB_MULT)

            # Add scanlines:
            drawImage.blit(self.overlayFrames[0], (0, 0), None, pygame.BLEND_RGB_MULT)

            # Scale up and draw:
            drawImage = pygame.transform.scale(drawImage, self.screenSize)
            self.screen.blit(drawImage, (0, 0))
            pygame.display.update()

    def render(self):
        if self.last_render_time == 0:
            self.last_render_time = time.time()
            return
        else:
            interval = time.time() - self.last_render_time
            self.last_render_time = time.time()
        self.root_children.clear(self.screen, self.background)
        self.root_children.render(interval)
        self.root_children.draw(self.screen)
        for group in self.groups:
            group.render(interval)
            group.draw(self.screen)
        pygame.display.flip()
        return interval

    def update(self):
        self.root_children.update()
        for group in self.groups:
            group.update()

    def add(self, group):
        if group not in self.groups:
            self.groups.append(group)

    def remove(self, group):
        if group in self.groups:
            self.groups.remove(group)


class EntityGroup(pygame.sprite.LayeredDirty):
    def render(self, interval):
        for entity in self:
            entity.render(interval)

    def move(self, x, y):
        for child in self:
            child.rect.move(x, y)


class Entity(pygame.sprite.DirtySprite):
    def __init__(self, dimensions=(0, 0), layer=0, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.image = pygame.surface.Surface(dimensions)
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        self.groups = pygame.sprite.LayeredDirty()
        self.layer = layer
        self.dirty = 2
        self.blendmode = pygame.BLEND_RGBA_ADD

    def render(self, interval=0, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def __le__(self, other):
        if type(self) == type(other):
            return self.label <= other.label
        else:
            return 0

    def __str__(self):
        return "Entity"