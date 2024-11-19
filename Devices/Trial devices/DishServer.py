

# import tango
# from tango import DevState, AttrWriteType, EventType, DeviceProxy
# from tango.server import Device, attribute, command, device_property, run
# from threading import Event

# # Define the Servo Device
# class ServoDevice(Device):
#     AntennaPosition = attribute(dtype=float, access=AttrWriteType.READ)
#     TargetPosition = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
#     ErrorPosition = attribute(dtype=float, access=AttrWriteType.READ)

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self._antenna_position = 0.0
#         self._target_position = 0.0
#         self._error_position = 0.0
#         self.set_status("Servo device initialized.")

#     def read_AntennaPosition(self):
#         return self._antenna_position

#     def read_TargetPosition(self):
#         return self._target_position

#     def write_TargetPosition(self, value):
#         self._target_position = value
#         self.calculate_error_position()

#     def read_ErrorPosition(self):
#         return self._error_position

#     def calculate_error_position(self):
#         self._error_position = self._target_position - self._antenna_position

#     @command
#     def Init(self):
#         self.init_device()

#     @command(dtype_in=float)
#     def Mov(self, degrees):
#         self._antenna_position += degrees
#         self.calculate_error_position()

#         # Check if the target position is reached
#         if abs(self._error_position) < 0.1:  # Position tolerance
#             self.push_change_event("PositionAchieved", True)
#             self.set_status("Target position reached.")
#         else:
#             self.set_status(f"Moved antenna by {degrees} degrees. Current position: {self._antenna_position}")


# # Define the Dish Device
# class DishDevice(Device):
#     servo_device = "sys/servo/1"

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         try:
#             self.servo_proxy = DeviceProxy(self.servo_device)
#             # Verify device is accessible before subscribing to events
#             if self.servo_proxy.ping():
#                 self.servo_proxy.subscribe_event("PositionAchieved", EventType.CHANGE_EVENT, self.on_position_achieved)
#                 self.set_status("Dish device initialized and subscribed to events.")
#             else:
#                 self.set_status("Failed to subscribe to Servo events.")
#         except tango.DevFailed as e:
#             self.error_stream(f"Failed to connect to Servo device: {e}")
#             self.set_status("Failed to initialize Dish device.")

#     def on_position_achieved(self, event):
#         if event.err:
#             self.error_stream("Error in PositionAchieved event")
#         else:
#             self.info_stream("Position achieved event received.")
#             self.set_status("Target position reached by Servo device.")

#     @command(dtype_in=float)
#     def MoveToTarget(self, degrees):
#         try:
#             self.servo_proxy.command_inout("Mov", degrees)
#             self.set_status(f"Requested Servo to move by {degrees} degrees.")
#         except tango.DevFailed as e:
#             self.error_stream(f"Failed to execute Mov command on Servo device: {e}")
#             self.set_status("Failed to command Servo device.")


# # Main function to register devices and start server
# if __name__ == "__main__":
#     db = tango.Database()

#     # Register Servo Device
#     servo_dev_info = tango.DbDevInfo()
#     servo_dev_info.server = "DishServer/01"
#     servo_dev_info._class = "ServoDevice"
#     servo_dev_info.name = "sys/servo/1"
#     try:
#         db.add_device(servo_dev_info)
#     except tango.DevFailed as e:
#         print(f"Failed to add Servo device: {e}")

#     # Register Dish Device with servo_device property explicitly set
#     dish_dev_info = tango.DbDevInfo()
#     dish_dev_info.server = "DishServer/01"
#     dish_dev_info._class = "DishDevice"
#     dish_dev_info.name = "sys/dish/1"
#     dish_dev_info.properties = {"servo_device": "sys/servo/1"}  # Set servo_device property here
#     try:
#         db.add_device(dish_dev_info)
#     except tango.DevFailed as e:
#         print(f"Failed to add Dish device: {e}")

