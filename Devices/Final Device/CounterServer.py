# import tango
# from tango import DevState, AttrWriteType
# from tango.server import Device, command, attribute, run, device_property
# from threading import Thread, Event
# import time

# # Device2: Counter
# class CounterDevice(Device):
#     # Attribute: Current count value
#     current_count = attribute(dtype=int, access=AttrWriteType.READ)

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self.set_status("CounterDevice initialized and waiting for commands.")
#         self._count = 0
#         self._counting = Event()
#         self._counting.clear()
        
#     # Read method for current_count
#     def read_current_count(self):
#         return self._count

#     # Method to count in a separate thread
#     def _counting_loop(self):
#         while self._counting.is_set():
#             self._count += 1
#             self.push_change_event("current_count", self._count)
#             time.sleep(1)  # Increment count every second

#     @command
#     def start_counting(self):
#         """Command to start counting."""
#         if not self._counting.is_set():
#             self._counting.set()
#             self._counter_thread = Thread(target=self._counting_loop)
#             self._counter_thread.start()
#             self.info_stream("Counter started.")

#     @command
#     def stop_counting(self):
#         """Command to stop counting."""
#         if self._counting.is_set():
#             self._counting.clear()
#             self._counter_thread.join()
#             self.info_stream("Counter stopped.")

#     @command(dtype_out=int)
#     def get_count(self):
#         """Command to retrieve the current count."""
#         return self._count


# # Device1: Controller
# class ControllerDevice(Device):
#     # Device property to specify CounterDevice's device name
#     counter_device_name = device_property(dtype=str)

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self.set_status("ControllerDevice initialized and running.")
        
#         # Initialize device proxy for CounterDevice
#         if self.counter_device_name:
#             self._counter_proxy = tango.DeviceProxy(self.counter_device_name)
#             self.info_stream("Connected to CounterDevice.")
#         else:
#             self.error_stream("Counter device name is not set. Cannot connect to CounterDevice.")

#     def read_counter_device_name(self):
#         """Method to return the CounterDevice's device name."""
#         return self.counter_device_name

#     @command
#     def start_counter(self):
#         """Command to start the counter on CounterDevice."""
#         self._counter_proxy.command_inout("start_counting")

#     @command
#     def stop_counter(self):
#         """Command to stop the counter on CounterDevice."""
#         self._counter_proxy.command_inout("stop_counting")

#     @command(dtype_out=int)
#     def get_current_count(self):
#         """Command to retrieve the current count from CounterDevice."""
#         return self._counter_proxy.read_attribute("current_count").value


# if __name__ == "__main__":
#     # Define the server name
#     server_name = "CounterServer/01"

#     # Setup for CounterDevice
#     counter_dev_info = tango.DbDevInfo()
#     counter_dev_info.server = server_name
#     counter_dev_info._class = "CounterDevice"
#     counter_dev_info.name = "sys/counter/1"

#     # Setup for ControllerDevice
#     controller_dev_info = tango.DbDevInfo()
#     controller_dev_info.server = server_name
#     controller_dev_info._class = "ControllerDevice"
#     controller_dev_info.name = "sys/controller/1"

#     # Define the property for the ControllerDevice
#     controller_dev_info.properties = {'counter_device_name': "sys/counter/1"}

#     # Create the database and add devices
#     db = tango.Database()
#     db.add_device(counter_dev_info)
#     db.add_device(controller_dev_info)

#     # Run the device server with both classes
#     run([CounterDevice, ControllerDevice])

# import tango
# from tango import DevState, AttrWriteType, Database, DeviceProxy
# from tango.server import Device, command, attribute, run, device_property
# from threading import Thread, Event
# import time


# # Device2: Counter
# class CounterDevice(Device):
#     # Attribute: Current count value
#     current_count = attribute(dtype=int, access=AttrWriteType.READ)

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self.set_status("CounterDevice initialized and waiting for commands.")
#         self._count = 0
#         self._counting = Event()
#         self._counting.clear()

