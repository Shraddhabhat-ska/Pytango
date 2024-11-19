# import tango
# from tango import DevState, AttrWriteType, Database, DeviceProxy
# from tango.server import Device, command, attribute, run, device_property
# from threading import Thread, Event
# import time

# # Device2: MotorDevice
# class MotorDevice(Device):
#     # Attributes for the motor device
#     speed = attribute(dtype=int, access=AttrWriteType.READ_WRITE)
#     position = attribute(dtype=int, access=AttrWriteType.READ_WRITE)
#     direction = attribute(dtype=str, access=AttrWriteType.READ_WRITE)
#     temperature = attribute(dtype=int, access=AttrWriteType.READ)
#     error_code = attribute(dtype=int, access=AttrWriteType.READ)

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self.set_status("MotorDevice initialized and waiting for commands.")
#         self._speed = 0
#         self._position = 0
#         self._direction = 'stopped'
#         self._temperature = 25
#         self._error_code = 0
#         self._counting = Event()
#         self._counting.clear()

#     def read_speed(self):
#         return self._speed

#     def write_speed(self, speed):
#         if speed < 0:
#             self.error_code = 1  # Example error code for invalid speed
#             raise ValueError("Speed cannot be negative.")
#         self._speed = speed
#         self._direction = 'running' if speed > 0 else 'stopped'
#         self.push_change_event("speed", self._speed)
#         self.info_stream(f"Motor speed set to {self._speed}. Direction: {self._direction}")

#     def read_position(self):
#         return self._position

#     def write_position(self, position):
#         self._position = position
#         self.push_change_event("position", self._position)
#         self.info_stream(f"Motor position set to {self._position}.")

#     def read_direction(self):
#         return self._direction

#     def write_direction(self, direction):
#         if direction in ['forward', 'backward', 'stopped']:
#             self._direction = direction
#             self.info_stream(f"Motor direction set to {self._direction}.")
#         else:
#             self.error_code = 2  # Example error code for invalid direction
#             raise ValueError("Invalid direction. Choose 'forward', 'backward', or 'stopped'.")

#     def read_temperature(self):
#         return self._temperature

#     def read_error_code(self):
#         return self._error_code

#     @command
#     def reset_motor(self):
#         """Command to reset the motor attributes."""
#         self._speed = 0
#         self._position = 0
#         self._direction = 'stopped'
#         self._error_code = 0
#         self.info_stream("Motor reset to default values.")


# # Device1: ControlSystem
# class ControlSystem(Device):
#     # Device property to specify MotorDevice's device name
#     motor_device_name = device_property(dtype=str)

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self.set_status("ControlSystem initialized and running.")

#         # Initialize device proxy for MotorDevice
#         if self.motor_device_name:
#             self._motor_proxy = DeviceProxy(self.motor_device_name)
#             self.info_stream("Connected to MotorDevice.")
#         else:
#             self.error_stream("MotorDevice name not set. Check motor_device_name property.")
#             self.set_status("MotorDevice name not set.")
#             self.set_state(DevState.FAULT)

#     @command
#     def set_motor_speed(self, speed):
#         """Command to set the speed of the motor."""
#         if self._motor_proxy:
#             self._motor_proxy.write_attribute("speed", speed)
#         else:
#             self.error_stream("MotorDevice proxy not initialized.")

#     @command
#     def set_motor_position(self, position):
#         """Command to set the position of the motor."""
#         if self._motor_proxy:
#             self._motor_proxy.write_attribute("position", position)
#         else:
#             self.error_stream("MotorDevice proxy not initialized.")

#     @command
#     def set_motor_direction(self, direction):
#         """Command to set the direction of the motor."""
#         if self._motor_proxy:
#             self._motor_proxy.write_attribute("direction", direction)
#         else:
#             self.error_stream("MotorDevice proxy not initialized.")

