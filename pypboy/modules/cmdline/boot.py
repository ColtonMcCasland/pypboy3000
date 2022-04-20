# RasPipBoy: A Pip-Boy 3000 implementation for Raspberry Pi
#	Neal D Corbett, 2013
# RobCo bootup printer

import math
import pygame
import time

import config


class CmdLineClass:
    def __init__(self, *args, **kwargs):
        self.parent = args[0]
        self.rootParent = self.parent.rootParent

        self.canvas = pygame.Surface(self.parent.canvasSize)

        # Use scanlines as base, with tint:
        self.baseOverlay = self.parent.scanLines.convert_alpha()
        self.baseOverlay.fill(config.TINTCOLOUR, None, pygame.BLEND_RGB_MULT)
        self.cursorRect = [0, 0, config.charWidth, config.charWidth]
        self.cursorYoffset = (config.charHeight - config.charWidth - 4)

        self.homeX = (config.charWidth * 2)
        self.homeY = (config.charHeight)
        self.printY = self.homeY

        self.maxCursorY = config.HEIGHT - (3 * config.charHeight)

    def printText(self, thisLine):
        if config.QUICKLOAD:
            print(thisLine)
        elif thisLine == "**cls":
            # Revert screen:
            time.sleep(2)
            self.canvas.fill((0, 0, 0))
            self.printY = self.homeY
        else:
            print(thisLine)

            printX = self.homeX
            charNum = 0
            firstChar = True
            self.cursorRect[1] = (self.printY + self.cursorYoffset)
            drawChars = ""
            lineEndNum = (len(thisLine) - 1)

            isInputLine = False

            for char in thisLine:
                if (char == "\t"):
                    drawChars += "  "
                else:
                    drawChars += char

                # Only actually redraw screen every so often:
                lastChar = (charNum == lineEndNum)
                if (math.fmod(charNum, 6) == 0) or (lastChar):
                    if config.SOUND_ENABLED:
                        config.SOUNDS["changemode"].play()

                    charImage = config.MONOFONT.render(drawChars, True, config.TINTCOLOUR, (0, 0, 0))
                    self.canvas.blit(charImage, (printX, self.printY))
                    drawChars = ""

                    printX += charImage.get_width()

                    # Put cursor on next line if at end of line:
                    if (lastChar):
                        self.cursorRect[0] = self.homeX

                        if (self.cursorRect[1] < self.maxCursorY):
                            self.cursorRect[1] += config.charHeight
                        else:
                            # Shift lines up if screen has been filled:
                            tempCanvas = self.canvas.convert()
                            self.canvas.fill((0, 0, 0))
                            self.canvas.blit(tempCanvas, (0, -config.charHeight))
                            pygame.draw.rect(self.canvas, (0, 0, 0), (0, 0, config.WIDTH, config.charHeight), 0)

                            self.printY -= config.charHeight
                    else:
                        self.cursorRect[0] = (printX + 1)

                    # Generate draw-image, including cursor:
                    drawImage = self.canvas.convert()
                    pygame.draw.rect(drawImage, config.TINTCOLOUR, self.cursorRect, 0)

                    drawImage.blit(self.parent.background, (0, 0), None, pygame.BLEND_RGB_ADD)
                    drawImage.blit(self.baseOverlay, (0, 0), None, pygame.BLEND_RGB_MULT)

                    # Scale up and display:
                    drawImage = pygame.transform.scale(drawImage, self.parent.screenSize)
                    self.parent.screen.blit(drawImage, (0, 0))

                    pygame.display.update()
                # self.clock.tick(config.FPS)
                # print self.parent.clock.get_fps()

                # Wait after drawing prompt-character:
                if firstChar:
                    firstChar = False
                    if (char == ">"):
                        isInputLine = True
                        time.sleep(1)

                charNum += 1

            self.printY += config.charHeight

            # Add wait for "processing" at end of "user-input" lines:
            if (isInputLine):
                time.sleep(0.5)
