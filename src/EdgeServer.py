import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883     
WAIT_TIME = 0.25  

class Edge_Server:
    
    def __init__(self, instance_name):
        
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []
        self.dev_status = []
        self.resp_message = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()



    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        self.client.subscribe("devices/registration")
        self.client.subscribe("devices/status/#")
        self.client.subscribe("devices/message/#")


        
    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):

        #Get the message payload
        d_status = json.loads(msg.payload)

        # Register device that has published in registration topic
        if msg.topic == "devices/registration":
            self._register_device(msg)

        # Collect and store the status of device from status topic
        elif msg.topic.startswith ("devices/status"):
            self.dev_status.append(d_status)

        # Collect and store the message of device from message topic
        elif msg.topic.startswith ("devices/message"):
            r_message = json.loads(msg.payload)
            self.resp_message.append(r_message["Message"])


    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list


    # Getting the status for the connected devices
    def get_status(self, device_id = None, room_type = None, device_type = None):

        self.dev_status = []

        # Sends request to device to publish device status
        if device_id:
            server_topic  = "server/command/getstatusbydevice/" + str(device_id)
            server_payload = "publish device status"
            self.client.publish(str(server_topic), server_payload)
            time.sleep(0.5)

        # Sends request to room to publish device status
        elif room_type:
            server_topic = "server/command/getstatusbyroom/" + str(room_type)
            server_payload = "publish room status"
            self.client.publish(str(server_topic), server_payload)
            time.sleep(0.5)

        # Sends request to device type to publish device status
        elif device_type:
            server_topic = "server/command/getstatusbydtype/" + str(device_type)
            server_payload = "publish device type status"
            self.client.publish(str(server_topic), server_payload)
            time.sleep(0.5)

        # Sends request to publish all device status
        else:
            server_topic = "server/command/getstatusforAll"
            server_payload = "publish all device status"
            self.client.publish(str(server_topic), server_payload)
            time.sleep(0.5)

        return self.dev_status, self.resp_message


    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self, device_id=None,  room_type=None, device_type=None, switch_state=None, intensity=None, temperature=None):

        self.dev_status = []
        self.resp_message = []

        # Creates the payload for set commands
        if  switch_state:
            payload1 = {"switch_state": switch_state}
        if intensity:
            payload2 = {"intensity": intensity}
        if temperature:
            payload3 = {"temperature": temperature}

        # Builds various topics for server to send device controls

        if device_id:
            if switch_state and intensity == None and temperature == None:
                server_state_t = "server/command/setstatusbydevice/" + str(device_id)
                self.client.publish(str(server_state_t), payload=json.dumps(payload1))
                time.sleep(0.5)

            elif (switch_state == None and intensity and temperature == None) or (
                    switch_state and intensity and temperature == None):
                server_control1_t = "server/command/setintensitybydevice/" + str(device_id)
                self.client.publish(str(server_control1_t), payload=json.dumps(payload2))
                time.sleep(0.5)

            elif (switch_state == None and intensity == None and temperature) or (
                    switch_state and intensity == None and temperature):
                server_control2_t = "server/command/settemperaturebydevice/" + str(device_id)
                self.client.publish(str(server_control2_t), payload=json.dumps(payload3))
                time.sleep(0.5)

            elif (switch_state == None and intensity and temperature) or (switch_state and intensity and temperature):
                server_control1_t = "server/command/setintensitybydevice/" + str(device_id)
                self.client.publish(str(server_control1_t), payload=json.dumps(payload2))
                server_control2_t = "server/command/settemperaturebydevice/" + str(device_id)
                self.client.publish(str(server_control2_t), payload=json.dumps(payload3))
                time.sleep(0.5)


        elif room_type:
            if switch_state and intensity == None and temperature == None:
                server_state_t = "server/command/setstatusbyroom/" + str(room_type)
                self.client.publish(str(server_state_t), payload=json.dumps(payload1))
                time.sleep(0.5)

            elif (switch_state == None and intensity and temperature == None) or (switch_state and intensity and temperature == None):
                server_control1_t = "server/command/setintensitybyroom/" + str(room_type)
                self.client.publish(str(server_control1_t), payload=json.dumps(payload2))
                time.sleep(0.5)

            elif (switch_state == None and intensity == None and temperature) or (switch_state and intensity == None and temperature):
                server_control2_t = "server/command/settemperaturebyroom/" + str(room_type)
                self.client.publish(str(server_control2_t), payload=json.dumps(payload3))
                time.sleep(0.5)

            elif (switch_state == None and intensity and temperature) or (switch_state and intensity and temperature) :
                server_control1_t = "server/command/setintensitybyroom/" + str(room_type)
                self.client.publish(str(server_control1_t), payload=json.dumps(payload2))
                server_control2_t = "server/command/settemperaturebyroom/" + str(room_type)
                self.client.publish(str(server_control2_t), payload=json.dumps(payload3))
                time.sleep(0.5)


        elif device_type:
            if switch_state and intensity == None and temperature == None:
                server_state_t = "server/command/setstatusbydtype/" + str(device_type)
                self.client.publish(str(server_state_t), payload=json.dumps(payload1))
                time.sleep(0.5)

            elif (switch_state == None and intensity and temperature == None) or (switch_state and intensity and temperature == None):
                server_control1_t = "server/command/setintensityforAll"
                self.client.publish(str(server_control1_t), payload=json.dumps(payload2))
                time.sleep(0.5)

            elif (switch_state == None and intensity == None and temperature) or (switch_state and intensity == None and temperature):
                server_control2_t = "server/command/settemperatureforAll"
                self.client.publish(str(server_control2_t), payload=json.dumps(payload3))
                time.sleep(0.5)

            elif (switch_state == None and intensity and temperature) or (switch_state and intensity and temperature):
                server_control1_t = "server/command/setintensityforAll"
                self.client.publish(str(server_control1_t), payload=json.dumps(payload2))
                server_control2_t = "server/command/settemperatureforAll"
                self.client.publish(str(server_control2_t), payload=json.dumps(payload3))
                time.sleep(0.5)


        elif device_type == None and device_id == None and room_type == None:
            if switch_state and intensity == None and temperature == None:
                server_state_t = "server/command/setstatusforAll"
                self.client.publish(str(server_state_t), payload=json.dumps(payload1))
                time.sleep(0.5)

            elif (switch_state == None and intensity and temperature == None) or (switch_state and intensity and temperature == None):
                server_control1_t = "server/command/setintensityforAll"
                self.client.publish(str(server_control1_t), payload=json.dumps(payload2))
                time.sleep(0.5)

            elif (switch_state == None and intensity == None and temperature) or (switch_state and intensity == None and temperature):
                server_control2_t = "server/command/settemperatureforAll"
                self.client.publish(str(server_control2_t), payload=json.dumps(payload3))
                time.sleep(0.5)

            elif (switch_state == None and intensity and temperature) or (switch_state and intensity and temperature) :
                server_control1_t = "server/command/setintensityforAll"
                self.client.publish(str(server_control1_t), payload=json.dumps(payload2))
                server_control2_t = "server/command/settemperatureforAll"
                self.client.publish(str(server_control2_t), payload=json.dumps(payload3))
                time.sleep(0.5)

        return self.dev_status, self.resp_message



    # Registers a Device and sends acknowledgement
    def _register_device(self, msg = None):
        device = json.loads(msg.payload)
        print("\n")
        print(f"Registration request is acknowledged for device '{device['device_id']}' in {device['room_type']}")
        self._registered_list.append(device)
        print(f"Request is processed for {device['device_id']}.")
        ackroomtype = device['room_type']
        ackdeviceId = device['device_id']
        ackdevicetype = device['device_type']
        device_topic = "server/acknowlegement/" + ackdevicetype +"/" + ackroomtype + "/"+ ackdeviceId
        self.client.publish(device_topic, msg.payload)









