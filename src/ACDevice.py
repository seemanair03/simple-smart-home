import json
import paho.mqtt.client as mqtt


HOST = "localhost"
PORT = 1883
    
class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32  

    def __init__(self, device_id, room):
        
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
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

        self.client.subscribe("server/acknowlegement/AC/#")

        self.client.subscribe("server/command/getstatusbydevice/#")
        self.client.subscribe("server/command/getstatusbyroom/#")
        self.client.subscribe("server/command/getstatusbydtype/AC")
        self.client.subscribe("server/command/getstatusforAll")

        self.client.subscribe("server/command/setstatusbydevice/#")
        self.client.subscribe("server/command/setstatusbyroom/#")
        self.client.subscribe("server/command/setstatusbydtype/AC")
        self.client.subscribe("server/command/setstatusforAll")

        self.client.subscribe("server/command/settemperaturebydevice/#")
        self.client.subscribe("server/command/settemperaturebyroom/#")
        self.client.subscribe("server/command/settemperatureforAll")


    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):

        # Once the acknowlegement is received from server, AC device confirms the details.
        if msg.topic == "server/acknowlegement/AC/" + self._room_type + "/" + self._device_id:
            self._device_registration_flag = True
            print(f"AC-DEVICE Registered! - Registration status is available for '{self._device_id}': {self._device_registration_flag}")

        # Publish the AC device status for the device id
        elif msg.topic == "server/command/getstatusbydevice/"+ self._device_id:
            device_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
            payload = {"device_id": self._device_id, 'switch_state': self._get_switch_status(), 'temperature': self._get_temperature()}
            return self.client.publish(device_topic, payload=json.dumps(payload))

        # Publish the AC device status for the room
        elif msg.topic == "server/command/getstatusbyroom/" + self._room_type:
            device_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
            payload = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                       'temperature': self._get_temperature()}
            return self.client.publish(device_topic, payload=json.dumps(payload))

        # Publish All the AC device status
        elif msg.topic == "server/command/getstatusbydtype/AC":
            device_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
            payload = {"device_id": self._device_id, 'switch_state': self._get_switch_status(), 'temperature': self._get_temperature()}
            return self.client.publish(device_topic, payload=json.dumps(payload))

        # Publish All the device status
        elif msg.topic == "server/command/getstatusforAll":
            device_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
            payload = {"device_id": self._device_id, 'switch_state': self._get_switch_status(), 'temperature': self._get_temperature()}
            return self.client.publish(device_topic, payload=json.dumps(payload))

        # Set switch state for ac device id, publish device status and success/failure message
        elif msg.topic == "server/command/setstatusbydevice/" + self._device_id:
            device_switch_status = json.loads(msg.payload)
            device_resp_topic = "devices/message/AC/" + self._room_type + "/" + self._device_id
            if device_switch_status["switch_state"] in ["ON", "OFF"]:
                self._set_switch_status(device_switch_status["switch_state"])
                device_status_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'temperature': self._get_temperature()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Status Change FAILED. Invalid Status received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))

        # Set switch state for ac device in room, publish device status and success/failure message
        elif msg.topic == "server/command/setstatusbyroom/" + self._room_type:
            device_switch_status = json.loads(msg.payload)
            device_resp_topic = "devices/message/AC/" + self._room_type + "/" + self._device_id
            if device_switch_status["switch_state"] in ["ON", "OFF"]:
                self._set_switch_status(device_switch_status["switch_state"])
                device_status_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'temperature': self._get_temperature()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Status Change FAILED. Invalid Status received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))

        # Set switch state for all ac devices, publish device status and success/failure message
        elif msg.topic == "server/command/setstatusbydtype/AC" or msg.topic ==  msg.topic == "server/command/setstatusforAll":
            device_switch_status = json.loads(msg.payload)
            device_resp_topic = "devices/message/AC/" + self._room_type + "/" + self._device_id
            if device_switch_status["switch_state"] in ["ON", "OFF"]:
                self._set_switch_status(device_switch_status["switch_state"])
                device_status_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'temperature': self._get_temperature()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Status Change FAILED. Invalid Status received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))

        #Set switch state for all ac (home) devices, publish device status and success/failure message
        elif msg.topic == "server/command/setstatusforAll":
            device_switch_status = json.loads(msg.payload)
            device_resp_topic = "devices/message/AC/" + self._room_type + "/" + self._device_id
            if device_switch_status["switch_state"] in ["ON", "OFF"]:
                self._set_switch_status(device_switch_status["switch_state"])
                device_status_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'temperature': self._get_temperature()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Status Change FAILED. Invalid Status received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))


        # Set temperature of the ac device id, publish device status and success/failure message
        elif msg.topic == "server/command/settemperaturebydevice/" + self._device_id:
            device_control = json.loads(msg.payload)
            device_resp_topic = "devices/message/AC/" + self._room_type + "/" + self._device_id
            if device_control["temperature"] >= self._MIN_TEMP and device_control["temperature"] <= self._MAX_TEMP :
                if self._switch_status == "OFF":
                    self._set_switch_status("ON")
                self._set_temperature(device_control["temperature"])
                device_status_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'temperature': self._get_temperature()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id, "Message": "Temperature Change FAILED. Invalid Temperature value received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))



        # Set temperature of the ac devices in room, publish device status and success/failure message
        elif msg.topic == "server/command/settemperaturebyroom/" + self._room_type:
            device_control = json.loads(msg.payload)
            device_resp_topic = "devices/message/AC/" + self._room_type + "/" + self._device_id
            if device_control["temperature"] >= self._MIN_TEMP and device_control["temperature"] <= self._MAX_TEMP :
                if self._switch_status == "OFF":
                    self._set_switch_status("ON")
                self._set_temperature(device_control["temperature"])
                device_status_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'temperature': self._get_temperature()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id,
                            "Message": "Temperature Change FAILED. Invalid Temperature value received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))



        # Set temperature of all the ac devices, publish device status and success/failure message
        elif msg.topic == "server/command/settemperatureforAll":
            device_control = json.loads(msg.payload)
            device_resp_topic = "devices/message/AC/" + self._room_type + "/" + self._device_id
            if device_control["temperature"] >= self._MIN_TEMP and device_control["temperature"] <= self._MAX_TEMP :
                if self._switch_status == "OFF":
                    self._set_switch_status("ON")
                self._set_temperature(device_control["temperature"])
                device_status_topic = "devices/status/AC/" + self._room_type + "/" + self._device_id
                payload1 = {"device_id": self._device_id, 'switch_state': self._get_switch_status(),
                   'temperature': self._get_temperature()}
                self.client.publish(device_status_topic, payload=json.dumps(payload1))
                payload2 = {"device_id": self._device_id, "Message": "SUCCESS"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))
            else:
                payload2 = {"device_id": self._device_id,
                            "Message": "Temperature Change FAILED. Invalid Temperature value received"}
                self.client.publish(device_resp_topic, payload=json.dumps(payload2))



    # Getting the current switch status of devices
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        self._switch_status = switch_state

    # Getting the temperature for the devices
    def _get_temperature(self):
        return self._temperature

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        self._temperature = temperature

    def _on_disconnect(self, client, userdata, msg):
        self.client.disconnect()


    
