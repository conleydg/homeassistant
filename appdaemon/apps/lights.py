import appdaemon.plugins.hass.hassapi as hass

class Lights(hass.Hass):

    def initialize(self):
        sensor = self.args["sensor"]
        self.listen_state(self.turn_on_light, sensor, new = "on")
        self.listen_state(self.turn_off_in_ten_minutes, sensor, new = "off")

    def turn_on_light(self, entity, attribute, old, new, kwargs):
        light = self.args["light"]
        if self.get_state(light) == 'on':
            try:
                self.cancel_timer(self.turn_off_timer)
            except:
                pass
        self.turn_on(light)

    def turn_off_in_ten_minutes(self, entity, attribute, old, new, kwargs):
        self.turn_off_timer = self.run_in(self.light_off, 600)

    def light_off(self, kwargs):
        light = self.args["light"]
        self.turn_off(light)

class MediaTurnOffLights(hass.Hass):

    def initialize(self):
        sensor = self.args["sensor"]
        self.listen_state(self.light_off, sensor, new = "playing", old = "Off")

    def light_off(self, entity, attribute, old, new, kwargs):
        light = self.args["light"]
        self.turn_off(light)


class SleepingLights(hass.Hass):

    def initialize(self):
        living_room = self.args["living_room"]
        foyer = self.args["foyer"]

        self.listen_state(self.turn_off_light, living_room, new = "on", duration = 10)
        self.listen_state(self.turn_off_light, foyer, new = "on", duration = 10)

    def turn_off_light(self, entity, attribute, old, new, kwargs):
        print(entity)
        self.turn_off(entity)
