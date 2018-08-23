import appdaemon.plugins.hass.hassapi as hass

class Sleeping(hass.Hass):

    def initialize(self):
        self.listen_state(self.activate_sleeping, self.args["sleeping_input"], new="on")
        self.listen_state(self.deactivate_sleeping, self.args["sleeping_input"], new="off")

    def activate_sleeping(self, entity, attribute, old, new, kwargs):
        self.call_service("input_boolean/turn_on", entity_id="input_boolean.camera_status")
        self.call_service("input_boolean/turn_on", entity_id="input_boolean.alarm_armed")
        self.turn_off(entity_id="group.lights")
        self.turn_on(entity_id="switch.master_outlet_fan")
        self.call_service("climate/set_operation_mode", entity_id="climate.downstairs_thermostat_cooling_1", operation_mode="Auto")
        self.call_service("climate/set_operation_mode", entity_id="climate.upstairs_thermostat_cooling_1", operation_mode="Auto")
        self.call_service("climate/set_temperature", entity_id="climate.downstairs_thermostat_cooling_1", temperature="75")
        self.call_service("climate/set_temperature", entity_id="climate.upstairs_thermostat_cooling_1", temperature="71")
        self.call_service("climate/set_temperature", entity_id="climate.downstairs_thermostat_heating_1", temperature="66")
        self.call_service("climate/set_temperature", entity_id="climate.upstairs_thermostat_heating_1", temperature="66")

    def deactivate_sleeping(self, entity, attribute, old, new, kwargs):
        self.call_service("input_boolean/turn_off", entity_id="input_boolean.camera_status")
        self.call_service("input_boolean/turn_off", entity_id="input_boolean.alarm_armed")
        self.call_service("climate/set_operation_mode", entity_id="climate.downstairs_thermostat_cooling_1", operation_mode="Auto")
        self.call_service("climate/set_operation_mode", entity_id="climate.upstairs_thermostat_cooling_1", operation_mode="Auto")
        self.call_service("climate/set_temperature", entity_id="climate.downstairs_thermostat_cooling_1", temperature="72")
        self.call_service("climate/set_temperature", entity_id="climate.upstairs_thermostat_cooling_1", temperature="73")
        self.call_service("climate/set_temperature", entity_id="climate.downstairs_thermostat_heating_1", temperature="66")
        self.call_service("climate/set_temperature", entity_id="climate.upstairs_thermostat_heating_1", temperature="66")
