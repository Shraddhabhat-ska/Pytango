import tango
import random
from time import sleep
from tango.server import Device, attribute, command,run
from tango import AttrWriteType

class PHSensor(Device):
    def init_device(self):
        super().init_device()
        self._ph = 7.0  
        self._updating = False  
        self.set_change_event("ph", True, False)
        self.set_archive_event("ph", True, False)

    @attribute(dtype=float, access=AttrWriteType.READ)
    def ph(self):
        
        return self._ph

    def _simulate_ph(self):
                   
        self._ph += random.uniform(-0.05, 0.05)
        self._ph = max(6.5, min(self._ph, 7.5)) 
        self.push_change_event("ph", self._ph)
       
        sleep(1)

    @command
    def start_updating(self):
        
        if not self._updating:
            self._updating = True
            self.info_stream("pH level simulation started.")
            self._simulate_ph()

    @command
    def stop_updating(self):
      
        if self._updating:
            self._updating = False
            self.info_stream("pH level simulation stopped.")

if __name__ == "__main__":
    
    
    dev_info = tango.DbDevInfo()
    dev_info.server = "PHSensor/01"
    dev_info._class = "PHSensor"
    dev_info.name = "dev/test/01"
    host="localhost"
    port = "10000"
    db = tango.Database(host,port)
    db.add_device(dev_info)

    run([PHSensor])