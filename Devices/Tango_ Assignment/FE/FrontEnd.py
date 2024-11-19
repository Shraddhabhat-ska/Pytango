import tango 
from tango import DevState, AttrWriteType, Database, DeviceProxy
from tango.server import Device, attribute, run, command, device_property, pipe
from tango.server import DevFailed  # type:ignore
from tango import EventType



class FrontEnd(Device):
    """A Front End Device is a part of Feed which collects the signal and does some processing"""

    def init_device(self):
        Device.init_device(self)
        self._chn1_attn = 0.0
        self._chn2_attn = 0.0
        self.set_state(DevState.ON)

    chn1_attn = attribute(
        name="channel1Attn",
        label="channel 1 Attunation",
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        unit="dB",
        min_value=0.0,
        max_value=50.0,
        fget="read_chn1_attn",
        fset="write_chn1_attn",
    )
    chn2_attn = attribute(
        name="channel2Attn",
        label="channel 2 Attunation",
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        unit="dB",
        min_value=0.0,
        max_value=50.0,
        fget="read_chn2_attn",
        fset="write_chn2_attn",
    )

    def read_chn1_attn(self):
        """Read channel 1 attenuation"""
        return self._chn1_attn

    def write_chn1_attn(self, value):
        """Write value to channel 1 attenuation"""
        if value < 0.0 or value > 50.0:
            raise DevFailed("Attenuation value out of range. Must be between 0 and 50")

        self._chn1_attn = value
        self.set_status(f"Channel 1 attunation value set to {value}")

    def read_chn2_attn(self):
        """Read Channel 2 attenuation"""
        return self._chn2_attn

    def write_chn2_attn(self, value):
        """Write value to channel 2 attenuation"""
        if value < 0.0 or value > 50.0:
            raise DevFailed("Attenuation value out of range. Must be between 0 and 50")

        self._chn2_attn = value
        self.set_status(f"Channel 2 attunation value set to {value}")

    @pipe()
    def channel_status(self):
        """pipe"""
        return {
            "ch1_attenuation": self._chn1_attn,
            "ch2_attenuation": self._chn2_attn,
        }

    @command()
    def on(self):
        """Turns On Front end Device"""
        self.set_state(DevState.ON)

    @command
    def off(self):
        """Turns off Front end Device"""
        self.set_state(DevState.OFF)

    @command(dtype_out=str)
    def get_dev_status(self):
        """Returns device status"""

        return self.get_status()

    @command(dtype_out=str)
    def get_dev_state(self):
        """Returns device state"""
        return self.get_state()

    @command(dtype_in=(float, float))
    def set_single_chn_attn(self, inp):
        channel_id, attn_value = inp
        if channel_id == 1:
            self.write_chn1_attn(attn_value)
        else:
            self.write_chn2_attn(attn_value)

    @command(dtype_in="DevVarLongArray")
    def set_both_chn_attn(self, inp):
        if len(inp) != 2:
            raise DevFailed("Enter 2 values for 2 channels")
        self.write_chn1_attn(inp[0])
        self.write_chn2_attn(inp[1])
