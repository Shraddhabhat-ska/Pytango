import tango
from tango import DevState, AttrWriteType, Database, DeviceProxy, Group, DeviceData, DevVarStringArray
from tango.server import Device, attribute, run, command, device_property, pipe

# Register devices in the Tango Database
def register_devices():
    db = tango.Database()
    for i in range(1, 6):  # Registering servo devices
        dev_info = tango.DbDevInfo()
        dev_info.server = "ServoDevice/01"
        dev_info._class = "ServoDevice"
        dev_info.name = f"sys/servo/{i}"
        
        try:
            db.add_device(dev_info)
            print(f"Device sys/servo/{i} registered successfully!")
        except tango.DevFailed as e:
            print(f"Failed to register device sys/servo/{i}: {e}")

    # Register Dish devices, each linked to a specific servo
    for i in range(1, 6):
        dish_info = tango.DbDevInfo()
        dish_info.server = "ServoDevice/01"
        dish_info._class = "DishDevice"
        dish_info.name = f"sys/dish/{i}"
                  
        try:
            db.add_device(dish_info)
            print(f"Device sys/dish/{i} registered successfully!")
        except tango.DevFailed as e:
            print(f"Failed to register device sys/dish/{i}: {e}")
    
    # Register Subarray device
    subarray_info = tango.DbDevInfo()
    subarray_info.server = "ServoDevice/01"
    subarray_info._class = "Subarray"
    subarray_info.name = "sys/subarray/1"
    try:
        db.add_device(subarray_info)
    except tango.DevFailed as e:
        print(f"Failed to add Subarray device: {e}")
    print("Device server started!")


# Servo Device class
class ServoDevice(Device):
    AntennaPosition = attribute(dtype=float, access=AttrWriteType.READ)
    TargetPosition = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
    ErrorPosition = attribute(dtype=float, access=AttrWriteType.READ)
    PositionAchieved = attribute(dtype=bool, access=AttrWriteType.READ)

    # Initialize device and attributes
    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self._antenna_position = 0.0
        self._target_position = 0.0
        self._error_position = 0.0
        self._position_achieved = False
        self.set_status("ServoDevice initialized and ready.")

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

    # Calculate the error position and check if target is achieved
    def calculate_error_position(self):
        self._error_position = self._target_position - self._antenna_position
        self._position_achieved = abs(self._error_position) < 0.1
        self.push_change_event("ErrorPosition", self._error_position)
        self.push_change_event("PositionAchieved", self._position_achieved)

    @command(dtype_in=float)
    def Mov(self, degrees):
        self._antenna_position += degrees
        self.calculate_error_position()
        if self._position_achieved:
            self.set_status("Target position reached.")
        else:
            self.set_status(f"Moved antenna by {degrees} degrees. Current position: {self._antenna_position}")


# Dish Device class
class DishDevice(Device):
    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("DishDevice initialized.")
        self.dish_number = int(self.get_name().split('/')[-1])
        self.servo_proxy = self.get_servo_proxy(self.dish_number)
        if self.servo_proxy:
            self.info_stream(f"DishDevice {self.dish_number} initialized and linked to sys/servo/{self.dish_number}.")
        else:
            self.error_stream(f"DishDevice {self.dish_number} failed to link to sys/servo/{self.dish_number}.")
            self.set_status("Error: Unable to connect to corresponding ServoDevice.")

    # Get the proxy for the corresponding servo device
    def get_servo_proxy(self, servo_number):
        servo_name = f"sys/servo/{servo_number}"
        try:
            return DeviceProxy(servo_name)
        except tango.DevFailed as e:
            self.error_stream(f"Failed to connect to Servo device {servo_name}: {e}")
            return None

    @command(dtype_in=float)
    def MoveToTarget(self, degrees):
        if self.servo_proxy:
            try:
                self.servo_proxy.command_inout("Mov", degrees)
                self.set_status(f"Requested Servo to move by {degrees} degrees.")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to execute Mov command on Servo device: {e}")
                self.set_status("Failed to command Servo device.")
        else:
            self.error_stream("No valid servo proxy found for move command.")

    @command
    def ReadAntennaPosition(self):
        if self.servo_proxy:
            try:
                antenna_position = self.servo_proxy.read_attribute("AntennaPosition").value
                self.set_status(f"Antenna Position: {antenna_position}")
                return antenna_position
            except tango.DevFailed as e:
                self.error_stream(f"Failed to read AntennaPosition from Servo device: {e}")
                self.set_status("Failed to read AntennaPosition.")
        else:
            self.error_stream("No valid servo proxy found for reading antenna position.")

    @command(dtype_in=float)
    def WriteTargetPosition(self, value):
        if self.servo_proxy:
            try:
                self.servo_proxy.write_attribute("TargetPosition", value)
                self.set_status(f"Target Position set to: {value}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to write TargetPosition to Servo device: {e}")
                self.set_status("Failed to write TargetPosition.")
        else:
            self.error_stream("No valid servo proxy found for writing target position.")

    @command
    def ReadTargetPosition(self):
        if self.servo_proxy:
            try:
                target_position = self.servo_proxy.read_attribute("TargetPosition").value
                self.set_status(f"Target Position: {target_position}")
                return target_position
            except tango.DevFailed as e:
                self.error_stream(f"Failed to read TargetPosition from Servo device: {e}")
                self.set_status("Failed to read TargetPosition.")
        else:
            self.error_stream("No valid servo proxy found for reading target position.")