#     @command(dtype_out=int)
#     def get_motor_speed(self):
#         """Command to get the current speed of the motor."""
#         if self._motor_proxy:
#             return self._motor_proxy.read_attribute("speed").value
#         else:
#             self.error_stream("MotorDevice proxy not initialized.")
#             return -1

#     @command(dtype_out=int)
#     def get_motor_position(self):
#         """Command to get the current position of the motor."""
#         if self._motor_proxy:
#             return self._motor_proxy.read_attribute("position").value
#         else:
#             self.error_stream("MotorDevice proxy not initialized.")
#             return -1

#     @command(dtype_out=str)
#     def get_motor_direction(self):
#         """Command to get the current direction of the motor."""
#         if self._motor_proxy:
#             return self._motor_proxy.read_attribute("direction").value
#         else:
#             self.error_stream("MotorDevice proxy not initialized.")
#             return "unknown"

#     @command
#     def reset_motor(self):
#         """Command to reset the motor."""
#         if self._motor_proxy:
#             self._motor_proxy.command_inout("reset_motor")
#         else:
#             self.error_stream("MotorDevice proxy not initialized.")


# if __name__ == "__main__":
#     # Setup for MotorDevice
#     motor_dev_info = tango.DbDevInfo()
#     motor_dev_info.server = "MotorServer/01"
#     motor_dev_info._class = "MotorDevice"
#     motor_dev_info.name = "sys/motor/1"

#     # Setup for ControlSystem
#     control_dev_info = tango.DbDevInfo()
#     control_dev_info.server = "MotorServer/01"
#     control_dev_info._class = "ControlSystem"
#     control_dev_info.name = "sys/controller/1"

#     # Set device properties explicitly
#     control_dev_info.properties = {'motor_device_name': "sys/motor/1"}

#     # Initialize Tango database and register devices
#     db = Database()
#     try:
#         db.add_device(motor_dev_info)
#         db.add_device(control_dev_info)
#     except tango.DevFailed as e:
#         print(f"Failed to add devices to database: {e}")
#         exit(1)

#     # Run the device server with both classes
#     run([MotorDevice, ControlSystem])

import tango
from tango import DevState, AttrWriteType, Database, DeviceProxy
from tango.server import Device, command, attribute, run, device_property

# Device2: MotorDevice
class MotorDevice(Device):
    speed = attribute(dtype=int, access=AttrWriteType.READ_WRITE)
    position = attribute(dtype=int, access=AttrWriteType.READ_WRITE)
    direction = attribute(dtype=str, access=AttrWriteType.READ_WRITE)
    temperature = attribute(dtype=int, access=AttrWriteType.READ)
    error_code = attribute(dtype=int, access=AttrWriteType.READ)

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("MotorDevice initialized and waiting for commands.")
        self._speed = 0
        self._position = 0
        self._direction = 'stopped'
        self._temperature = 25
        self._error_code = 0

    def read_speed(self):
        self.info_stream(f"Reading speed: {self._speed}")
        return self._speed

    def write_speed(self, speed):
        if speed < 0:
            self._error_code = 1  # Example error code for invalid speed
            raise ValueError("Speed cannot be negative.")
        self._speed = speed
        self._direction = 'running' if speed > 0 else 'stopped'
        self.push_change_event("speed", self._speed)
        self.info_stream(f"Motor speed set to {self._speed}. Direction: {self._direction}")

    def read_position(self):
        self.info_stream(f"Reading position: {self._position}")
        return self._position

    def write_position(self, position):
        self._position = position
        self.push_change_event("position", self._position)
        self.info_stream(f"Motor position set to {self._position}.")

    def read_direction(self):
        self.info_stream(f"Reading direction: {self._direction}")
        return self._direction

    def write_direction(self, direction):
        if direction in ['forward', 'backward', 'stopped']:
            self._direction = direction
            self.push_change_event("direction", self._direction)
            self.info_stream(f"Motor direction set to {self._direction}.")
        else:
            self._error_code = 2  # Example error code for invalid direction
            raise ValueError("Invalid direction. Choose 'forward', 'backward', or 'stopped'.")

    def read_temperature(self):
        self.info_stream(f"Reading temperature: {self._temperature}")
        return self._temperature

    def read_error_code(self):
        self.info_stream(f"Reading error code: {self._error_code}")
        return self._error_code

    @command
    def reset_motor(self):
        """Command to reset the motor attributes."""
        self._speed = 0
        self._position = 0
        self._direction = 'stopped'
        self._error_code = 0
        self.info_stream("Motor reset to default values.")


