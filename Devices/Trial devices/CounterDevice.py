import tango
from tango import DevState, AttrWriteType, DeviceProxy
from tango.server import Device, command, attribute, run, device_property
import time


class CounterDevice(Device):
    # Define the attribute for current count
    current_count = attribute(dtype=int, access=AttrWriteType.READ)
    
    # Maximum threshold for warning state
    max_warning_threshold = 100  # Example threshold value

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("CounterDevice initialized and running.")
        self._count = 0  # Initial count value

    # Read method for the current count
    def read_current_count(self):
        return self._count

    # Increment count and check threshold
    @command
    def increment_count(self):
        """Command to increment the count."""
        self._count += 1
        
        # Check if count exceeds the max warning threshold
        if self._count >= self.max_warning_threshold:
            # Set device to WARNING state and update status message
            self.set_state(DevState.WARNING)
            self.set_status(f"Warning: Count has reached the maximum threshold of {self.max_warning_threshold}.")
            self.push_change_event("current_count", self._count)
            self.info_stream("Threshold reached: Counter is in WARNING state.")
        else:
            # Reset state to ON if under the threshold
            self.set_state(DevState.ON)
            self.set_status("CounterDevice running normally.")
            self.push_change_event("current_count", self._count)
            self.info_stream(f"Counter incremented to {self._count}.")

    # Reset the count back to zero
    @command
    def reset_count(self):
        """Command to reset the count to zero."""
        self._count = 0
        self.set_state(DevState.ON)  # Reset to normal state
        self.set_status("CounterDevice reset to zero and running normally.")
        self.push_change_event("current_count", self._count)
        self.info_stream("Counter has been reset to zero.")

    # Retrieve the current count directly
    @command(dtype_out=int)
    def get_count(self):
        """Command to retrieve the current count."""
        return self._count


if __name__ == "__main__":
    # Register the CounterDevice in the Tango database
    counter_dev_info = tango.DbDevInfo()
    counter_dev_info.server = "CounterDevice/01"
    counter_dev_info._class = "CounterDevice"
    counter_dev_info.name = "sys/counter/1"

    # Initialize Tango database and register the device
    db = tango.Database()
    try:
        db.add_device(counter_dev_info)
    except tango.DevFailed as e:
        print(f"Failed to add CounterDevice to database: {e}")
        exit(1)

    # Run the CounterDevice server
    run([CounterDevice])
