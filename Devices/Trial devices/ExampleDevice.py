import tango
from tango import DevState, AttrWriteType
from tango.server import Device, attribute, command, run

class ExampleDevice(Device):
    # Define an attribute with read-write access
    some_value = attribute(dtype=int, access=AttrWriteType.READ_WRITE)

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("ExampleDevice initialized and ready.")
        self._some_value = 0

    def read_some_value(self):
        return self._some_value

    def write_some_value(self, value):
        # Define acceptable range for value
        if 0 <= value <= 100:
            self._some_value = value
            self.info_stream(f"some_value set to {self._some_value}.")
        else:
            # Log error for out-of-range values
            self.error_stream("Value out of range! Must be between 0 and 100.")
            # Set state to FAULT to indicate an error state
            self.set_state(DevState.FAULT)
            self.set_status("Error: Value out of range.")
            # Raise an exception to indicate an error
            raise ValueError("Value out of range. Must be between 0 and 100.")

    @command
    def reset_device(self):
        self._some_value = 0
        self.set_state(DevState.ON)
        self.set_status("Device reset successfully.")
        self.info_stream("Device reset and ready.")

# Run the server
if __name__ == "__main__":
    dev_info = tango.DbDevInfo()
    dev_info.server = "ExampleDevice/01"
    dev_info._class = "ExampleDevice"
    dev_info.name = "sys/example/1"
    db = tango.Database()
    try:
        db.add_device(dev_info)
    except tango.DevFailed as e:
        print(f"Failed to add CounterDevice to database: {e}")
        exit(1)
    run([ExampleDevice])
