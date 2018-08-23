import appdaemon.plugins.hass.hassapi as hass

class Doorbell(hass.Hass):

    def initialize(self):
        sensor = self.args["sensor"]
        self.listen_state(self.notify_us, sensor, new = "off")

    def notify_us(self, entity, attribute, old, new, kwargs):
        friendly_name = self.friendly_name(entity)
        self.call_service("camera/snapshot", entity_id= "camera.front_door", filename= "/config/snapshots/doorbell.jpg")
        self.call_service('notify/us', message=('Someone Rang the Doorbell'), data={'push': {'category': 'camera'}, 'entity_id': 'camera.local_file'})
        self.dash_navigate("/doorbell", timeout=90)
