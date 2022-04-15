from pypboy import BaseModule
from pypboy.modules.items import weapons
from pypboy.modules.items import apparel
from pypboy.modules.items import aid
from pypboy.modules.items import misc
from pypboy.modules.items import ammo


class Module(BaseModule):

	label = "ITEMS"
	GPIO_LED_ID = 21

	def __init__(self, *args, **kwargs):
		self.submodules = [
			weapons.Module(self),
			apparel.Module(self),
			aid.Module(self),
			misc.Module(self),
			ammo.Module(self)
		]
		super(Module, self).__init__(*args, **kwargs)
