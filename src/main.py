import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 0.25  

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user
edge_server_1 = Edge_Server(instance_name='edge_server_1')
time.sleep(WAIT_TIME)  

# Creating the light_device
#print("Intitate the device creation and registration process." )
#print("\nCreating the Light devices for their respective rooms.")

print("\n******************* Problem Statement 1.a *******************")
print("\n******************* REGSITRATION OF THE DEVICES THROUGH SERVER *******************")
print("\n******************* REGSITRATION OF LIGHT DEVICES INITIATED *******************")
light_device_1 = Light_Device("light_1", "Kitchen")
time.sleep(WAIT_TIME)
light_device_2 = Light_Device("light_2", "Garage")
time.sleep(WAIT_TIME)
light_device_3 = Light_Device("light_3", "BR1")
time.sleep(WAIT_TIME)
light_device_4 = Light_Device("light_4", "BR2")
time.sleep(WAIT_TIME)
light_device_5 = Light_Device("light_5", "Living")
time.sleep(WAIT_TIME)

# Creating the ac_device  
#print("\nCreating the AC devices for their respective rooms. ")
print("\n******************* REGSITRATION OF AC DEVICES INITIATED *******************")
ac_device_1 = AC_Device("ac_1", "BR1")
time.sleep(WAIT_TIME)
ac_device_2 = AC_Device("ac_2", "BR2")
time.sleep(WAIT_TIME)
ac_device_3 = AC_Device("ac_3", "Living")
time.sleep(WAIT_TIME)

print("\n******************* REGISTERED DEVICES ON THE SERVER *******************")
print("\nFetching the list of registered devices from EdgeServer")
devices_list = edge_server_1.get_registered_device_list()
dev_ids = [y['device_id'] for y in devices_list]
print("The Registered devices on Edge-Server:")
print (dev_ids)
time.sleep(WAIT_TIME)


print("\n******************* Problem Statement 2.a *******************")
print("\n******************* GETTING THE STATUS AND CONTROLLING THE DEVICES *******************")
count = 0

print("\n******************* GETTING THE STATUS BY DEVICE_ID *******************")
devices = ["light_1", "light_2", "light_3", "light_4", "light_5", "ac_1", "ac_2", "ac_3"]
for device in devices:
     count = count + 1
     print("\nStatus based on device_id: " + device)
     print("Command ID", count ,"request is intiated.")
     device_status = edge_server_1.get_status(device_id=device)
     device_s = device_status[0]
     print("Here is the current device-status for", device, ":", device_s[0])
     time.sleep(0.5)
     print("Command ID", count, "is executed.")


print("\n******************* GETTING THE STATUS BY DEVICE_TYPE *******************")
device_ty = ["LIGHT", "AC"]
for device_t in device_ty:
     count = count + 1
     print("\nStatus based on: " + device_t + " DEVICE_TYPE")
     print("Command ID", count ,"request is intiated.")
     device_status = edge_server_1.get_status(device_type=device_t)
     device_s = device_status[0]
     for dev in device_s:
          print(f"Here is the current device-status for {dev['device_id']}:", dev)
     time.sleep(0.5)
     print("Command ID", count, "is executed.")



print("\n******************* GETTING THE STATUS BY ROOM_TYPE *******************")
room_t = ["Kitchen", "Garage", "BR1", "BR2", "Living"]
for rm in room_t:
     count = count + 1
     print("\nStatus based on: " + rm + " ROOM_TYPE")
     print("Command ID", count ,"request is intiated.")
     device_status = edge_server_1.get_status(room_type=rm)
     device_s = device_status[0]

     for dev in device_s:
          print(f"Here is the current device-status for {dev['device_id']}:", dev)
     time.sleep(0.5)
     print("Command ID", count, "is executed.")



print("\n******************* GETTING THE STATUS BY ENTIRE_HOME *******************")
count = count +1
print("\nStatus based for entire home")
print("Command ID", count ,"request is intiated.")
device_status = edge_server_1.get_status()
device_s = device_status[0]
for dev in device_s:
     print(f"Here is the current device-status for", dev["device_id"],":", dev)
time.sleep(0.5)
print("Command ID", count, "is executed.")



print("\n******************* SETTING UP THE STATUS AND CONTROLLING BY THE DEVICE_ID *******************")
devices = ["light_1", "light_2", "light_3", "light_4", "light_5", "ac_1", "ac_2", "ac_3"]

print("\n******************* Problem Statement 2.b *******************")
print("\n******************* 2.b SIMULATE STATUS CHANGE FOR DEVICE_ID *******************")
# Sets the switch state of devices by device id
for device in devices:
    count = count +1
    print("\nControlling the devices based on ID:")
    print("Command ID", count ,"request is intiated.")
    edge_server_1.set(device_id = device, switch_state="ON")
    device_status = edge_server_1.get_status(device_id = device)
    if device_status[1] != []:
        device_message = device_status[1][0]
        if device_status[1][0] != "SUCCESS":
            print(device_message)
    else:
        device_message = device_status [1]
    print(f"Here is the current device-status for", device, ":", device_status[0][0])
    print("Command ID", count, "is executed.")
    time.sleep(0.5)


