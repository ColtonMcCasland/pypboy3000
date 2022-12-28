from pypboy import BaseModule
from pypboy.modules.items import weapons
from pypboy.modules.items import apparel
from pypboy.modules.items import aid
from pypboy.modules.items import misc
from pypboy.modules.items import ammo


class Module(BaseModule):

	label = "ITEMS"
	GPIO_LED_ID = 27

	def __init__(self, *args, **kwargs):
		GPIO.setup(GPIO_LED_ID, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

		self.submodules = [
			weapons.Module(self),
			apparel.Module(self),
			aid.Module(self),
			misc.Module(self),
			ammo.Module(self)
		]
		super(Module, self).__init__(*args, **kwargs)
