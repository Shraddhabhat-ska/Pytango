import tango
from tango import DevState, AttrWriteType, Database, DeviceProxy
from tango.server import Device, command, attribute, run, device_property

# Device: ServoMotor
class ServoMotor(Device):
    azimuth_position = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
    elevation_position = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
    azimuth_speed = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
    elevation_speed = attribute(dtype=float, access=AttrWriteType.READ_WRITE)
    motor_temperature = attribute(dtype=float, access=AttrWriteType.READ)
    error_code = attribute(dtype=int, access=AttrWriteType.READ)

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("ServoMotor initialized and waiting for commands.")
        self._azimuth_position = 0.0
        self._elevation_position = 0.0
        self._azimuth_speed = 0.0
        self._elevation_speed = 0.0
        self._motor_temperature = 25.0
        self._error_code = 0

    def read_azimuth_position(self):
        return self._azimuth_position

    def write_azimuth_position(self, position):
        if -180.0 <= position <= 180.0:
            self._azimuth_position = position
            self.push_change_event("azimuth_position", self._azimuth_position)
            self.info_stream(f"Azimuth position set to {self._azimuth_position}.")
        else:
            self._error_code = 1
            self.warn_stream("Azimuth position out of range! Allowed: -180 to 180.")
            raise ValueError("Azimuth position out of range. Must be between -180° and 180°.")

    def read_elevation_position(self):
        return self._elevation_position

    def write_elevation_position(self, position):
        if 0.0 <= position <= 90.0:
            self._elevation_position = position
            self.push_change_event("elevation_position", self._elevation_position)
            self.info_stream(f"Elevation position set to {self._elevation_position}.")
        else:
            self._error_code = 2
            self.warn_stream("Elevation position out of range! Allowed: 0 to 90.")
            raise ValueError("Elevation position out of range. Must be between 0° and 90°.")

    def read_azimuth_speed(self):
        return self._azimuth_speed

    def write_azimuth_speed(self, speed):
        if 0.0 <= speed <= 10.0:
            self._azimuth_speed = speed
            self.push_change_event("azimuth_speed", self._azimuth_speed)
            self.info_stream(f"Azimuth speed set to {self._azimuth_speed}.")
        else:
            self._error_code = 3
            self.warn_stream("Azimuth speed out of range! Allowed: 0 to 10.")
            raise ValueError("Azimuth speed out of range. Must be between -10°/s and 10°/s.")

    def read_elevation_speed(self):
        return self._elevation_speed

    def write_elevation_speed(self, speed):
        if 0.0 <= speed <= 5.0:
            self._elevation_speed = speed
            self.push_change_event("elevation_speed", self._elevation_speed)
            self.info_stream(f"Elevation speed set to {self._elevation_speed}.")
        else:
            self._error_code = 4
            self.warn_stream("Elevation speed out of range! Allowed: 0 to 5.")
            raise ValueError("Elevation speed out of range. Must be between 0°/s and 5°/s.")

    def read_motor_temperature(self):
        return self._motor_temperature

    def read_error_code(self):
        return self._error_code

    @command
    def reset_motor(self):
        self._azimuth_position = 0.0
        self._elevation_position = 0.0
        self._azimuth_speed = 0.0
        self._elevation_speed = 0.0
        self._error_code = 0
        self.info_stream("Motor reset to default values with error code cleared.")


# Device: ControlSystem
class ControlSystem(Device):
    motor_device_name = "sys/servomotor/1"

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("ControlSystem initialized and running.")
        if self.motor_device_name:
            self._motor_proxy = DeviceProxy(self.motor_device_name)
            self.info_stream("Connected to ServoMotor.")
        else:
            self.error_stream("ServoMotor name not set. Check motor_device_name property.")
            self.set_status("ServoMotor name not set.")
            self.set_state(DevState.FAULT)

    @command(dtype_in=float)
    def set_azimuth_position(self, position):
        if self._motor_proxy:
            self._motor_proxy.write_attribute("azimuth_position", position)

    @command(dtype_in=float)
    def set_elevation_position(self, position):
        if self._motor_proxy:
            self._motor_proxy.write_attribute("elevation_position", position)

    @command(dtype_in=float)
    def set_azimuth_speed(self, speed):
        if self._motor_proxy:
            self._motor_proxy.write_attribute("azimuth_speed", speed)

    @command(dtype_in=float)
    def set_elevation_speed(self, speed):
        if self._motor_proxy:
            self._motor_proxy.write_attribute("elevation_speed", speed)

    @command(dtype_out=float)
    def get_azimuth_position(self):
        if self._motor_proxy:
            return self._motor_proxy.read_attribute("azimuth_position").value

    @command(dtype_out=float)
    def get_elevation_position(self):
        if self._motor_proxy:
            return self._motor_proxy.read_attribute("elevation_position").value

    @command(dtype_out=float)
    def get_azimuth_speed(self):
        if self._motor_proxy:
            return self._motor_proxy.read_attribute("azimuth_speed").value

    @command(dtype_out=float)
    def get_elevation_speed(self):
        if self._motor_proxy:
            return self._motor_proxy.read_attribute("elevation_speed").value

    @command(dtype_out=float)
    def get_motor_temperature(self):
        if self._motor_proxy:
            return self._motor_proxy.read_attribute("motor_temperature").value


    @command(dtype_out=int)
    def get_error_code(self):
        if self._motor_proxy:
            return self._motor_proxy.read_attribute("error_code").value

    @command
    def reset_motor(self):
        if self._motor_proxy:
            self._motor_proxy.command_inout("reset_motor")


# Ensure device registration and start server
if __name__ == "__main__":
    db = Database()

    # Setup for ServoMotor device
    motor_dev_info = tango.DbDevInfo()
    motor_dev_info.server = "ServoMotor/01"
    motor_dev_info._class = "ServoMotor"
    motor_dev_info.name = "sys/servomotor/1"

    # Setup for ControlSystem device
    control_dev_info = tango.DbDevInfo()
    control_dev_info.server = "ServoMotor/01"
    control_dev_info._class = "ControlSystem"
    control_dev_info.name = "sys/servocontroller/1"
    control_dev_info.properties = {'motor_device_name': "sys/servomotor/1"}

    # Register devices if not already in database
    try:
        db.get_device_info("sys/servomotor/1")
        print("sys/servomotor/1 is already registered.")
    except tango.DevFailed:
        print("Registering sys/servomotor/1.")
        db.add_device(motor_dev_info)

    try:
        db.get_device_info("sys/servocontroller/1")
        print("sys/servocontroller/1 is already registered.")
    except tango.DevFailed:
        print("Registering sys/servocontroller/1.")
        db.add_device(control_dev_info)

    # Run the device server
    run([ServoMotor, ControlSystem])