#     print("Devices registered successfully!")
#     run([ServoDevice, DishDevice])  # Run the server
# import tango
# from tango import DevState, AttrWriteType, EventType, DeviceProxy
# from tango.server import Device, attribute, command, device_property, run

# # Define the Servo Device
# class ServoDevice(Device):
#     AntennaPosition = attribute(dtype=float, access=AttrWriteType.READ)
#     TargetPosition = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
#     ErrorPosition = attribute(dtype=float, access=AttrWriteType.READ)

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self._antenna_position = 0.0
#         self._target_position = 0.0
#         self._error_position = 0.0
#         self.set_status("Servo device initialized.")

#     def read_AntennaPosition(self):
#         return self._antenna_position

#     def read_TargetPosition(self):
#         return self._target_position

#     def write_TargetPosition(self, value):
#         self._target_position = value
#         self.calculate_error_position()

#     def read_ErrorPosition(self):
#         return self._error_position

#     def calculate_error_position(self):
#         self._error_position = self._target_position - self._antenna_position

#     @command
#     def Init(self):
#         self.init_device()

#     @command(dtype_in=float)
#     def Mov(self, degrees):
#         self._antenna_position += degrees
#         self.calculate_error_position()

#         # Check if the target position is reached
#         if abs(self._error_position) < 0.1:  # Position tolerance
#             self.push_change_event("PositionAchieved", True)
#             self.set_status("Target position reached.")
#         else:
#             self.set_status(f"Moved antenna by {degrees} degrees. Current position: {self._antenna_position}")

# # Define the Dish Device
# class DishDevice(Device):
#     servo_device = "sys/servo/1"

    # def init_device(self):
    #     super().init_device()
    #     self.set_state(DevState.ON)
    #     try:
    #         self.servo_proxy = DeviceProxy("sys/servo/1")
    #         # Verify device is accessible before subscribing to events
    #         if self.servo_proxy.ping():
    #             self.servo_proxy.subscribe_event("PositionAchieved", EventType.CHANGE_EVENT, self.on_position_achieved)
    #             self.set_status("Dish device initialized and subscribed to events.")
    #         else:
    #             self.set_status("Failed to subscribe to Servo events.")
    #     except tango.DevFailed as e:
    #         self.error_stream(f"Failed to connect to Servo device: {e}")
    #         self.set_status("Failed to initialize Dish device.")
#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
        
#         try:
#             print(f"Initializing Dish device and connecting to Servo device: {self.servo_device}")
#             # Create the DeviceProxy for the Servo device
#             self.servo_proxy = DeviceProxy(self.servo_device)
            
#             # Ping the Servo device to check if it is reachable
#             if self.servo_proxy.ping():
#                 print(f"Successfully connected to Servo device: {self.servo_device}")
                
#                 # Subscribe to the PositionAchieved event (check if event exists)
#                 try:
#                     self.servo_proxy.subscribe_event("PositionAchieved", EventType.CHANGE_EVENT, self.on_position_achieved)
#                     self.set_status("Dish device initialized and subscribed to events.")
#                     print(f"Subscribed to 'PositionAchieved' event from {self.servo_device}.")
#                 except tango.DevFailed as e:
#                     self.error_stream(f"Failed to subscribe to event 'PositionAchieved': {e}")
#                     self.set_status(f"Failed to subscribe to event: {e}")
#             else:
#                 print(f"Failed to ping Servo device: {self.servo_device}")
#                 self.set_status("Failed to connect to Servo device.")

#         except tango.DevFailed as e:
#             # Detailed error message if DeviceProxy fails
#             print(f"Error initializing Dish device: {e}")
#             self.error_stream(f"Failed to connect to Servo device: {e}")
#             self.set_status("Failed to initialize Dish device.") 

#     def on_position_achieved(self, event):
#         if event.err:
#             self.error_stream("Error in PositionAchieved event")
#         else:
#             self.info_stream("Position achieved event received.")
#             self.set_status("Target position reached by Servo device.")