# Device1: ControlSystem
class ControlSystem(Device):
    motor_device_name = "sys/motor/1"

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("ControlSystem initialized and running.")
        

        # Initialize device proxy for MotorDevice
        if self.motor_device_name:
            self._motor_proxy = DeviceProxy(self.motor_device_name)
            self.info_stream("Connected to MotorDevice.")
        else:
            self.error_stream("MotorDevice name not set. Check motor_device_name property.")
            self.set_status("MotorDevice name not set.")
            self.set_state(DevState.FAULT)

    @command(dtype_in=int)
    def set_motor_speed(self, speed):
        """Command to set the speed of the motor."""
        if self._motor_proxy:
            self._motor_proxy.write_attribute("speed", speed)
        else:
            self.error_stream("MotorDevice proxy not initialized.")

    @command(dtype_in=int)
    def set_motor_position(self, position):
        """Command to set the position of the motor."""
        if self._motor_proxy:
            self._motor_proxy.write_attribute("position", position)
        else:
            self.error_stream("MotorDevice proxy not initialized.")

    @command(dtype_in=str)
    def set_motor_direction(self, direction):
        """Command to set the direction of the motor."""
        if self._motor_proxy:
            self._motor_proxy.write_attribute("direction", direction)
        else:
            self.error_stream("MotorDevice proxy not initialized.")

    @command(dtype_out=int)
    def get_motor_speed(self):
        """Command to get the current speed of the motor."""
        if self._motor_proxy:
            return self._motor_proxy.read_attribute("speed").value
        else:
            self.error_stream("MotorDevice proxy not initialized.")
            return -1

    @command(dtype_out=int)
    def get_motor_position(self):
        """Command to get the current position of the motor."""
        if self._motor_proxy:
            return self._motor_proxy.read_attribute("position").value
        else:
            self.error_stream("MotorDevice proxy not initialized.")
            return -1

    @command(dtype_out=str)
    def get_motor_direction(self):
        """Command to get the current direction of the motor."""
        if self._motor_proxy:
            return self._motor_proxy.read_attribute("direction").value
        else:
            self.error_stream("MotorDevice proxy not initialized.")
            return "unknown"

    @command
    def reset_motor(self):
        """Command to reset the motor."""
        if self._motor_proxy:
            self._motor_proxy.command_inout("reset_motor")
        else:
            self.error_stream("MotorDevice proxy not initialized.")


if __name__ == "__main__":
    # Setup for MotorDevice
    motor_dev_info = tango.DbDevInfo()
    motor_dev_info.server = "MotorServer/01"
    motor_dev_info._class = "MotorDevice"
    motor_dev_info.name = "sys/motor/1"

    # Setup for ControlSystem
    control_dev_info = tango.DbDevInfo()
    control_dev_info.server = "MotorServer/01"
    control_dev_info._class = "ControlSystem"
    control_dev_info.name = "sys/controller/1"

    # Set device properties explicitly
    control_dev_info.properties = {'motor_device_name': "sys/motor/1"}

    # Initialize Tango database and register devices
    db = Database()
    try:
        db.add_device(motor_dev_info)
        db.add_device(control_dev_info)
    except tango.DevFailed as e:
        print(f"Failed to add devices to database: {e}")
        exit(1)

    # Run the device server with both classes
    run([MotorDevice, ControlSystem])