print("\n******************* Problem Statement 3.a and 3.b *******************")
print("\n******************* 3.a and 3.b SIMULATE CONTROL CHANGE FOR DEVICE_ID *******************")
# Sets the status and control of devices by device ids
devices = ["light_1", "ac_1", "ac_2"]
for device in devices:
    count = count +1
    print("\nControlling the devices based on ID:")
    print("Command ID", count ,"request is intiated.")
    # Problem statement 3.a - Sets light intensity based on device_id
    if device == "light_1":
        edge_server_1.set(device_id = device, intensity="HIGH")
    # Problem statement 3.b - Sets ac temperature based on device_id
    elif device == "ac_1":
        edge_server_1.set(device_id=device, temperature=29)
    elif device == "ac_2":
        edge_server_1.set(device_id=device, temperature=21)
    device_status = edge_server_1.get_status(device_id = device)
    if device_status[1] != []:
        device_message = device_status[1][0]
        if device_status[1][0] != "SUCCESS":
            print(device_message)
    else:
        device_message = device_status [1]
    print(f"Here is the current device-status for", device, ":", device_status[0][0])
    print("Command ID", count, "is executed.")
    time.sleep(0.5)


print("\n******************* SETTING UP THE STATUS AND CONTROLLING BY THE DEVICE_TYPE *******************")
device_types = ["LIGHT", "AC"]


print("\n******************* Problem Statement 2.b *******************")
print("\n******************* 2.b SIMULATE STATUS CHANGE FOR DEVICE_TYPE *******************")
# Sets the switch state of devices by device type
for dt in device_types:
    count = count +1
    print("\nControlling the devices based on DEVICE TYPE: ", dt)
    print("Command ID", count ,"request is intiated.")
    if dt == "LIGHT":
        edge_server_1.set(device_type = dt, switch_state="ON")
    elif dt == "AC":
        edge_server_1.set(device_type = dt, switch_state="OFF")
    device_status = edge_server_1.get_status(device_type = dt)
    if device_status[1] != []:
        device_message = device_status[1][0]
        if device_status[1][0] != "SUCCESS":
            print(device_message)
    else:
        device_message = device_status [1]
    for dev in device_status[0]:
        print(f"Here is the current device-status for {dev['device_id']}:", dev)
    print("Command ID", count, "is executed.")
    time.sleep(1)

print("\n******************* Problem Statement 3.a and 3.b *******************")
print("\n******************* 3.a and 3.b SIMULATE CONTROL CHANGE FOR DEVICE_TYPE *******************")
# Sets the controls of devices by device type
device_types = ["LIGHT", "AC"]
for dt in device_types:
    count = count +1
    print("\nControlling the devices based on DEVICE TYPE: ", dt)
    print("Command ID", count ,"request is intiated.")

    # Problem statement 3.a - Sets light intensity for all light devices in the home
    if dt == "LIGHT":
        edge_server_1.set(device_type = dt, intensity="HIGH")

    # Problem statement 3.b - Sets ac temperature for all ac devices in the home
    elif dt == "AC":
        edge_server_1.set(device_type = dt, temperature=21)
    device_status = edge_server_1.get_status(device_type = dt)
    if device_status[1] != []:
        device_message = device_status[1][0]
        if device_status[1][0] != "SUCCESS":
            print(device_message)
    else:
        device_message = device_status [1]
    for dev in device_status[0]:
        print(f"Here is the current device-status for {dev['device_id']}:", dev)
    print("Command ID", count, "is executed.")
    time.sleep(1)


print("\n******************* SETTING UP THE STATUS AND CONTROLLING BY ROOM *******************")
room_t = ["Kitchen", "Garage", "BR1", "BR2", "Living"]

print("\n******************* Problem Statement 2.b *******************")
print("\n******************* 2.b SIMULATE STATUS CHANGE FOR ROOM_TYPE *******************")
# Sets the status of devices in various room types
for rt in room_t:
    count = count +1
    print("\nControlling the devices based on ROOM TYPE:", rt)
    print("Command ID", count ,"request is intiated.")
    if rt == "Kitchen":
        # Simulates invalid switch_state response
        edge_server_1.set(room_type = rt, switch_state="UNKNOWN")
    elif rt == "BR1":
        edge_server_1.set(room_type=rt, switch_state="OFF")
    elif rt == "BR2":
        edge_server_1.set(room_type=rt, switch_state="OFF")
    elif rt == "Living":
        edge_server_1.set(room_type=rt, switch_state="OFF")
    elif rt == "Garage":
        edge_server_1.set(room_type=rt, switch_state="OFF")
    device_status = edge_server_1.get_status(room_type = rt)
    if device_status[1] != []:
        device_message = device_status[1][0]
        if device_status[1][0] != "SUCCESS":
            print(device_message)
    else:
        device_message = device_status [1]
    for dev in device_status[0]:
        print(f"Here is the current device-status for {dev['device_id']}:", dev)
    print("Command ID", count, "is executed.")
    time.sleep(1)


