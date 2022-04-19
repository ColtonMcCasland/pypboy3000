import pypboy
import config

from pypboy.modules.data import entities


class Module(pypboy.SubModule):
    label = "Radio"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self.stations = [
            entities.ClassicalRadio(),
            entities.DiamondCityRadio()
            # entities.EnclaveRadio(),
            # entities.InstituteRadio(),
            # entities.MinutemenRadio(),
            # entities.Vault101Radio(),
            # entities.ViolinRadio(),
            # entities.F3Radio()
        ]
        for station in self.stations:
            self.add(station)
        self.active_station = None
        config.radio = self

        stationLabels = []
        stationCallbacks = []
        for i, station in enumerate(self.stations):
            stationLabels.append(station.label)
            stationCallbacks.append(lambda i=i: self.select_station(i))

        self.menu = pypboy.ui.Menu(200, stationLabels, stationCallbacks, 0)
        self.menu.rect[0] = 4
        self.menu.rect[1] = 60
        self.add(self.menu)

        self.menu.select(1)

    def select_station(self, station):
        if hasattr(self, 'active_station') and self.active_station:
            self.active_station.stop()
        self.active_station = self.stations[station]
        self.active_station.play_random()

    def handle_event(self, event):
        if event.type == config.EVENTS['SONG_END']:
            if hasattr(self, 'active_station') and self.active_station:
                self.active_station.play_random()

    def handle_resume(self):
        self.parent.pypboy.header.headline = "DATA"
        self.parent.pypboy.header.title = ["Radio"]
        super(Module, self).handle_resume()

    def handle_tap(self):
        if self.menu.handle_tap() == False:
            if self.active_station.state == 1:
                self.active_station.pause()
            # else:
            #     self.active_station.play()