# Subarray Device class
class Subarray(Device):
    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("Subarray device initialized.")
        
        # Initialize proxies for all Dish devices in the group
        self.dish_proxies = {}
        for i in range(1, 6):
            device_name = f"sys/dish/{i}"
            try:
                self.dish_proxies[device_name] = DeviceProxy(device_name)
                self.info_stream(f"Subarray device linked to Dish {i}.")
            except Exception as e:
                self.error_stream(f"Failed to link Subarray device to Dish {i}: {e}")
        
        self.info_stream("Subarray initialized with all dish devices in a group.")

    @command(dtype_in=float)
    def group_move_to_target(self, degrees):
        results = []
        for dish_device, dish_proxy in self.dish_proxies.items():
            try:
                result = dish_proxy.command_inout("MoveToTarget", degrees)
                results.append((dish_device, result))
            except Exception as e:
                self.error_stream(f"Failed to move {dish_device}: {e}")
                results.append((dish_device, "Failed"))

        for dish_device, status in results:
            if status == "Failed":
                self.error_stream(f"Failed to move {dish_device}")
            else:
                self.info_stream(f"Dish {dish_device} moved by {degrees} degrees.")

    @command(dtype_in=float)
    def group_write_target_position(self, target_position):
        results = []
        for dish_device, dish_proxy in self.dish_proxies.items():
            try:
                result = dish_proxy.command_inout("WriteTargetPosition", target_position)
                results.append((dish_device, result))
            except Exception as e:
                self.error_stream(f"Failed to write TargetPosition to {dish_device}: {e}")
                results.append((dish_device, "Failed"))

        for dish_device, status in results:
            if status == "Failed":
                self.error_stream(f"Failed to set TargetPosition for {dish_device}")
            else:
                self.info_stream(f"Set TargetPosition for Dish {dish_device} to {target_position}.")

    @command(dtype_out=DevVarStringArray)
    def read_group_antenna_position(self):
        antenna_positions = []
        for dish_device_name, dish_proxy in self.dish_proxies.items():
            servo_device_name = f"sys/servo/{dish_device_name.split('/')[-1]}"
            try:
                servo_proxy = DeviceProxy(servo_device_name)
                antenna_position = servo_proxy.read_attribute("AntennaPosition").value
                antenna_positions.append(f"{dish_device_name}: {antenna_position}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to read AntennaPosition from {dish_device_name}: {e}")
                antenna_positions.append(f"{dish_device_name}: Error")
        return antenna_positions
    @command(dtype_out=DevVarStringArray)
    def read_group_target_position(self):        
        target_positions = []
        for dish_device_name, dish_proxy in self.dish_proxies.items():            
            servo_device_name = f"sys/servo/{dish_device_name.split('/')[-1]}"
            try:                
                servo_proxy = DeviceProxy(servo_device_name)                
                target_position = servo_proxy.read_attribute("TargetPosition").value
                position_info = f"Target Position for {dish_device_name}: {target_position}"
                target_positions.append(position_info)
                self.info_stream(position_info)
            except tango.DevFailed as e:
                error_info = f"Failed to read TargetPosition from {dish_device_name}: {e}"
                target_positions.append(error_info)
                self.error_stream(error_info)        
        return target_positions


if __name__ == "__main__":
    register_devices()
    run([ServoDevice, DishDevice, Subarray])