#     @command(dtype_in=float)
#     def MoveToTarget(self, degrees):
#         try:
#             self.servo_proxy.command_inout("Mov", degrees)
#             self.set_status(f"Requested Servo to move by {degrees} degrees.")
#         except tango.DevFailed as e:
#             self.error_stream(f"Failed to execute Mov command on Servo device: {e}")
#             self.set_status("Failed to command Servo device.")

#     # Commands for reading and writing attributes
#     @command
#     def ReadAntennaPosition(self):
#         try:
#             antenna_position = self.servo_proxy.read_attribute("AntennaPosition").value
#             self.set_status(f"Antenna Position: {antenna_position}")
#             return antenna_position
#         except tango.DevFailed as e:
#             self.error_stream(f"Failed to read AntennaPosition from Servo device: {e}")
#             self.set_status("Failed to read AntennaPosition.")

#     @command(dtype_in=float)
#     def WriteTargetPosition(self, value):
#         try:
#             self.servo_proxy.write_attribute("TargetPosition", value)
#             self.set_status(f"Target Position set to: {value}")
#         except tango.DevFailed as e:
#             self.error_stream(f"Failed to write TargetPosition to Servo device: {e}")
#             self.set_status("Failed to write TargetPosition.")

#     @command
#     def ReadTargetPosition(self):
#         try:
#             target_position = self.servo_proxy.read_attribute("TargetPosition").value
#             self.set_status(f"Target Position: {target_position}")
#             return target_position
#         except tango.DevFailed as e:
#             self.error_stream(f"Failed to read TargetPosition from Servo device: {e}")
#             self.set_status("Failed to read TargetPosition.")


# # Main function to register devices and start server
# if __name__ == "__main__":
#     db = tango.Database()

#     # Register Servo Device
#     servo_dev_info = tango.DbDevInfo()
#     servo_dev_info.server = "DishServer/01"
#     servo_dev_info._class = "ServoDevice"
#     servo_dev_info.name = "sys/servo/1"
#     try:
#         db.add_device(servo_dev_info)
#     except tango.DevFailed as e:
#         print(f"Failed to add Servo device: {e}")

#     # Register Dish Device with servo_device property explicitly set
#     dish_dev_info = tango.DbDevInfo()
#     dish_dev_info.server = "DishServer/01"
#     dish_dev_info._class = "DishDevice"
#     dish_dev_info.name = "sys/dish/1"
#     dish_dev_info.properties = {"servo_device": "sys/servo/1"}  # Set servo_device property here
#     try:
#         db.add_device(dish_dev_info)
#     except tango.DevFailed as e:
#         print(f"Failed to add Dish device: {e}")

#     print("Devices registered successfully!")
#     run([ServoDevice, DishDevice])  # Run the server

import tango
from tango import DevState, AttrWriteType, EventType, DeviceProxy
from tango.server import Device, attribute, command, device_property, run

# Define the Servo Device
class ServoDevice(Device):
    AntennaPosition = attribute(dtype=float, access=AttrWriteType.READ)
    TargetPosition = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
    ErrorPosition = attribute(dtype=float, access=AttrWriteType.READ)
    PositionAchieved = attribute(dtype=bool, access=AttrWriteType.READ)  # Added PositionAchieved attribute

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self._antenna_position = 0.0
        self._target_position = 0.0
        self._error_position = 0.0
        self._position_achieved = False  # Default value for position achieved
        self.set_status("Servo device initialized.")

    def read_AntennaPosition(self):
        return self._antenna_position

    def read_TargetPosition(self):
        return self._target_position

    def write_TargetPosition(self, value):
        self._target_position = value
        self.calculate_error_position()

    def read_ErrorPosition(self):
        return self._error_position

    def read_PositionAchieved(self):
        return self._position_achieved  # Returning the event status

    def calculate_error_position(self):
        self._error_position = self._target_position - self._antenna_position
        # Trigger the event when the position is achieved
        if abs(self._error_position) < 0.1:  # Position tolerance
            self._position_achieved = True
            self.push_change_event("PositionAchieved", self._position_achieved)  # Trigger event
        else:
            self._position_achieved = False

    @command
    def Init(self):
        self.init_device()

    @command(dtype_in=float)
    def Mov(self, degrees):
        self._antenna_position += degrees
        self.calculate_error_position()

        # Check if the target position is reached
        if self._position_achieved:
            self.set_status("Target position reached.")
        else:
            self.set_status(f"Moved antenna by {degrees} degrees. Current position: {self._antenna_position}")


