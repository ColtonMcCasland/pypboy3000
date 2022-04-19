# encoding=utf-8

import game
import os
import pygame
import traceback
import numpy 
from numpy.fft import fft 
from math import log10 
import math
from random import randint
import copy
import game.globals as globals
import mutagen.oggvorbis
import config


class Radio(game.Entity):
    def __init__(self):
        super(Radio, self).__init__((globals.WIDTH, globals.HEIGHT))
        # set up the mixer
        
        try: 
            pygame.mixer.quit()
        except Exception as e: 
            print(e)
            pass
        
        freq = 44100	 # audio CD quality
        bitsize = -16	# unsigned 16 bit
        channels = 2	 # 1 is mono, 2 is stereo
        buffer = 2048	# number of samples (experiment to get right sound)
        if config.SOUND_ENABLED:
            pygame.mixer.init(freq, bitsize, channels, buffer)
        self.osc = Oscilloscope() 
        self.osc.open(self)
        self.paused = True
        self.loaded = False
        self.spectrum = None 
        self.filename = ""
    
    def play_rnd(self):
        if config.SOUND_ENABLED:
            files = load_files()
            file = files[randint(0,len(files)-1)]
            self.filename = file
            pygame.mixer.music.load(file)
            self.spectrum = LogSpectrum(file,force_mono=True) 
            # pygame.mixer.music.play()
            self.loaded = True
            self.paused = False
        
    def play(self):
        if self.loaded and config.SOUND_ENABLED:
            self.paused = False
            pygame.mixer.music.unpause()
        else:
            self.play_rnd()
        
    def stop(self):
        self.paused = True
        pygame.mixer.music.pause()

    def update(self, *args, **kwargs):
        super(Radio, self).update(*args, **kwargs)

    def render(self, *args, **kwargs):
        if not self.paused :
            f,p = None,[0 for i in range(21)]
            start = pygame.mixer.music.get_pos() / 1000.0
            try:
                f,p = self.spectrum.get_mono(start-0.001, start+0.001)
            except Exception as e:
                print(e)
                pass
            self.osc.update(start*50,f,p)	
        if self.osc:
            self.blit(self.osc.screen, (550, 150))
            
        metadata = mutagen.File(filename, easy = True)
            
        selectFont = pygame.font.Font('monofonto.ttf', 24)
        basicFont = pygame.font.Font('monofonto.ttf', 22)
        
        text = selectFont.render(game.Entity.name, True, (105, 251, 187), (0, 0, 0))
        
        #text = selectFont.render(" -   Random Play Radio ", True, (105, 251, 187), (0, 0, 0))
        
        self.blit(text, (75, 75))
        text = basicFont.render("  'r' selects a random song ", True, (105, 251, 187), (0, 0, 0))
        self.blit(text, (75, 100))
        text = basicFont.render("  'p' to play   's' to stop ", True, (105, 251, 187), (0, 0, 0))
        self.blit(text, (75, 120))
        
        if self.filename:
            text = selectFont.render(" %s " % metadata["ARTIST"] + ' - ' + metadata["TITLE"], True, (105, 251, 187), (0, 0, 0))
            
            #text = selectFont.render(u" %s " % self.filename[self.filename.rfind(os.sep)+1:], True, (105, 251, 187), (0, 0, 0))
            self.blit(text, (75, 200))
            
        super(Radio, self).update(*args, **kwargs)

