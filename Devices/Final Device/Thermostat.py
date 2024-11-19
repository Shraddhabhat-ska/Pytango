import tango
from tango.server import Device, command, attribute, run, pipe
from tango import AttrWriteType, DevState

class Thermostat(Device):
    def init_device(self):
        super().init_device()
        self._current_temp = 20  # Initial current temperature
        self._target_temp = 22    # Initial target temperature
        self.set_state(DevState.ON)
        self.set_status("Thermostat initialized and running.")

        # Set up change event for current_temperature with a tolerance of 0.1
        self.set_change_event("current_temperature", True, False)
        self.set_archive_event("current_temperature", True, False)

    @attribute(dtype=float, access=AttrWriteType.READ)
    def current_temperature(self):
        return self._current_temp

    @attribute(dtype=float, access=AttrWriteType.READ_WRITE)
    def target_temperature(self):
        return self._target_temp

    @target_temperature.write
    def target_temperature(self, value):
        self._target_temp = value

    @command(dtype_out=str)
    def adjust_temperature(self):
        if self._current_temp < self._target_temp:
            self._current_temp += 1  # Heat up by 1 degree
        elif self._current_temp > self._target_temp:
            self._current_temp -= 1  # Cool down by 1 degree
        else:
            return "Temperature is stable"

        # Notify Tango of the temperature change by pushing the change event
        self.push_change_event("current_temperature", self._current_temp)

        return f"Adjusted to: {self._current_temp}"



if __name__ == "__main__":
    dev_info = tango.DbDevInfo()
    dev_info.server = "Thermostat/01"
    dev_info._class = "Thermostat"
    dev_info.name = "dev/test/01"
    host = "localhost"
    port = "10000"
    db = tango.Database(host, port)
    db.add_device(dev_info)

    run([Thermostat])