#     # Read method for current_count
#     def read_current_count(self):
#         return self._count

#     # Method to count in a separate thread
#     def _counting_loop(self):
#         while self._counting.is_set():
#             self._count += 1
#             self.push_change_event("current_count", self._count)
#             time.sleep(1)  # Increment count every second

#     @command
#     def start_counting(self):
#         """Command to start counting."""
#         if not self._counting.is_set():
#             self._counting.set()
#             self._counter_thread = Thread(target=self._counting_loop)
#             self._counter_thread.start()
#             self.info_stream("Counter started.")

#     @command
#     def stop_counting(self):
#         """Command to stop counting."""
#         if self._counting.is_set():
#             self._counting.clear()
#             self._counter_thread.join()
#             self.info_stream("Counter stopped.")

#     @command(dtype_out=int)
#     def get_count(self):
#         """Command to retrieve the current count."""
#         return self._count
    
#     @command
#     def reset_count(self):
#         """Command to reset the count to zero."""
#         self._count = 0
#         self.push_change_event("current_count", self._count)  # Notify change
#         self.info_stream("Counter reset to zero.")


# # Device1: Controller
# class ControllerDevice(Device):
#     # Device property to specify CounterDevice's device name
#     counter_device_name = device_property(dtype=str)

#     def init_device(self):
#         super().init_device()
#         self.set_state(DevState.ON)
#         self.set_status("ControllerDevice initialized and running.")
        
#         # Initialize device proxy for CounterDevice
#         if self.counter_device_name:
#             self._counter_proxy = DeviceProxy(self.counter_device_name)
#             self.info_stream("Connected to CounterDevice.")
#         else:
#             self.error_stream("CounterDevice name not set. Check counter_device_name property.")
#             self.set_status("CounterDevice name not set.")
#             self.set_state(DevState.FAULT)

#     @command
#     def start_counter(self):
#         """Command to start the counter on CounterDevice."""
#         if self._counter_proxy:
#             self._counter_proxy.command_inout("start_counting")
#         else:
#             self.error_stream("CounterDevice proxy not initialized.")

#     @command
#     def stop_counter(self):
#         """Command to stop the counter on CounterDevice."""
#         if self._counter_proxy:
#             self._counter_proxy.command_inout("stop_counting")
#         else:
#             self.error_stream("CounterDevice proxy not initialized.")

#     @command(dtype_out=int)
#     def get_current_count(self):
#         """Command to retrieve the current count from CounterDevice."""
#         if self._counter_proxy:
#             return self._counter_proxy.read_attribute("current_count").value
#         else:
#             self.error_stream("CounterDevice proxy not initialized.")
#             return -1

#     @command
#     def reset_counter(self):
#         """Command to reset the counter on CounterDevice."""
#         if self._counter_proxy:
#             self._counter_proxy.command_inout("reset_count")
#         else:
#             self.error_stream("CounterDevice proxy not initialized.")

# if __name__ == "__main__":
#     # Setup for CounterDevice
#     counter_dev_info = tango.DbDevInfo()
#     counter_dev_info.server = "CounterServer/01"
#     counter_dev_info._class = "CounterDevice"
#     counter_dev_info.name = "sys/counter/1"

#     # Setup for ControllerDevice
#     controller_dev_info = tango.DbDevInfo()
#     controller_dev_info.server = "CounterServer/01"
#     controller_dev_info._class = "ControllerDevice"
#     controller_dev_info.name = "sys/controller/1"

#     # Set device properties explicitly
#     controller_dev_info.properties = {'counter_device_name': "sys/counter/1"}

#     # Initialize Tango database and register devices
#     db = Database()
#     try:
#         db.add_device(counter_dev_info)
#         db.add_device(controller_dev_info)
#     except tango.DevFailed as e:
#         print(f"Failed to add devices to database: {e}")
#         exit(1)

#     # Run the device server with both classes
#     run([CounterDevice, ControllerDevice])
import tango
from tango import DevState, AttrWriteType, Database, DeviceProxy
from tango.server import Device, command, attribute, run, device_property
from threading import Thread, Event
import time