# Define the Dish Device
class DishDevice(Device):
    servo_device = device_property(str, default_value="sys/servo/1")

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        try:
            self.servo_proxy = DeviceProxy(self.servo_device)
            # Verify device is accessible before subscribing to events
            if self.servo_proxy.ping():
                # Subscribe to PositionAchieved event correctly
                self.servo_proxy.subscribe_event("PositionAchieved", EventType.CHANGE_EVENT, self.on_position_achieved)
                self.set_status("Dish device initialized and subscribed to events.")
            else:
                self.set_status("Failed to subscribe to Servo events.")
        except tango.DevFailed as e:
            self.error_stream(f"Failed to connect to Servo device: {e}")
            self.set_status("Failed to initialize Dish device.")

    def on_position_achieved(self, event):
        if event.err:
            self.error_stream("Error in PositionAchieved event")
        else:
            self.info_stream("Position achieved event received.")
            self.set_status("Target position reached by Servo device.")

    @command(dtype_in=float)
    def MoveToTarget(self, degrees):
        try:
            self.servo_proxy.command_inout("Mov", degrees)
            self.set_status(f"Requested Servo to move by {degrees} degrees.")
        except tango.DevFailed as e:
            self.error_stream(f"Failed to execute Mov command on Servo device: {e}")
            self.set_status("Failed to command Servo device.")

    # Commands for reading and writing attributes
    @command
    def ReadAntennaPosition(self):
        try:
            antenna_position = self.servo_proxy.read_attribute("AntennaPosition").value
            self.set_status(f"Antenna Position: {antenna_position}")
            return antenna_position
        except tango.DevFailed as e:
            self.error_stream(f"Failed to read AntennaPosition from Servo device: {e}")
            self.set_status("Failed to read AntennaPosition.")

    @command(dtype_in=float)
    def WriteTargetPosition(self, value):
        try:
            self.servo_proxy.write_attribute("TargetPosition", value)
            self.set_status(f"Target Position set to: {value}")
        except tango.DevFailed as e:
            self.error_stream(f"Failed to write TargetPosition to Servo device: {e}")
            self.set_status("Failed to write TargetPosition.")

    @command
    def ReadTargetPosition(self):
        try:
            target_position = self.servo_proxy.read_attribute("TargetPosition").value
            self.set_status(f"Target Position: {target_position}")
            return target_position
        except tango.DevFailed as e:
            self.error_stream(f"Failed to read TargetPosition from Servo device: {e}")
            self.set_status("Failed to read TargetPosition.")


# Main function to register devices and start server
if __name__ == "__main__":
    db = tango.Database()

    # Register Servo Device
    servo_dev_info = tango.DbDevInfo()
    servo_dev_info.server = "DishServer/01"
    servo_dev_info._class = "ServoDevice"
    servo_dev_info.name = "sys/servo/1"
    try:
        db.add_device(servo_dev_info)
    except tango.DevFailed as e:
        print(f"Failed to add Servo device: {e}")

    # Register Dish Device with servo_device property explicitly set
    dish_dev_info = tango.DbDevInfo()
    dish_dev_info.server = "DishServer/01"
    dish_dev_info._class = "DishDevice"
    dish_dev_info.name = "sys/dish/1"
    dish_dev_info.properties = {"servo_device": "sys/servo/1"}  # Set servo_device property here
    try:
        db.add_device(dish_dev_info)
    except tango.DevFailed as e:
        print(f"Failed to add Dish device: {e}")

    print("Devices registered successfully!")
    run([ServoDevice, DishDevice])  # Run the server

