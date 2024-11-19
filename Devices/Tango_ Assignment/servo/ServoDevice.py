import tango
from tango import DevState, AttrWriteType, Database, DeviceProxy
from tango.server import Device, attribute, run, command, device_property


def register_devices():
    db = tango.Database()
    for i in range(1, 6):  # Looping through device numbers 1 to 5 (for servo devices)
        dev_info = tango.DbDevInfo()
        dev_info.server = "ServoDevice/01"
        dev_info._class = "ServoDevice"
        dev_info.name = (
            f"sys/servo/{i}"  # Format device name as sys/servo/01, sys/servo/02, etc.
        )

        try:
            db.add_device(dev_info)
            print(f"Device sys/servo/{i} registered successfully!")
        except tango.DevFailed as e:
            print(f"Failed to register device sys/servo/{i}: {e}")

    # Register Dish devices dynamically, each linked to a specific servo
    for i in range(1, 6):  # Looping through device numbers 1 to 5
        dish_info = tango.DbDevInfo()
        dish_info.server = "ServoDevice/01"
        dish_info._class = "DishDevice"
        dish_info.name = (
            f"sys/dish/{i}"  # Format device name as sys/dish/01, sys/dish/02, etc.
        )

        try:
            db.add_device(dish_info)
            print(f"Device sys/dish/{i} registered successfully!")
        except tango.DevFailed as e:
            print(f"Failed to register device sys/dish/{i}: {e}")
    print("Device server started!")


# Level 4: Servo Device
class ServoDevice(Device):
    AntennaPosition = attribute(dtype=float, access=AttrWriteType.READ)
    TargetPosition = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
    ErrorPosition = attribute(dtype=float, access=AttrWriteType.READ)
    PositionAchieved = attribute(
        dtype=bool,
        access=AttrWriteType.READ
    )

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self._antenna_position = 0.0
        self._target_position = 0.0
        self._error_position = 0.0
        self._position_achieved = False
        self.poll_attribute("PositionAchieved", 1000)
        self.set_status(self.get_status() + "\n" + "ServoDevice initialized and ready.")
        self.set_state(DevState.ON)

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
        self.push_change_event("ErrorPosition", self._error_position)
        self.push_change_event("PositionAchieved", self._position_achieved)

    @command(dtype_in=float)
    def Mov(self, degrees):
        self._antenna_position += degrees
        self.calculate_error_position()
        if self._position_achieved:
            self.set_status(self.get_status() + "\n" + "Target position reached.")
        else:
            self.set_status(
                self.get_status()
                + "\n"
                + f"Moved antenna by {degrees} degrees. Current position: {self._antenna_position}"
            )


# Main function to start the server
if __name__ == "__main__":
    register_devices()
    # Run the device server
    print("Device server started!")
    run([ServoDevice])
