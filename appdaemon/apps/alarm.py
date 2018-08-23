import appdaemon.plugins.hass.hassapi as hass

class Status(hass.Hass):

    def initialize(self):
        alarm_input = self.args["alarm_input"]
        alarm_partition = self.args["alarm_partition"]
        door_access = self.args["door_access"]
        self.listen_state(self.alarm_arm, alarm_input, new="on")
        self.listen_state(self.alarm_disarm, alarm_input, new="off")
        self.listen_state(self.alarm_input_off, alarm_partition, new="disarmed")
        self.listen_state(self.alarm_input_on, alarm_partition, new="armed_home")
        self.listen_state(self.alarm_input_on, alarm_partition, new="armed_away")
        self.listen_state(self.alarm_input_off, door_access, new="6")

    def alarm_arm(self, entity, attribute, old, new, kwargs):
        self.turn_on('script.homearm')

    def alarm_disarm(self, entity, attribute, old, new, kwargs):
        self.turn_on('script.disarm')

    def alarm_input_on(self, entity, attribute, old, new, kwargs):
        input = self.set_state('input_boolean.alarm_armed', state = 'on')

    def alarm_input_off(self, entity, attribute, old, new, kwargs):
        input = self.set_state('input_boolean.alarm_armed', state = 'off')
