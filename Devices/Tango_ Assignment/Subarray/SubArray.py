import tango 
from tango import DevState, AttrWriteType, Database, DeviceProxy
from tango.server import Device, attribute, run, command, device_property
from tango.server import DevFailed  
from tango import EventType


class SubArray(Device):

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.ON)
        self.is_dish_assigned: bool = False
        self.no_of_dish: int = 0
        self.dish_proxy_dict: dict[str, DeviceProxy] = {}
        self.dish_events = [
            dish_d.subscribe_event(
                "PositionAchieved",
                EventType.CHANGE_EVENT,
                self.handle_dish_position_achived_event,
            )
            for dish_d in self.dish_proxy_dict.values()
        ]
        self.log = ""

    def handle_dish_position_achived_event(self, event):
        if not event.err and not event.attr_value.value:
            self.set_status(
                self.get_status()
                + "\n"
                + f"Dish: {event.device} has reached the desired position"
            )
            self.info_stream("Dish is at desired position")
        elif event.err:
            self.error_stream("Error in receiving event from child device.")

    @command
    def on(self):
        self.set_state(DevState.ON)
        self.set_status(self.get_status() + "\n" + "Subarry is ON")

    @command
    def off(self):
        self.set_state(DevState.OFF)
        self.set_status(self.get_status() + "\n" + "Subarry is OFF")

    @command(dtype_in=[int])
    def assign_dish(self, dish_nos: list[int]):

        for i in dish_nos:
            self.dish_proxy_dict[f"dd/dev/{i}"] = DeviceProxy(f"dd/dev/{i}")
        self.no_of_dish = len(dish_nos)
        self.is_dish_assigned = True

    @command(dtype_in=float)
    def group_move_to_target(self, degrees):
        """Send a move command to all DishDevices in the group."""
        results = []
        for dish_device, dish_proxy in self.dish_proxy_dict.items():
            try:
                result = dish_proxy.command_inout("MoveToTarget", degrees)
                results.append((dish_device, result))
            except Exception as e:
                self.error_stream(f"Failed to move {dish_device}: {e}")
                results.append((dish_device, "Failed"))

        for dish_device, status in results:
            if status == "Failed":
                self.error_stream(f"Failed to move {dish_device}")
            else:
                self.info_stream(f"Dish {dish_device} moved by {degrees} degrees.")

    @command(dtype_in=float)
    def group_write_target_position(self, target_position):
        """Set the target position on all DishDevices in the group."""
        results = []
        for dish_device, dish_proxy in self.dish_proxy_dict.items():
            try:
                result = dish_proxy.command_inout(
                    "WriteTargetPosition", target_position
                )
                results.append((dish_device, result))
            except Exception as e:
                self.error_stream(
                    f"Failed to write TargetPosition to {dish_device}: {e}"
                )
                results.append((dish_device, "Failed"))

        for dish_device, status in results:
            if status == "Failed":
                self.error_stream(f"Failed to set TargetPosition for {dish_device}")
            else:
                self.info_stream(
                    f"Set TargetPosition for Dish {dish_device} to {target_position}."
                )

    @command(dtype_out="DevVarStringArray")
    def read_group_antenna_position(self):
        """Read current antenna positions from all linked Servo devices and log in info_stream."""
        antenna_positions = []
        for dish_device_name, dish_proxy in self.dish_proxy_dict.items():
            # Retrieve servo device name from the dish device number
            servo_device_name = f"servo/dev/{dish_device_name.split('/')[-1]}"
            try:
                # Create a proxy to the servo device
                servo_proxy = DeviceProxy(servo_device_name)
                # Read the current antenna position from the servo device's attribute
                antenna_position = servo_proxy.read_attribute("AntennaPosition").value
                position_info = (
                    f"Antenna Position for {dish_device_name}: {antenna_position}"
                )
                antenna_positions.append(position_info)
                self.info_stream(position_info)
            except tango.DevFailed as e:
                error_info = (
                    f"Failed to read AntennaPosition from {servo_device_name}: {e}"
                )
                antenna_positions.append(error_info)
                self.error_stream(error_info)

        return antenna_positions

    @command(dtype_out="DevVarStringArray")
    def read_group_target_position(self):
        """Read target positions from all linked Servo devices and log in info_stream."""
        target_positions = []
        for dish_device_name, dish_proxy in self.dish_proxy_dict.items():
            # Retrieve servo device name from the dish device number
            servo_device_name = f"servo/dev/{dish_device_name.split('/')[-1]}"
            try:
                # Create a proxy to the servo device
                servo_proxy = DeviceProxy(servo_device_name)
                # Read the target position from the servo device's attribute
                target_position = servo_proxy.read_attribute("TargetPosition").value
                position_info = (
                    f"Target Position for {dish_device_name}: {target_position}"
                )
                target_positions.append(position_info)
                self.info_stream(position_info)
            except tango.DevFailed as e:
                error_info = (
                    f"Failed to read TargetPosition from {servo_device_name}: {e}"
                )
                target_positions.append(error_info)
                self.error_stream(error_info)

        return target_positions

    @command(dtype_in=(float, float, float))
    def set_dish_attn(self, dish_channel_attn):
        try:
            if len(dish_channel_attn) != 3:
                raise DevFailed(
                    "Improper input, Please Provide dish no,channel no,attenuation"
                )
            else:
                dish_no, channel, attn = dish_channel_attn
                if channel == 1:
                    self.dish_proxy_dict[f"dd/dev/{int(dish_no)}"].command_inout(
                        "set_chn1_attn_FrontEnd", (attn)
                    )
                elif channel == 2:
                    self.dish_proxy_dict[f"dd/dev/{int(dish_no)}"].command_inout(
                        "set_chn2_attn_FrontEnd", (attn)
                    )
                else:
                    raise DevFailed("Channel not defined")

        except DevFailed as e:
            self.error_stream(
                "Improper input, Please Provide dish no,channel no,attenuation"
            )

    @command(dtype_in=int, dtype_out=(float, float))
    def get_dish_attn(self, dish_no):
        dish_p: DeviceProxy = self.dish_proxy_dict[f"dd/dev/{dish_no}"]
        return dish_p.command_inout("get_channel_attn")
    
    @command(dtype_out="DevVarStringArray")
    def get_assigned_dish(self):
        assigned_dishes=[]
        if(self.is_dish_assigned==True):
            for i in self.dish_proxy_dict.keys():
                assigned_dishes.append(f"Dish {i.split('/')[-1]}")
        else:
            assigned_dishes.append("No dishes assigned currently to this subarray")
        return assigned_dishes