# Device2: Counter
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
       
        if self.get_state() == DevState.ON: 
            if not self._counting.is_set():
                self._counting.set()
                self._counter_thread = Thread(target=self._counting_loop)
                self._counter_thread.start()
                self.info_stream("Counter started.")
        

    @command
    def stop_counting(self):
        
        if self.get_state() == DevState.ON:
            if self._counting.is_set():
                self._counting.clear()
                self._counter_thread.join()
                self.info_stream("Counter stopped.")

    @command(dtype_out=int)
    def get_count(self):
        
        if self.get_state() == DevState.ON:
            return self._count
    
    @command
    def reset_count(self):
        
        if self.get_state() == DevState.ON:
            self._count = 0
            self.push_change_event("current_count", self._count)  # Notify change
            self.info_stream("Counter reset to zero.")
    
    @command
    def turn_off(self):
       
        self.stop_counting()
        self.set_state(DevState.OFF)
        self.set_status("CounterDevice is OFF.")
    @command
    def turn_on(self):
       
        self.stop_counting()
        self.set_state(DevState.ON)
        self.set_status("CounterDevice is ON.")

# Device1: Controller
class ControllerDevice(Device):
   
    counter_device_name = "sys/counter/1"

    def init_device(self):
        super().init_device()
        self.set_state(DevState.ON)
        self.set_status("ControllerDevice initialized and running.")
        
      
        if self.counter_device_name:
            self._counter_proxy = DeviceProxy(self.counter_device_name)
            self.info_stream("Connected to CounterDevice.")
        else:
            self.error_stream("CounterDevice name not set. Check counter_device_name property.")
            self.set_status("CounterDevice name not set.")
            self.set_state(DevState.FAULT)

    @command
    def start_counter(self):
        
        if self._counter_proxy:
            self._counter_proxy.command_inout("start_counting")
        else:
            self.error_stream("CounterDevice proxy not initialized.")

    @command
    def stop_counter(self):
        
        if self._counter_proxy:
            self._counter_proxy.command_inout("stop_counting")
        else:
            self.error_stream("CounterDevice proxy not initialized.")

    @command
    def turn_off_counter(self):
       
        if self._counter_proxy:
            self._counter_proxy.command_inout("turn_off")
            self.info_stream("CounterDevice turned OFF.")
        else:
            self.error_stream("CounterDevice proxy not initialized.")
    @command
    def turn_on_counter(self):
        
        if self._counter_proxy:
            self._counter_proxy.command_inout("turn_on")
            self.info_stream("CounterDevice turned ON.")
        else:
            self.error_stream("CounterDevice proxy not initialized.")

    @command(dtype_out=int)
    def get_current_count(self):
       
        if self._counter_proxy:
            return self._counter_proxy.read_attribute("current_count").value
        else:
            self.error_stream("CounterDevice proxy not initialized.")
            return -1

    @command
    def reset_counter(self):
       
        if self._counter_proxy:
            self._counter_proxy.command_inout("reset_count")
        else:
            self.error_stream("CounterDevice proxy not initialized.")

if __name__ == "__main__":
    
    counter_dev_info = tango.DbDevInfo()
    counter_dev_info.server = "CounterServer/01"
    counter_dev_info._class = "CounterDevice"
    counter_dev_info.name = "sys/counter/1"

   
    controller_dev_info = tango.DbDevInfo()
    controller_dev_info.server = "CounterServer/01"
    controller_dev_info._class = "ControllerDevice"
    controller_dev_info.name = "sys/controller/1"

   
    controller_dev_info.properties = {'counter_device_name': "sys/counter/1"}

  
    db = Database()
    try:
        db.add_device(counter_dev_info)
        db.add_device(controller_dev_info)
    except tango.DevFailed as e:
        print(f"Failed to add devices to database: {e}")
        exit(1)

   
    run([CounterDevice, ControllerDevice])





