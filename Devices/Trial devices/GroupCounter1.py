# import tango
# from tango import DevState, AttrWriteType, DeviceProxy
# from tango.server import Device, command, attribute, run
# from threading import Thread, Event
# import time

# def register_devices():
#     db = tango.Database()
#     for i in range(1, 4):
#         counter_dev_info = tango.DbDevInfo()
#         counter_dev_info.server = "GroupCounter1/01"  
#         counter_dev_info._class = "CounterDevice"
#         counter_dev_info.name = f"sys/counter/{i}"
#         try:
#             db.add_device(counter_dev_info)
#         except tango.DevFailed as e:
#             print(f"Failed to add Counter device {i}: {e}")

#     for i in range(1, 4):
#         controller_dev_info = tango.DbDevInfo()
#         controller_dev_info.server = "GroupCounter1/01"
#         controller_dev_info._class = "ControllerDevice"
#         controller_dev_info.name = f"sys/controller/{i}"
#         try:
#             db.add_device(controller_dev_info)
#         except tango.DevFailed as e:
#             print(f"Failed to add Controller device {i}: {e}")

#     print("Devices registered successfully!")

# class CounterDevice(Device):
#     current_count = attribute(dtype=int, access=AttrWriteType.READ)

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self.set_status("CounterDevice initialized")
#         self._count = 0
#         self._counting = Event()
#         self._counting.clear()

#     def read_current_count(self):
#         return self._count

#     def _counting_loop(self):
#         while self._counting.is_set() and self.get_state() == DevState.ON:
#             self._count += 1
#             self.push_change_event("current_count", self._count)
#             time.sleep(1)

#     @command
#     def start_counting(self):
#         if self.get_state() == DevState.ON and not self._counting.is_set():
#             self._counting.set()
#             self._counter_thread = Thread(target=self._counting_loop)
#             self._counter_thread.start()
#             self.info_stream("Counter started.")

#     @command
#     def stop_counting(self):
#         if self.get_state() == DevState.ON and self._counting.is_set():
#             self._counting.clear()
#             self._counter_thread.join()
#             self.info_stream("Counter stopped.")

#     @command(dtype_out=int)
#     def get_count(self):
#         return self._count if self.get_state() == DevState.ON else -1

#     @command
#     def reset_count(self):
#         self._count = 0
#         self.push_change_event("current_count", self._count)
#         self.info_stream("Counter reset to zero.")

#     @command
#     def turn_off(self):
#         self.stop_counting()
#         self.set_state(DevState.OFF)
#         self.set_status("CounterDevice is OFF.")

#     @command
#     def turn_on(self):
#         self.set_state(DevState.ON)
#         self.set_status("CounterDevice is ON.")

# class ControllerDevice(Device):
#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self.set_status("ControllerDevice initialized.")

#         # Extract controller number from device name
#         self.controller_number = int(self.get_name().split('/')[-1])

#         # Link to the corresponding counter device
#         self.counter_proxy = self.get_counter_proxy(self.controller_number)
#         self.info_stream(f"Controller device {self.controller_number} initialized and linked to sys/counter/{self.controller_number}.")

#     def get_counter_proxy(self, counter_number):
#         """Helper function to get the proxy for the corresponding counter device."""
#         counter_name = f"sys/counter/{counter_number}"
#         try:
#             return DeviceProxy(counter_name)
#         except tango.DevFailed as e:
#             self.error_stream(f"Failed to connect to counter {counter_name}: {e}")
#             return None

#     @command
#     def start_counter(self):
#         """Start counting on this controller's specific counter."""
#         if self.counter_proxy:
#             try:
#                 self.counter_proxy.command_inout("start_counting")
#                 self.info_stream(f"Started counting on {self.counter_proxy.dev_name}")
#             except tango.DevFailed as e:
#                 self.error_stream(f"Failed to start counting on {self.counter_proxy.dev_name}: {e}")

