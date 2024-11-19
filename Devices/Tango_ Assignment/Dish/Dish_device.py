import tango
from tango.server import Device
from tango.server import attribute, AttrWriteType, command, device_property
from tango import DeviceProxy, EventType, DevState
from tango.server import DevFailed  # type: ignore


# Level 3: Dish Device
class DishDevice(Device):

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status(self.get_status() + "DishDevice initialized.")
        self.dish_number = int(self.get_name().split("/")[-1])
        self.servo_proxy = self.get_servo_proxy(self.dish_number)
        self.frontend_device: DeviceProxy = self.get_frontend_proxy(self.dish_number)
        self.servo_proxy.subscribe_event(
            "PositionAchieved", EventType.CHANGE_EVENT, self.handle_servo_event
        )

        if self.servo_proxy:
            self.info_stream(
                f"DishDevice {self.dish_number} initialized and linked to servo/dev/{self.dish_number}."
            )
        else:
            self.error_stream(
                f"DishDevice {self.dish_number} failed to link to servo/dev/{self.dish_number}."
            )
            self.set_status(
                self.get_status()
                + "\n"
                + "Error: Unable to connect to corresponding ServoDevice."
            )

        if self.frontend_device:
            f"DishDevice {self.dish_number} initialized and linked to servo/dev/{self.dish_number}."

        else:
            self.error_stream(
                f"DishDevice {self.dish_number} failed to link to servo/dev/{self.dish_number}."
            )
            self.set_status(
                self.get_status()
                + "\n"
                + "Error: Unable to connect to corresponding ServoDevice."
            )

    def handle_servo_event(self, event):
        if not event.err and not event.attr_value.value:
            self.set_status(
                self.get_status()
                + "\n"
                + f"Servo: {event.device} has reached the desired position"
            )
            return f"Servo: {event.device} has reached the desired position"
        elif event.err:
            self.error_stream("Error in receiving event from child device.")

    def get_frontend_proxy(self, fe_number):
        fe_name = f"fe/dev/{fe_number}"
        try:
            return DeviceProxy(fe_name)
        except tango.DevFailed as e:
            self.error_stream(f"Failed to connect to FrontEnd Device {fe_name}: {e}")
            return None

    def get_servo_proxy(self, servo_number):
        """Helper function to get the proxy for the corresponding servo device."""
        servo_name = f"servo/dev/{servo_number}"
        try:
            return DeviceProxy(servo_name)
        except tango.DevFailed as e:
            self.error_stream(f"Failed to connect to Servo device {servo_name}: {e}")
            return None

    @command(dtype_in=float)
    def MoveToTarget(self, degrees):
        """Command the linked Servo device to move."""
        if self.servo_proxy:
            try:
                self.servo_proxy.command_inout("Mov", degrees)
                self.set_status(
                    self.get_status()
                    + "\n"
                    + f"Requested Servo to move by {degrees} degrees."
                )
            except tango.DevFailed as e:
                self.error_stream(f"Failed to execute Mov command on Servo device: {e}")
                self.set_status(self.get_status() + "Failed to command Servo device.")
        else:
            self.error_stream("No valid servo proxy found for move command.")

    @command(dtype_out=float)
    def ReadAntennaPosition(self):
        """Read the antenna position from the linked Servo device."""
        if self.servo_proxy:
            try:
                antenna_position = self.servo_proxy.read_attribute(
                    "AntennaPosition"
                ).value
                self.set_status(
                    self.get_status() + "\n" + f"Antenna Position: {antenna_position}"
                )
                return antenna_position
            except tango.DevFailed as e:
                self.error_stream(
                    f"Failed to read AntennaPosition from Servo device: {e}"
                )
                self.set_status(self.get_status() + "Failed to read AntennaPosition.")
        else:
            self.error_stream(
                "No valid servo proxy found for reading antenna position."
            )

    @command(dtype_in=float)
    def WriteTargetPosition(self, value):
        """Set the target position on the linked Servo device."""
        if self.servo_proxy:
            try:
                self.servo_proxy.write_attribute("TargetPosition", value)
                self.set_status(self.get_status() + f"Target Position set to: {value}")
            except tango.DevFailed as e:
                self.error_stream(
                    f"Failed to write TargetPosition to Servo device: {e}"
                )
                self.set_status(self.get_status() + "Failed to write TargetPosition.")
        else:
            self.error_stream("No valid servo proxy found for writing target position.")

    @command(dtype_out=float)
    def ReadTargetPosition(self):
        """Read the target position from the linked Servo device."""
        if self.servo_proxy:
            try:
                target_position = self.servo_proxy.read_attribute(
                    "TargetPosition"
                ).value
                self.set_status(
                    self.get_status() + "\n" + f"Target Position: {target_position}"
                )
                return target_position
            except tango.DevFailed as e:
                self.error_stream(
                    f"Failed to read TargetPosition from Servo device: {e}"
                )
                self.set_status(self.get_status() + "Failed to read TargetPosition.")
        else:
            self.error_stream("No valid servo proxy found for reading target position.")

    # Commands
    @command
    def on(self):
        self.set_state(DevState.ON)
        self.set_status(self.get_status() + "Device is in on position")

    @command
    def off(self):
        self.set_state(DevState.OFF)
        self.set_status(self.get_status() + "Dish is OFF")

    @command
    def moving(self):
        self.set_state(DevState.MOVING)
        self.set_status(self.get_status() + "Dish is moving")

    @command(dtype_in=float)
    def set_chn1_attn_FrontEnd(self, attn_value):

        self.frontend_device.command_inout("set_single_chn_attn", (1, attn_value))

    @command(dtype_in=float)
    def set_chn2_attn_FrontEnd(self, attn_value):

        self.frontend_device.command_inout("set_single_chn_attn", (2, attn_value))

    @command(dtype_in="DevVarLongArray")
    def set_both_chn_attn_FrontEnd(self, inp):
        self.frontend_device.command_inout("set_both_chn_attn", inp)

    @command(dtype_out=float)
    def get_chn1_attn_FrontEnd(self):
        attn = self.frontend_device.read_attribute("chn1_attn").value
        self.info_stream(f"{self.frontend_device.name()} chn1 attn : {attn}")
        return attn

    @command(dtype_out=float)
    def get_chn2_attn_FrontEnd(self):
        attn = self.frontend_device.read_attribute("chn2_attn").value
        self.info_stream(f"{self.frontend_device.name()} chn2 attn : {attn}")
        return attn

    @command(dtype_out=(float, float))
    def get_channel_attn(self):
        attn1, attn2 = (
            self.frontend_device.read_attribute("channel1Attn").value,
            self.frontend_device.read_attribute("channel2Attn").value,
        )

        self.info_stream(f"Channel 1 : {attn1} , Channel 1 : {attn2}")
        return attn1, attn2
