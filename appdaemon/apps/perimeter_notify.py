import appdaemon.plugins.hass.hassapi as hass

class notify_perimeter(hass.Hass):

    def initialize(self):

        self.listen_state(self.notify_us_open, self.args["sliding_door"], new="on", old="off")
        self.listen_state(self.notify_us_closed, self.args["sliding_door"], new="off", old="on")

        self.listen_state(self.notify_us_open, self.args["windows"], new="on", old="off")
        self.listen_state(self.notify_us_closed, self.args["windows"], new="off", old="on")

        self.listen_state(self.notify_us_open, self.args["garage_motion"], new="on", old="off")
        self.listen_state(self.notify_us_closed, self.args["garage_motion"], new="off", old="on")

        self.listen_state(self.notify_us_open, self.args["window_next_to_sliding_door"], new="on", old="off")
        self.listen_state(self.notify_us_closed, self.args["window_next_to_sliding_door"], new="off", old="on")

        self.listen_state(self.notify_us_open, self.args["front_door"], new="on", old="off")
        self.listen_state(self.notify_us_closed, self.args["front_door"], new="off", old="on")

        self.listen_state(self.notify_us_open, self.args["garage_doors"], new="on", old="off")
        self.listen_state(self.notify_us_closed, self.args["garage_doors"], new="off", old="on")

        self.listen_state(self.notify_us_open, self.args['door_alarm'], new="1", old="0")
        self.listen_state(self.notify_us_open, self.args['door_alarm'], new="2", old="0")
        self.listen_state(self.notify_us_open, self.args['door_alarm'], new="3", old="0")

        self.listen_state(self.fire_alarm, self.args['mud_room_fire'], new="Fire Detected")
        self.listen_state(self.fire_alarm, self.args['nursery_fire'], new="Fire Detected")
        self.listen_state(self.fire_alarm, self.args['master_fire'], new="Fire Detected")
        self.listen_state(self.fire_alarm, self.args['mud_room_fire'], new="Carbon Monoxide Detected")
        self.listen_state(self.fire_alarm, self.args['nursery_fire'], new="Carbon Monoxide Detected")
        self.listen_state(self.fire_alarm, self.args['master_fire'], new="Carbon Monoxide Detected")
        self.listen_state(self.fire_alarm, self.args['main_fire'], new="on")

        self.listen_state(self.notify_us_open, self.args['glassbreak'], new="on")

        self.listen_state(self.cancel_trigger_timer, self.args['input_alarm'], new="off")


    def fire_alarm(self, entity, attribute, old, new, kwargs):
        friendly_name = self.friendly_name(entity)
        print(friendly_name, kwargs)
        self.call_service('notify/us', message=(friendly_name + ' reporting ' + new  + '.  Alarm will activate in less than 25 seconds.  Fire extinguishers are in the garage, under the kitchen sink, and under the upstair bathroom sinks.'))
        tts_message = friendly_name + ' reporting ' + new  + '.  Alarm will activate in 25 seconds.  Fire extinguishers are in the garage, under the kitchen sink, and under the upstair bathroom sinks.'
        self.call_service("tts/google_say", entity_id="media_player.living_room", message=tts_message + tts_message + tts_message)
        self.call_service("tts/google_say", entity_id="media_player.otter_mating_retreat", message=tts_message + tts_message + tts_message)
        self.set_state("switch.davids_lamp", state = "on")
        self.set_state("switch.emilys_lamp", state = "on")
        self.set_state("group.lights", state = "on")
        self.call_service("light/turn_on", entity_id = "light.6001948a4fa2_192168148", brightness=255, rgb_color= [255,255,255])
        self.call_service("light/turn_on", entity_id = "light.downstairs_led", brightness=255, rgb_color= [255,255,255])
        self.call_service("light/turn_on", entity_id = "light.level", brightness=255)
        self.call_service("lock/unlock", entity_id = "goup.all_locks")
        self.call_service("climate/set_operation_mode", entity_id = "group.climate", operation_mode="off")
        self.trigger_timer = self.run_in(self.trigger_alarm, 30)
        self.alarm_turn_off = self.run_in(self.turn_alarm_off, 300)


    def notify_us_open(self, entity, attribute, old, new, kwargs):
        friendly_name = self.friendly_name(entity)
        print(friendly_name, kwargs)
        alarm_armed = True if self.get_state('alarm_control_panel.partition_1') == 'armed_home' or self.get_state('alarm_control_panel.partition_1') == 'armed_away' else False
        is_always_trigger_for_alarm = friendly_name in ["Glassbreak", "Front Door Alarm"]
        if alarm_armed or is_always_trigger_for_alarm:
            self.call_service('notify/ios_davids_iphone', message=(friendly_name + ' Opened.  Alarm will trigger in 15 seconds'))
            tts_message = "Alarm Triggered by " + friendly_name + ".  You have less than ten seconds before the siren activates and the police are notified."
            self.call_service("tts/google_say", entity_id="media_player.living_room", message=tts_message + tts_message + tts_message)
            self.call_service("tts/google_say", entity_id="media_player.otter_mating_retreat", message=tts_message + tts_message + tts_message)
            self.set_state("switch.davids_lamp", state = "on")
            self.set_state("switch.emilys_lamp", state = "on")
            self.call_service("light/turn_on", entity_id = "Flight.6001948a4fa2_192168148", brightness=200, rgb_color= [255,0,0])
            self.call_service("light/turn_on", entity_id = "light.downstairs_led", effect = "red_strobe")
            self.alarm_turn_off = self.run_in(self.turn_alarm_off, 300)
            self.trigger_timer = self.run_in(self.trigger_alarm, 20)

    def trigger_alarm(self, kwargs):
        print(kwargs)
        self.call_service('notify/ios_davids_iphone', message=(kwargs['friendly_name'] + ' Triggered Alarm'))
        self.call_service("alarm_control_panel/alarm_trigger", entity_id = "alarm_control_panel.partition_1", code = "0514")


    def turn_alarm_off(self, kwargs):
        print(kwargs)
        self.set_state('input_boolean.alarm_armed', state='off')
        self.call_service('notify/ios_davids_iphone', message=('Alarm turned off after 5 minutes'))

    def cancel_trigger_timer(self, entity, attribute, old, new, kwargs):
        print('cancelling trigger timer')
        self.call_service("light/turn_off", entity_id = "light.6001948a4fa2_192168148")
        self.call_service("light/turn_on", entity_id = "light.downstairs_led", brightness=200, rgb_color = [168,198,255])
        if self.trigger_timer:
            self.cancel_timer(self.trigger_timer)
            self.cancel_timer(self.alarm_turn_off)


    def notify_us_closed(self, entity, attribute, old, new, kwargs):
        friendly_name = self.friendly_name(entity)
        print('sending closed notification')
        # self.call_service('notify/ios_davids_iphone', message=(friendly_name + ' Closed'))