#     @command
#     def stop_counter(self):
#         """Stop counting on this controller's specific counter."""
#         if self.counter_proxy:
#             try:
#                 self.counter_proxy.command_inout("stop_counting")
#                 self.info_stream(f"Stopped counting on {self.counter_proxy.dev_name}")
#             except tango.DevFailed as e:
#                 self.error_stream(f"Failed to stop counting on {self.counter_proxy.dev_name}: {e}")

#     @command
#     def reset_counter(self):
#         """Reset the count on this controller's specific counter."""
#         if self.counter_proxy:
#             try:
#                 self.counter_proxy.command_inout("reset_count")
#                 self.info_stream(f"Reset counter on {self.counter_proxy.dev_name}")
#             except tango.DevFailed as e:
#                 self.error_stream(f"Failed to reset counter on {self.counter_proxy.dev_name}: {e}")

#     @command
#     def turn_off_counter(self):
#         """Turn off this controller's specific counter."""
#         if self.counter_proxy:
#             try:
#                 self.counter_proxy.command_inout("turn_off")
#                 self.info_stream(f"Turned off {self.counter_proxy.dev_name}")
#             except tango.DevFailed as e:
#                 self.error_stream(f"Failed to turn off {self.counter_proxy.dev_name}: {e}")

#     @command
#     def turn_on_counter(self):
#         """Turn on this controller's specific counter."""
#         if self.counter_proxy:
#             try:
#                 self.counter_proxy.command_inout("turn_on")
#                 self.info_stream(f"Turned on {self.counter_proxy.dev_name}")
#             except tango.DevFailed as e:
#                 self.error_stream(f"Failed to turn on {self.counter_proxy.dev_name}: {e}")


# if __name__ == "__main__":
#     register_devices()  # Register the devices before running the server
#     run([CounterDevice, ControllerDevice])  # Run the server

import tango
from tango import DevState, AttrWriteType, DeviceProxy
from tango.server import Device, command, attribute, run
from tango import Group
from threading import Thread, Event
import time

def register_devices():
    db = tango.Database()
    
    # Register Counter devices
    for i in range(1, 4):  # Assuming 3 Counter devices
        counter_dev_info = tango.DbDevInfo()
        counter_dev_info.server = "GroupCounter1/01"
        counter_dev_info._class = "CounterDevice"
        counter_dev_info.name = f"sys/counter/{i}"
        try:
            db.add_device(counter_dev_info)
        except tango.DevFailed as e:
            print(f"Failed to add Counter device {i}: {e}")
    
    # Register Controller devices
    for i in range(1, 4):  # Assuming 3 Controller devices
        controller_dev_info = tango.DbDevInfo()
        controller_dev_info.server = "GroupCounter1/01"
        controller_dev_info._class = "ControllerDevice"
        controller_dev_info.name = f"sys/controller/{i}"
        try:
            db.add_device(controller_dev_info)
        except tango.DevFailed as e:
            print(f"Failed to add Controller device {i}: {e}")

    # Register Subarray device
    subarray_dev_info = tango.DbDevInfo()
    subarray_dev_info.server = "GroupCounter1/01"
    subarray_dev_info._class = "Subarray"
    subarray_dev_info.name = "sys/subarray/1"
    try:
        db.add_device(subarray_dev_info)
    except tango.DevFailed as e:
        print(f"Failed to add Subarray device: {e}")

    print("Devices registered successfully!")

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

