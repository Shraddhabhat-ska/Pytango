import tango
from tango import DevState, AttrWriteType, Database, Group
from tango.server import Device, command, attribute, run
from threading import Thread, Event
import time

# Device: Counter
class CounterDevice(Device):
    current_count = attribute(dtype=int, access=AttrWriteType.READ)

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("CounterDevice initialized")
        self._count = 0
        self._counting = Event()
        self._counting.clear()

    def read_current_count(self):
        return self._count

    def _counting_loop(self):
        while self._counting.is_set() and self.get_state() == DevState.ON:
            self._count += 1
            self.push_change_event("current_count", self._count)
            time.sleep(1)

    @command
    def start_counting(self):
        if self.get_state() == DevState.ON and not self._counting.is_set():
            self._counting.set()
            self._counter_thread = Thread(target=self._counting_loop)
            self._counter_thread.start()
            self.info_stream("Counter started.")

    @command
    def stop_counting(self):
        if self.get_state() == DevState.ON and self._counting.is_set():
            self._counting.clear()
            self._counter_thread.join()
            self.info_stream("Counter stopped.")

    @command(dtype_out=int)
    def get_count(self):
        return self._count if self.get_state() == DevState.ON else -1

    @command
    def reset_count(self):
        self._count = 0
        self.push_change_event("current_count", self._count)
        self.info_stream("Counter reset to zero.")

    @command
    def turn_off(self):
        self.stop_counting()
        self.set_state(DevState.OFF)
        self.set_status("CounterDevice is OFF.")

    @command
    def turn_on(self):
        self.set_state(DevState.ON)
        self.set_status("CounterDevice is ON.")

# Device: Controller
class ControllerDevice(Device):
    counter_device_names = ["sys/counter/1", "sys/counter/2", "sys/counter/3"]

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("ControllerDevice initialized and connected to counters.")
        
        # Create a group for counter devices and add them to the group
        self.counter_group = Group("CounterGroup")
        for name in self.counter_device_names:
            self.counter_group.add(name)
        
        self.info_stream("Connected to Counter devices.")

    @command
    def start_all_counters(self):
        results = self.counter_group.command_inout("start_counting")
        for result in results:
            if result.has_failed:
                self.error_stream(f"Failed to start counting on {result.dev_name}")
            else:
                self.info_stream(f"Started counting on {result.dev_name}")

    @command
    def stop_all_counters(self):
        results = self.counter_group.command_inout("stop_counting")
        for result in results:
            if result.has_failed:
                self.error_stream(f"Failed to stop counting on {result.dev_name}")
            else:
                self.info_stream(f"Stopped counting on {result.dev_name}")

    @command
    def reset_all_counters(self):
        results = self.counter_group.command_inout("reset_count")
        for result in results:
            if result.has_failed:
                self.error_stream(f"Failed to reset counter on {result.dev_name}")
            else:
                self.info_stream(f"Reset counter on {result.dev_name}")

    @command
    def turn_off_all_counters(self):
        results = self.counter_group.command_inout("turn_off")
        for result in results:
            if result.has_failed:
                self.error_stream(f"Failed to turn off {result.dev_name}")
            else:
                self.info_stream(f"Turned off {result.dev_name}")

    @command
    def turn_on_all_counters(self):
        results = self.counter_group.command_inout("turn_on")
        for result in results:
            if result.has_failed:
                self.error_stream(f"Failed to turn on {result.dev_name}")
            else:
                self.info_stream(f"Turned on {result.dev_name}")

# Function to register devices in the Tango database
def register_devices():
    db = Database()

    # Define Counter devices
    for i in range(1, 4):
        counter_dev_info = tango.DbDevInfo()
        counter_dev_info.server = "GroupCounter/01"
        counter_dev_info._class = "CounterDevice"
        counter_dev_info.name = f"sys/counter/{i}"
        db.add_device(counter_dev_info)

    # Define Controller device
    controller_dev_info = tango.DbDevInfo()
    controller_dev_info.server = "GroupCounter/01"
    controller_dev_info._class = "ControllerDevice"
    controller_dev_info.name = "sys/controller/1"
    db.add_device(controller_dev_info)

    print("Devices registered successfully!")

if __name__ == "__main__":
    # Register devices in the Tango database
    register_devices()

    # Run the device servers
    run([CounterDevice, ControllerDevice])
