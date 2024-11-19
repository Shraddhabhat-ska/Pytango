import tango
from tango import DevState, AttrWriteType, Database, DeviceProxy
from tango.server import Device, attribute, run, device_property, command
import time

# Level 4: Servo Device
class ServoDevice(Device):
    AntennaPosition = attribute(dtype=float, access=AttrWriteType.READ)
    TargetPosition = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
    ErrorPosition = attribute(dtype=float, access=AttrWriteType.READ)
    PositionAchieved = attribute(dtype=bool, access=AttrWriteType.READ)

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self._antenna_position = 0.0
        self._target_position = 0.0
        self._error_position = 0.0
        self._position_achieved = False
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
        return self._position_achieved

    def calculate_error_position(self):
        self._error_position = self._target_position - self._antenna_position
        self._position_achieved = abs(self._error_position) < 0.1

    @command(dtype_in=float)
    def Mov(self, degrees):
        self._antenna_position += degrees
        self.calculate_error_position()
        if self._position_achieved:
            self.set_status("Target position reached.")
        else:
            self.set_status(f"Moved antenna by {degrees} degrees. Current position: {self._antenna_position}")

# Level 3: Dish Device
class DishDevice(Device):
    servo_device = device_property(str, default_value="sys/servo/default")

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        try:
            self.servo_proxy = DeviceProxy(self.servo_device)
            # Checking if the device is reachable
            self.servo_proxy.read_attribute("AntennaPosition")
            self.set_status("Dish device initialized and connected to Servo.")
        except tango.DevFailed as e:
            self.error_stream(f"Error connecting to Servo device: {e}")
            self.set_status("Dish device initialization failed.")

    @command(dtype_in=float)
    def MoveToTarget(self, degrees):
        try:
            self.servo_proxy.command_inout("Mov", degrees)
            self.set_status(f"Requested Servo to move by {degrees} degrees.")
        except tango.DevFailed as e:
            self.error_stream(f"Failed to execute Mov command on Servo device: {e}")
            self.set_status("Failed to command Servo device.")

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

# Level 2: SubArray Device
class SubArrayDevice(Device):
    dish1_device = device_property(str, default_value="sys/dish/1")
    dish2_device = device_property(str, default_value="sys/dish/2")

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        try:
            self.dish1_proxy = DeviceProxy(self.dish1_device)
            self.dish2_proxy = DeviceProxy(self.dish2_device)
            self.set_status("SubArray device initialized and connected to dishes.")
        except tango.DevFailed as e:
            self.error_stream(f"Error connecting to Dish devices: {e}")
            self.set_status("SubArray device initialization failed.")

    @command
    def MoveDishes(self, degrees):
        try:
            self.dish1_proxy.command_inout("MoveToTarget", degrees)
            self.dish2_proxy.command_inout("MoveToTarget", degrees)
            self.set_status(f"Moved both dishes by {degrees} degrees.")
        except tango.DevFailed as e:
            self.error_stream(f"Failed to command dishes to move: {e}")
            self.set_status("Failed to move dishes.")

# Level 1: CentralNode Device
class CentralNodeDevice(Device):
    subarray1_device = device_property(str, default_value="sys/subarray/1")
    subarray2_device = device_property(str, default_value="sys/subarray/2")

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        try:
            self.subarray1_proxy = DeviceProxy(self.subarray1_device)
            self.subarray2_proxy = DeviceProxy(self.subarray2_device)
            self.set_status("CentralNode device initialized and connected to SubArrays.")
        except tango.DevFailed as e:
            self.error_stream(f"Error connecting to SubArray devices: {e}")
            self.set_status("CentralNode device initialization failed.")

    @command
    def AssignDishes(self):
        try:
            self.subarray1_proxy.command_inout("MoveDishes", 10)
            self.subarray2_proxy.command_inout("MoveDishes", 20)
            self.set_status("Dishes assigned to subarrays.")
        except tango.DevFailed as e:
            self.error_stream(f"Failed to assign dishes: {e}")
            self.set_status("Failed to assign dishes.")

# Main function to register devices and start server
if __name__ == "__main__":
    db = Database()

    # Register CentralNodeDevice
    central_node_info = tango.DbDevInfo()
    central_node_info.server = "DeviceServer/01"
    central_node_info._class = "CentralNodeDevice"
    central_node_info.name = "sys/centralnode/1"
    db.add_device(central_node_info)

    # Register SubArrayDevice
    subarray1_info = tango.DbDevInfo()
    subarray1_info.server = "DeviceServer/01"
    subarray1_info._class = "SubArrayDevice"
    subarray1_info.name = "sys/subarray/1"
    db.add_device(subarray1_info)

    subarray2_info = tango.DbDevInfo()
    subarray2_info.server = "DeviceServer/01"
    subarray2_info._class = "SubArrayDevice"
    subarray2_info.name = "sys/subarray/2"
    db.add_device(subarray2_info)

    # Register DishDevice
    dish1_info = tango.DbDevInfo()
    dish1_info.server = "DeviceServer/01"
    dish1_info._class = "DishDevice"
    dish1_info.name = "sys/dish/1"
    db.add_device(dish1_info)

    dish2_info = tango.DbDevInfo()
    dish2_info.server = "DeviceServer/01"
    dish2_info._class = "DishDevice"
    dish2_info.name = "sys/dish/2"
    db.add_device(dish2_info)

    # Register ServoDevice
    servo1_info = tango.DbDevInfo()
    servo1_info.server = "DeviceServer/01"
    servo1_info._class = "ServoDevice"
    servo1_info.name = "sys/servo/1"
    db.add_device(servo1_info)

    servo2_info = tango.DbDevInfo()
    servo2_info.server = "DeviceServer/01"
    servo2_info._class = "ServoDevice"
    servo2_info.name = "sys/servo/2"
    db.add_device(servo2_info)

    # Run server
    print("Devices registered successfully!")
    run([CentralNodeDevice, SubArrayDevice, DishDevice, ServoDevice])