class ControllerDevice(Device):
    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("ControllerDevice initialized.")

        # Extract controller number from device name
        self.controller_number = int(self.get_name().split('/')[-1])

        # Link to the corresponding counter device
        self.counter_proxy = self.get_counter_proxy(self.controller_number)
        self.info_stream(f"Controller device {self.controller_number} initialized and linked to sys/counter/{self.controller_number}.")

    def get_counter_proxy(self, counter_number):
        """Helper function to get the proxy for the corresponding counter device."""
        counter_name = f"sys/counter/{counter_number}"
        try:
            return DeviceProxy(counter_name)
        except tango.DevFailed as e:
            self.error_stream(f"Failed to connect to counter {counter_name}: {e}")
            return None

    @command
    def start_counter(self):
        """Start counting on this controller's specific counter."""
        if self.counter_proxy:
            try:
                self.counter_proxy.command_inout("start_counting")
                self.info_stream(f"Started counting on {self.counter_proxy.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to start counting on {self.counter_proxy.dev_name}: {e}")

    @command
    def stop_counter(self):
        """Stop counting on this controller's specific counter."""
        if self.counter_proxy:
            try:
                self.counter_proxy.command_inout("stop_counting")
                self.info_stream(f"Stopped counting on {self.counter_proxy.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to stop counting on {self.counter_proxy.dev_name}: {e}")

    @command
    def reset_counter(self):
        """Reset the count on this controller's specific counter."""
        if self.counter_proxy:
            try:
                self.counter_proxy.command_inout("reset_count")
                self.info_stream(f"Reset counter on {self.counter_proxy.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to reset counter on {self.counter_proxy.dev_name}: {e}")

    @command
    def turn_off_counter(self):
        """Turn off this controller's specific counter."""
        if self.counter_proxy:
            try:
                self.counter_proxy.command_inout("turn_off")
                self.info_stream(f"Turned off {self.counter_proxy.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to turn off {self.counter_proxy.dev_name}: {e}")

    @command
    def turn_on_counter(self):
        """Turn on this controller's specific counter."""
        if self.counter_proxy:
            try:
                self.counter_proxy.command_inout("turn_on")
                self.info_stream(f"Turned on {self.counter_proxy.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to turn on {self.counter_proxy.dev_name}: {e}")

class Subarray(Device):
    
    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("Subarray device initialized.")
        
        # Correct device initialization
        try:
            self.subarray_device = DeviceProxy("sys/subarray/1")
        except tango.DevFailed as e:
            self.error_stream(f"Failed to connect to sys/subarray/1: {e}")

    @command
    def group_start_counting(self):
        """Send a start counting command to all ControllerDevices manually."""
        controller_devices = [
            DeviceProxy(f"sys/controller/{i}") for i in range(1, 4)  # Assuming 3 controllers
        ]
        for device in controller_devices:
            try:
                device.command_inout("start_counter")
                self.info_stream(f"Started counting on {device.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to start counting on {device.dev_name}: {e}")

    @command
    def group_stop_counting(self):
        """Send a stop counting command to all ControllerDevices manually."""
        controller_devices = [
            DeviceProxy(f"sys/controller/{i}") for i in range(1, 4)
        ]
        for device in controller_devices:
            try:
                device.command_inout("stop_counter")
                self.info_stream(f"Stopped counting on {device.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to stop counting on {device.dev_name}: {e}")

    @command
    def group_reset_count(self):
        """Send a reset count command to all ControllerDevices manually."""
        controller_devices = [
            DeviceProxy(f"sys/controller/{i}") for i in range(1, 4)
        ]
        for device in controller_devices:
            try:
                device.command_inout("reset_counter")
                self.info_stream(f"Reset counter on {device.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to reset counter on {device.dev_name}: {e}")

    @command
    def group_turn_off(self):
        """Send a turn off command to all ControllerDevices manually."""
        controller_devices = [
            DeviceProxy(f"sys/controller/{i}") for i in range(1, 4)
        ]
        for device in controller_devices:
            try:
                device.command_inout("turn_off_counter")
                self.info_stream(f"Turned off {device.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to turn off {device.dev_name}: {e}")

    @command
    def group_turn_on(self):
        """Send a turn on command to all ControllerDevices manually."""
        controller_devices = [
            DeviceProxy(f"sys/controller/{i}") for i in range(1, 4)
        ]
        for device in controller_devices:
            try:
                device.command_inout("turn_on_counter")
                self.info_stream(f"Turned on {device.dev_name}")
            except tango.DevFailed as e:
                self.error_stream(f"Failed to turn on {device.dev_name}: {e}")


if __name__ == "__main__":
    register_devices()  # Register devices before running the server
    run([Subarray, ControllerDevice, CounterDevice])