print("\n******************* Problem Statement 3.a and 3.b *******************")
print("\n******************* 3.a and 3.b SIMULATE CONTROL CHANGE FOR ROOM_TYPE *******************")
# Sets the controls of devices in various room types
for rt in room_t:
    count = count +1
    print("\nControlling the devices based on ROOM TYPE:", rt)
    print("Command ID", count ,"request is intiated.")

    # Problem statement 3.a - Sets light intensity based on room type
    if rt == "Kitchen":
        edge_server_1.set(room_type = rt, intensity="MEDIUM")

    # Problem statement 3.b - Sets ac temperature based on room type
    elif rt == "BR1":
        edge_server_1.set(room_type=rt, intensity="LOW", temperature=23)
    elif rt == "BR2":
        edge_server_1.set(room_type=rt, intensity="MEDIUM", temperature=23)
    elif rt == "Living":
        edge_server_1.set(room_type=rt, intensity="MEDIUM", temperature=19)
    elif rt == "Garage":
        edge_server_1.set(room_type=rt, intensity="MEDIUM")
    device_status = edge_server_1.get_status(room_type = rt)
    if device_status[1] != []:
        device_message = device_status[1][0]
        if device_status[1][0] != "SUCCESS":
            print(device_message)
    else:
        device_message = device_status [1]
    for dev in device_status[0]:
        print(f"Here is the current device-status for {dev['device_id']}:", dev)
    print("Command ID", count, "is executed.")
    time.sleep(1)


print("\n******************* SETTING UP THE STATUS AND CONTROLLING BY ENTIRE_HOME *******************")
print("\n******************* Problem Statement 2.b *******************")
print("\n******************* 2.b SIMULATE STATUS CHANGE FOR ENTIRE_HOME *******************")
count = count +1
print("\nControlling the devices based on entire homa:")
print("Command ID", count ,"request is intiated.")
device_status = edge_server_1.set(switch_state="OFF")
device_status = edge_server_1.get_status()
device_s = device_status[0]
if device_status[1] != []:
    device_message = device_status[1][0]
    if device_status[1][0] != "SUCCESS":
        print(device_message)
else:
    device_message = device_status[1]
for dev in device_status[0]:
    print(f"Here is the current device-status for {dev['device_id']}:", dev)
print("Command ID", count, "is executed.")




print("\n******************* SETTING UP THE STATUS AND CONTROLLING FOR INVALID REQUESTS *******************")

# Sets the status of devices in various room types, displays messages for invalid requests

room_t = ["Kitchen", "Garage", "BR1", "BR2", "Living"]
for rt in room_t:
    count = count +1
    print("\nControlling the devices based on ROOM TYPE:", rt)
    print("Command ID", count ,"request is intiated.")
    if rt == "Kitchen":
        edge_server_1.set(room_type = rt, intensity="VERY LOW")
    elif rt == "BR1":
        edge_server_1.set(room_type=rt, intensity="LOW", temperature=23)
    elif rt == "BR2":
        edge_server_1.set(room_type=rt, intensity="MEDIUM", temperature=15)
    elif rt == "Living":
        edge_server_1.set(room_type=rt, intensity="HIGH", temperature=19)
    elif rt == "Garage":
        edge_server_1.set(room_type=rt, intensity="MEDIUM")
    device_status = edge_server_1.get_status(room_type = rt)
    if device_status[1] != []:
        device_message = device_status[1][0]
        if device_status[1][0] != "SUCCESS":
            print(device_message)
    else:
        device_message = device_status [1]
    for dev in device_status[0]:
        print(f"Here is the current device-status for {dev['device_id']}:", dev)
    print("Command ID", count, "is executed.")
    time.sleep(1)


print("\n******************* CURRENT STATUS BEFORE CLOSING THE PROGRAM *******************")
# gets current status of devices by room types.
count = count+1
room_t = ["Kitchen", "Garage", "BR1", "BR2", "Living"]
print("\nStatus based on room:")
print("Command ID", count, "request is intiated.")
for rm in room_t:
     device_status = edge_server_1.get_status(room_type=rm)
     device_s = device_status[0]
     for dev in device_s:
          print(f"Here is the current device-status for {dev['device_id']}:", dev)
     time.sleep(0.5)
print("Command ID", count, "is executed.")



print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()
