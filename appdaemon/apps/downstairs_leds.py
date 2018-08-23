import appdaemon.plugins.hass.hassapi as hass
import datetime

class HelloWorld(hass.Hass):

    def initialize(self):
        motion = self.args["motion"]
        perimeter = self.args["perimeter"]
        office_motion = self.args["office_motion"]
        self.listen_state(self.sliding_motion, perimeter, new = "on")
        self.listen_state(self.sliding_motion, motion, new = "on")
        self.listen_state(self.turn_on_office_leds, office_motion, new = "motion detected")


    def sliding_motion(self, entity, attribute, old, new, kwargs):
        if self.get_state("light.downstairs_led") == 'on':
            try:
                self.cancel_timer(self.turn_off_timer)
            except:
                pass
        self.call_service("light/turn_on", entity_id = "light.downstairs_led", brightness=200, rgb_color=[169,199,255])
        self.turn_off_timer = self.run_in(self.light_off, 6000)

    def light_off(self, kwargs):
        self.turn_off("light.downstairs_led")

    def turn_on_office_leds(self, entity, attribute, old, new, kwargs):
        if hasattr(self, 'turn_off_office_led_timer'):
            print('cancled timer @ ', datetime.datetime.now())
            self.cancel_timer(self.turn_off_office_led_timer)
        sun = self.get_state('sun.sun')
        if sun == 'above_horizon':
            rgb_settings = [0,0,255]
        else:
            rgb_settings = [255,0,0]
        self.call_service("light/turn_on", entity_id = "light.dc4f22813a83_192168186", brightness=255, rgb_color=rgb_settings)
        print('turned on @ ', datetime.datetime.now())
        self.turn_off_office_led_timer = self.run_in(self.office_led_off, 300)
        print(self.turn_off_office_led_timer)

    def office_led_off(self, kwargs):
        print('turned off @ ', datetime.datetime.now())
        self.turn_off("light.dc4f22813a83_192168186")
