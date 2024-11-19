import tango
from tango import DevState, AttrWriteType, Database, DeviceProxy
from tango.server import Device, attribute, run, command, device_property
from tango.server import DevFailed  # type:ignore


class CentralController(Device):

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.ON)
        self.is_subarray_assigned: list[bool] = [False, False]
        self.no_of_dish: list[int] = [0, 0]
        self.subarray_proxy_dict: dict[str, DeviceProxy] = {}

    @command
    def on(self):
        self.set_state(DevState.ON)
        self.set_status("CentralController is ON")

    @command
    def off(self):
        self.set_state(DevState.OFF)
        self.set_status("CentralController is OFF")

    #   Add command for unallocating dishes from subarray

    @command(dtype_in=([int]), dtype_out=str)
    def assign_dishes_to_subarray(self, subarray_dish_nos: list[int]):
        subarray_no = subarray_dish_nos[0]
        subarray_dish_nos = subarray_dish_nos[1:]
        out = ""
        if subarray_no == 1 or subarray_no == 2:
            self.subarray_proxy_dict[f"sub/dev/{subarray_no}"] = DeviceProxy(
                f"sub/dev/{subarray_no}"
            )
            self.subarray_proxy_dict[f"sub/dev/{subarray_no}"].command_inout(
                "assign_dish", subarray_dish_nos
            )
            self.no_of_dish[subarray_no - 1] = len(subarray_dish_nos)
            self.is_subarray_assigned[subarray_no - 1] = True
            out = f"Subarray {subarray_no} has been successfully assigned dishes {subarray_dish_nos}"
        else:
            self.error_stream(
                "There are 2 subarrays. Please give first argument as 1 or 2"
            )
            out = "There are 2 subarrays. Please give first argument as 1 or 2"
        return out

    @command(dtype_in=int, dtype_out="DevVarStringArray")
    def get_assigned_dish_to_subarray(self, subarray_no):
        assigned_dishes = []
        if subarray_no >= 1 and subarray_no <= 2:
            if self.is_subarray_assigned[subarray_no - 1] == True:
                assigned_dishes.append(
                    f"Subarray {subarray_no} currently is assigned with these dishes"
                )
                assigned_dishes += self.subarray_proxy_dict[
                    f"sub/dev/{subarray_no}"
                ].command_inout("get_assigned_dish")
            else:
                assigned_dishes.append(
                    f"No dishes assigned currently to subarray {subarray_no}"
                )
        else:
            self.error_stream(
                "There are two subarrays. Kindly enter the argument as 1 or 2"
            )
            assigned_dishes.append(
                "There are two subarrays. Kindly enter the argument as 1 or 2"
            )
        return assigned_dishes

    @command(dtype_in=(float, float))
    def subarray_move_to_target(self, subarray_no__degrees):
        """Send a move command to all DishDevices in the subarray."""
        results = []
        subarray_no = int(subarray_no__degrees[0])
        degrees = subarray_no__degrees[1]
        self.subarray_proxy_dict[f"sub/dev/{subarray_no}"].command_inout(
            "group_move_to_target", degrees
        )

    @command(dtype_in=(float, float))
    def subarray_write_target_position(self, subarray_no__target_position):
        """Set the target position on all DishDevices in the subarray."""
        results = []
        subarray_no = int(subarray_no__target_position[0])
        target_position = subarray_no__target_position[1]
        self.subarray_proxy_dict[f"sub/dev/{subarray_no}"].command_inout(
            "group_write_target_position", target_position
        )

    @command(dtype_in=int, dtype_out="DevVarStringArray")
    def read_subarray_antenna_position(self, subarray_no):
        """Read current antenna positions from all linked Servo devices and log in info_stream."""
        antenna_positions = []
        antenna_positions = self.subarray_proxy_dict[
            f"sub/dev/{subarray_no}"
        ].command_inout("read_group_antenna_position")
        return antenna_positions

    @command(dtype_in=int, dtype_out="DevVarStringArray")
    def read_subarray_target_position(self, subarray_no):
        """Read target positions from all linked Servo devices and log in info_stream."""
        target_positions = []
        target_positions = self.subarray_proxy_dict[
            f"sub/dev/{subarray_no}"
        ].command_inout("read_group_target_position")
        return target_positions

    @command(dtype_in=(float, float, float, float))
    def set_subarr_attn(self, subarray_dish_channel_attn):
        try:
            if len(subarray_dish_channel_attn) != 4:
                raise DevFailed(
                    "Improper input, Please Provide subarray no,dish no,channel no,attenuation"
                )
            else:
                subarray_no = int(subarray_dish_channel_attn[0])
                dish_channel_attn = subarray_dish_channel_attn[1:]
                self.subarray_proxy_dict[f"sub/dev/{subarray_no}"].command_inout(
                    "set_dish_attn", dish_channel_attn
                )

        except DevFailed as e:
            self.error_stream(
                "Improper input, Please Provide subarray no,dish no,channel no,attenuation"
            )

    @command(dtype_in=(int, int), dtype_out=(float, float))
    def get_subarr_attn(self, subarray_no__dish_no):
        subarray_no = subarray_no__dish_no[0]
        dish_no = subarray_no__dish_no[1]
        subarray_p: DeviceProxy = self.subarray_proxy_dict[f"sub/dev/{subarray_no}"]
        return subarray_p.command_inout("get_dish_attn", dish_no)