class Oscilloscope:
    
    def __init__(self): 
        # Constants
        self.WIDTH, self.HEIGHT = 210, 200
        self.TRACE, self.AFTER, self.GREY = (80, 255, 100),(20, 155, 40),(20, 110, 30)
        self.embedded = False
    
    def open(self, screen=None):
        # Open window
        pygame.init()
        if screen:
            '''Embedded'''
            self.screen = pygame.Surface((self.WIDTH, self.HEIGHT), 0)
            self.embedded = True
        else:
            '''Own Display'''
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0)
                
        # Create a blank chart with vertical ticks, etc
        self.blank = numpy.zeros((self.WIDTH, self.HEIGHT, 3))
        # Draw x-axis
        self.xaxis = self.HEIGHT/2
        self.blank[::, self.xaxis] = self.GREY
        self.blank[::, self.HEIGHT - 2] = self.TRACE
        self.blank[::, self.HEIGHT - 1] = self.TRACE
        self.blank[::50, self.HEIGHT - 4] = self.TRACE
        self.blank[::50, self.HEIGHT - 3] = self.TRACE
        self.blank[self.WIDTH - 2, ::] = self.TRACE
        self.blank[self.WIDTH - 1, ::] = self.TRACE
        self.blank[self.WIDTH - 3, ::40] = self.TRACE
        self.blank[self.WIDTH - 4, ::40] = self.TRACE
        
        # Draw vertical ticks
        vticks = [-80, -40, +40, +80]
        for vtick in vticks: self.blank[::5, self.xaxis + vtick] = self.GREY # Horizontals
        for vtick in vticks: self.blank[::50, ::5] = self.GREY			   # Verticals
    
        # Draw the 'blank' screen.
        pygame.surfarray.blit_array(self.screen, self.blank)	  # Blit the screen buffer
        pygame.display.flip()									 # Flip the double buffer
        
            
    def update(self,time,frequency,power):
        try:
            pixels = copy.copy(self.blank)
            offset = 1
            for x in range(self.WIDTH):
                offset = offset - 1
                if offset < -1:
                    offset = offset + 1.1		 
                try:
                    pow = power[int(x/10)]
                    log = math.log10( pow )
                    offset = ((pow / math.pow(10, math.floor(log))) + log)*1.8
                except Exception as e:
                    print(e)
                    pass
                try: 
                    y = float(self.xaxis) - (math.sin((float(x)+float(time))/5.0)*2.0*offset) 
                    pixels[x][y] = self.TRACE
                    pixels[x][y-1] = self.AFTER
                    pixels[x][y+1] = self.AFTER
                    if abs(y) > 120:
                        pixels[x][y-2] = self.AFTER
                        pixels[x][y+2] = self.AFTER
                except Exception as e: 
                    print(e)
                    pass
            pygame.surfarray.blit_array(self.screen, pixels)	 # Blit the screen buffer
            if not self.embedded:
                pygame.display.flip()  
        except Exception:
            _, err, _ = sys.exc_info()
            print(traceback.format_exc())

def play_pygame(file):
    if config.SOUND_ENABLED:
        clock = pygame.time.Clock()
        # set up the mixer
        freq = 44100	 # audio CD quality
        bitsize = -16	# unsigned 16 bit
        channels = 2	 # 1 is mono, 2 is stereo
        buffer = 2048	# number of samples (experiment to get right sound)
        if config.SOUND_ENABLED:
            pygame.mixer.init(freq, bitsize, channels, buffer)
        
        while not pygame.mixer.get_init():
            clock.tick(50)
        
        pygame.mixer.music.load(file)
        s = LogSpectrum(file,force_mono=True) 
        osc = Oscilloscope() 
        osc.open()
        
        f = None
        p = None
        running = True
        paused = True
        # pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy() and running : 
            if not paused:
                start = pygame.mixer.music.get_pos() / 1000.0
                try:
                    f,p = s.get_mono(start-0.001, start+0.001)
                except Exception as e:
                    print(e)
                    pass
                osc.update(start*50,f,p)			 
            pygame.time.wait(50)
            
            for event in pygame.event.get():
                if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
                    if (event.PIOkey == pygame.K_UP):
                        pygame.mixer.music.pause()
                        paused = True
                    elif (event.key == pygame.K_DOWN):
                        pygame.mixer.music.unpause()
                        paused = False
                elif event.type == pygame.QUIT:
                    running = False
        pygame.mixer.quit()
            
if __name__ == "__main__":
    try:
        files = load_files()
        if files and config.SOUND_ENABLED:
            play_pygame(files[randint(0,len(files)-1)])
    except Exception:
        _, err, _ = sys.exc_info()
        print(traceback.format_exc())
