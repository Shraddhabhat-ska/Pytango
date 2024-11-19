from tango import AttrWriteType, DevFloat, DeviceProxy, EventType
from tango.server import Device, attribute, command


class TemperatureDevice(Device):
    # Attributes
    Temperature = attribute(
        dtype=DevFloat,                # Data type of the attribute
        access=AttrWriteType.READ,     # Read-only attribute
        label="Temperature",           # Label displayed in the client
        unit="°C",                     # Unit of the attribute
        format="%.2f",                 # Format for the value display
        doc="Current temperature",     # Documentation for the attribute
        abs_change=2.0                 # Absolute change threshold
    )

    def init_device(self):
        super().init_device()
        self.set_change_event("Temperature", True)  # Enable change events for Temperature
        self._temperature = 25.0  # Initialize temperature value
        self.event_id = None  # Placeholder for the subscription ID
        self.device_proxy = DeviceProxy(self.get_name())  # Persistent proxy for subscriptions

    # Attribute read method
    def read_Temperature(self):
        """Read method for the Temperature attribute."""
        return self._temperature

    # Commands
    @command(dtype_in=DevFloat, doc_in="New temperature value", 
             dtype_out=str, doc_out="Status message")
    def UpdateTemperature(self, new_value):
        """
        Simulate updating the current temperature.
        Push a change event if the new value differs enough.
        """
        self._temperature = new_value
        self.push_change_event("Temperature", new_value)  # Notify clients
        return f"Temperature updated to {new_value}°C"

    @command(dtype_out=str, doc_out="Subscription status message")
    def SubscribeToTemperatureEvents(self):
        """
        Subscribe to the Temperature change events of this device.
        """
        if self.event_id is not None:
            return "Already subscribed to events."

        def callback(event):
            if event.err:
                self.error_stream(f"Event error: {event.errors}")
            else:
                value = event.attr_value.value
                # Set the device status to the new temperature value
                self.set_status(f"Temperature changed to {value}°C")
                self.info_stream(f"Event received: Temperature = {value}°C")

        # Subscribe to the change events using the persistent proxy
        self.event_id = self.device_proxy.subscribe_event(
            "Temperature", EventType.CHANGE_EVENT, callback
        )
        return "Successfully subscribed to Temperature change events."

    @command(dtype_out=str, doc_out="Unsubscription status message")
    def UnsubscribeFromTemperatureEvents(self):
        """
        Unsubscribe from the Temperature change events of this device.
        """
        if self.event_id is None:
            return "No active subscription to unsubscribe from."

        # Unsubscribe using the stored event_id and persistent proxy
        try:
            self.device_proxy.unsubscribe_event(self.event_id)
            self.event_id = None
            return "Successfully unsubscribed from Temperature change events."
        except KeyError as e:
            self.error_stream(f"Unsubscribe error: {e}")
            return f"Error while unsubscribing: {str(e)}"


# Run the server
if __name__ == "__main__":
    from tango.server import run
    run([TemperatureDevice])
