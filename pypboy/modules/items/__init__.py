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
	GPIO_LED_ID = 18


	if config.GPIO_AVAILABLE:
		GPIO.setup(GPIO_LED_ID, GPIO.OUT)
		GPIO.output(GPIO_LED_ID, True),
		GPIO.output(22, False),
		GPIO.output(25, False),

	def __init__(self, *args, **kwargs):
		self.submodules = [
			weapons.Module(self),
			apparel.Module(self),
			aid.Module(self),
			misc.Module(self),
			ammo.Module(self),

		]
		super(Module, self).__init__(*args, **kwargs)
