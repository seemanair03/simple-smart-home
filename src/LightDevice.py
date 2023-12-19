import time
import json
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883

class Light_Device():

    # setting up the intensity choices for Smart Light Bulb  
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect  
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        payload = {"device_id": device_id, "room_type": room_type, "device_type": device_type}
        self.client.publish("devices/registration",  payload=json.dumps(payload))


    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):

        self.client.subscribe("server/acknowlegement/LIGHT/#")

        self.client.subscribe("server/command/getstatusbydevice/#")
        self.client.subscribe("server/command/getstatusbyroom/#")
        self.client.subscribe("server/command/getstatusbydtype/LIGHT")
        self.client.subscribe("server/command/getstatusforAll")

        self.client.subscribe("server/command/setstatusbydevice/#")
        self.client.subscribe("server/command/setstatusbyroom/#")
        self.client.subscribe("server/command/setstatusbydtype/LIGHT")
        self.client.subscribe("server/command/setstatusforAll")

        self.client.subscribe("server/command/setintensitybydevice/#")
        self.client.subscribe("server/command/setintensitybyroom/#")
        self.client.subscribe("server/command/setintensityforAll")


    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):

        # Once the acknowlegement is received from server, LIGHT device confirms the details.
        if msg.topic == "server/acknowlegement/LIGHT/" + self._room_type + "/" + self._device_id:
            self._device_registration_flag = True
            print(f"LIGHT-DEVICE Registered! - Registration status is available for '{self._device_id}': {self._device_registration_flag}")

        # Publish the LIGHT device status for the device id
        elif msg.topic == "server/command/getstatusbydevice/"+ self._device_id:
            device_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
            payload = {"device_id": self._device_id, 'switch_state': self._get_switch_status(), 'intensity': self._get_light_intensity()}
            return self.client.publish(device_topic, payload=json.dumps(payload))

        # Publish All the LIGHT device status
        elif msg.topic == "server/command/getstatusbydtype/LIGHT":
            device_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
            payload = {"device_id": self._device_id, 'switch_state': self._get_switch_status(), 'intensity': self._get_light_intensity()}
            return self.client.publish(device_topic, payload=json.dumps(payload))

        # Publish the LIGHT device status for the room
        elif msg.topic == "server/command/getstatusbyroom/" + self._room_type:
            device_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
            payload = {"device_id": self._device_id, 'switch_state': self._get_switch_status(), 'intensity': self._get_light_intensity()}
            return self.client.publish(device_topic, payload=json.dumps(payload))

        # Publish All the light device status
        elif msg.topic == "server/command/getstatusforAll":
            device_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
            payload = {"device_id": self._device_id, 'switch_state': self._get_switch_status(), 'intensity': self._get_light_intensity()}
            return self.client.publish(device_topic, payload=json.dumps(payload))

        # Set light switch state for light device id, publish device status and success/failure message
        elif msg.topic == "server/command/setstatusbydevice/" + self._device_id:
            device_switch_status = json.loads(msg.payload)
            device_resp_topic = "devices/message/LIGHT/" + self._room_type + "/" + self._device_id
            if device_switch_status["switch_state"] in ["ON", "OFF"]:
                self._set_switch_status(device_switch_status["switch_state"])
                device_status_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'intensity': self._get_light_intensity()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Status Change FAILED. Invalid Status received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))

        # Set switch state for light device in room, publish device status and success/failure message
        elif msg.topic == "server/command/setstatusbyroom/" + self._room_type:
            device_switch_status = json.loads(msg.payload)
            device_resp_topic = "devices/message/LIGHT/" + self._room_type + "/" + self._device_id
            if device_switch_status["switch_state"] in ["ON", "OFF"]:
                self._set_switch_status(device_switch_status["switch_state"])
                device_status_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'intensity': self._get_light_intensity()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Status Change FAILED. Invalid Status received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))

        # Set switch state for all light devices, publish device status and success/failure message
        elif msg.topic == "server/command/setstatusbydtype/LIGHT" or msg.topic == msg.topic == "server/command/setstatusforAll":
            device_switch_status = json.loads(msg.payload)
            device_resp_topic = "devices/message/LIGHT/" + self._room_type + "/" + self._device_id
            if device_switch_status["switch_state"] in ["ON", "OFF"]:
                self._set_switch_status(device_switch_status["switch_state"])
                device_status_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'intensity': self._get_light_intensity()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Status Change FAILED. Invalid Status received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))

        #Set switch state for all light (home) devices, publish device status and success/failure message
        elif msg.topic == "server/command/setstatusforAll":
            device_switch_status = json.loads(msg.payload)
            device_resp_topic = "devices/message/LIGHT/" + self._room_type + "/" + self._device_id
            if device_switch_status["switch_state"] in ["ON", "OFF"]:
                self._set_switch_status(device_switch_status["switch_state"])
                device_status_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'intensity': self._get_light_intensity()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Status Change FAILED. Invalid Status received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))


        # Set intensity of the light devices id, publish device status and success/failure message
        elif msg.topic == "server/command/setintensitybydevice/" + self._device_id:
            device_control = json.loads(msg.payload)
            device_resp_topic = "devices/message/LIGHT/" + self._room_type + "/" + self._device_id
            if device_control["intensity"] in self._INTENSITY:
                if self._switch_status == "OFF":
                    self._set_switch_status("ON")
                self._set_light_intensity(device_control["intensity"])
                device_status_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                               'intensity': self._get_light_intensity()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Intensity Change FAILED. Invalid Light Intensity level received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))

        # Set intensity of the light devices in room, publish device status and success/failure message
        elif msg.topic == "server/command/setintensitybyroom/" + self._room_type:
            device_control = json.loads(msg.payload)
            device_resp_topic = "devices/message/LIGHT/" + self._room_type + "/" + self._device_id
            if device_control["intensity"] in self._INTENSITY:
                if self._switch_status == "OFF":
                    self._set_switch_status("ON")
                self._set_light_intensity(device_control["intensity"])
                device_status_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'intensity': self._get_light_intensity()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Intensity Change FAILED. Invalid Light Intensity level received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))

        # Set intensity of all the light devices, publish device status and success/failure message
        elif msg.topic == "server/command/setintensityforAll":
            device_control = json.loads(msg.payload)
            device_resp_topic = "devices/message/LIGHT/" + self._room_type + "/" + self._device_id
            if device_control["intensity"] in self._INTENSITY:
                if self._switch_status == "OFF":
                    self._set_switch_status("ON")
                self._set_light_intensity(device_control["intensity"])
                device_topic = "devices/status/LIGHT/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'intensity': self._get_light_intensity()}
                self.client.publish(device_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Intensity Change FAILED. Invalid Light Intensity level received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))



    # Getting the current switch status of devices
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        self._switch_status = switch_state

    # Getting the light intensity for the devices
    def _get_light_intensity(self):
        return self._light_intensity

    # Setting the light intensity for devices
    def _set_light_intensity(self, light_intensity):
        self._light_intensity = light_intensity

    def _on_disconnect(self, client, userdata, msg):
        self.client.disconnect()






