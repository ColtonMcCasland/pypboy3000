from pypboy import BaseModule
from pypboy.modules.stats import status
from pypboy.modules.stats import special
from pypboy.modules.stats import skills
from pypboy.modules.stats import perks
from pypboy.modules.stats import general
import config

if config.GPIO_AVAILABLE:
    import RPi.GPIO as GPIO

class Module(BaseModule):

    label = "STATS"
    GPIO_LED_ID = 18

    def __init__(self, *args, **kwargs):

        self.submodules = [
            status.Module(self),
            special.Module(self),
            skills.Module(self),
            perks.Module(self),
            general.Module(self)
        ]
        super(Module, self).__init__(*args, **kwargs)
        
    def handle_resume(self):

        self.pypboy.header.headline = self.label
        self.pypboy.header.title = ["AP  75/99","HP  159/314", "LVL 31"]
        self.active.handle_action("resume")
