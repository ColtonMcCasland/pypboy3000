from pypboy import BaseModule
from pypboy.modules.items import weapons
from pypboy.modules.items import apparel
from pypboy.modules.items import aid
from pypboy.modules.items import misc
from pypboy.modules.items import ammo
import config

if config.GPIO_AVAILABLE:
    import RPi.GPIO as GPIO


class Module(BaseModule):

	label = "ITEMS"
	GPIO_LED_ID = 22
	
	def __init__(self, *args, **kwargs):
		if config.GPIO_AVAILABLE:
            print("led number ->  %d" % self.GPIO_LED_ID)
            GPIO.setup(self.GPIO_LED_ID, GPIO.OUT)
            GPIO.output(self.GPIO_LED_ID, True)
            GPIO.output(self.GPIO_LED_ID, 18)
            GPIO.output(self.GPIO_LED_ID, 25)
     
		self.submodules = [
			weapons.Module(self),
			apparel.Module(self),
			aid.Module(self),
			misc.Module(self),
			ammo.Module(self),

		]
		super(Module, self).__init__(*args, **kwargs)
