import tango
from tango import DevState, DeviceProxy
from tango.server import Device, command, run
from tango.server import DeviceGroup

# Registering Devices (this would normally go into a database or similar)
def register_devices():
    db = tango.Database()

    # Register SubDevices
    for i in range(1, 4):
        sub_dev_info = tango.DbDevInfo()
        sub_dev_info.server = "GroupExample/01"
        sub_dev_info._class = "SubDevice"
        sub_dev_info.name = f"sys/subdevice/{i}"
        try:
            db.add_device(sub_dev_info)
        except tango.DevFailed as e:
            print(f"Failed to add SubDevice {i}: {e}")

    # Register ControllerDevice
    controller_dev_info = tango.DbDevInfo()
    controller_dev_info.server = "GroupExample/01"
    controller_dev_info._class = "ControllerDevice"
    controller_dev_info.name = "sys/controller/1"
    try:
        db.add_device(controller_dev_info)
    except tango.DevFailed as e:
        print(f"Failed to add ControllerDevice: {e}")

    print("Devices registered successfully!")

# SubDevice class
class SubDevice(Device):
    current_value = tango.attribute(dtype=int, access=tango.AttrWriteType.READ_WRITE)

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("SubDevice initialized")
        self._value = 0  # Initial value

    def read_current_value(self):
        return self._value

    def write_current_value(self, value):
        self._value = value
        self.push_change_event("current_value", self._value)
        self.info_stream(f"SubDevice value updated to {self._value}")

# ControllerDevice class
class ControllerDevice(Device):
    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("ControllerDevice initialized.")
        self.sub_devices_group = DeviceGroup()  # Group for subdevices
        self.info_stream("Controller device initialized.")

    def add_to_group(self, sub_device_numbers):
        """Adds multiple subdevices to the group."""
        for sub_device_number in sub_device_numbers:
            proxy = DeviceProxy(f"sys/subdevice/{sub_device_number}")
            self.sub_devices_group.add_device(proxy)
            self.info_stream(f"Added {proxy.dev_name} to the group.")

    def execute_on_group(self, command_name, *args):
        """Executes a command on all devices in the group."""
        for device_proxy in self.sub_devices_group.get_devices():
            try:
                device_proxy.command_inout(command_name, *args)
                self.info_stream(f"Executed {command_name} on {device_proxy.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to execute {command_name} on {device_proxy.dev_name}: {e}")

    @command(dtype_in=int)
    def update_all_subdevices(self, value):
        """Updates the value on all subdevices at once."""
        # Add subdevices to the group
        self.add_to_group([1, 2, 3])
        # Execute the 'write_current_value' command on all subdevices in the group
        self.execute_on_group("write_current_value", value)

# Main function to register devices and start the Tango server
if __name__ == "__main__":
    register_devices()  # Register devices before running the server
    run([SubDevice, ControllerDevice])  # Run the Tango server
