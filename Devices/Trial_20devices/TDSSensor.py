#!/usr/bin/env python
# -*- coding:utf-8 -*-


# ############################################################################
#  license :
# ============================================================================
#
#  File :        TDSSensor.py
#
#  Project :     tds sensor
#
# This file is part of Tango device class.
# 
# Tango is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Tango is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Tango.  If not, see <http://www.gnu.org/licenses/>.
# 
#
#  $Author :      shraddhabhat.ska$
#
#  $Revision :    $
#
#  $Date :        $
#
#  $HeadUrl :     $
# ============================================================================
#            This file is generated by POGO
#     (Program Obviously used to Generate tango Object)
# ############################################################################

__all__ = ["TDSSensor", "TDSSensorClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(TDSSensor.additionnal_import) ENABLED START -----#

#----- PROTECTED REGION END -----#	//	TDSSensor.additionnal_import

# Device States Description
# No states for this device


class TDSSensor (PyTango.LatestDeviceImpl):
    """dummy tds sensor"""
    
    # -------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(TDSSensor.global_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	TDSSensor.global_variables

    def __init__(self, cl, name):
        PyTango.LatestDeviceImpl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        TDSSensor.init_device(self)
        #----- PROTECTED REGION ID(TDSSensor.__init__) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(TDSSensor.delete_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_current_tds_read = 0.0
        self.attr_temperature_read = 0.0
        self.attr_max_tds_threshold_read = 0.0
        #----- PROTECTED REGION ID(TDSSensor.init_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(TDSSensor.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.always_executed_hook

    # -------------------------------------------------------------------------
    #    TDSSensor read/write attribute methods
    # -------------------------------------------------------------------------
    
    def read_current_tds(self, attr):
        self.debug_stream("In read_current_tds()")
        #----- PROTECTED REGION ID(TDSSensor.current_tds_read) ENABLED START -----#
        attr.set_value(self.attr_current_tds_read)
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.current_tds_read
        
    def read_temperature(self, attr):
        self.debug_stream("In read_temperature()")
        #----- PROTECTED REGION ID(TDSSensor.temperature_read) ENABLED START -----#
        attr.set_value(self.attr_temperature_read)
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.temperature_read
        
    def read_max_tds_threshold(self, attr):
        self.debug_stream("In read_max_tds_threshold()")
        #----- PROTECTED REGION ID(TDSSensor.max_tds_threshold_read) ENABLED START -----#
        attr.set_value(self.attr_max_tds_threshold_read)
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.max_tds_threshold_read
        
    def write_max_tds_threshold(self, attr):
        self.debug_stream("In write_max_tds_threshold()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(TDSSensor.max_tds_threshold_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.max_tds_threshold_write
        
    
    
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(TDSSensor.read_attr_hardware) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.read_attr_hardware


    # -------------------------------------------------------------------------
    #    TDSSensor command methods
    # -------------------------------------------------------------------------
    
    def calibrate(self):
        """ 
        """
        self.debug_stream("In calibrate()")
        #----- PROTECTED REGION ID(TDSSensor.calibrate) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.calibrate
        
    def get_tds(self):
        """ 
        :rtype: PyTango.DevFloat
        """
        self.debug_stream("In get_tds()")
        argout = 0.0
        #----- PROTECTED REGION ID(TDSSensor.get_tds) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.get_tds
        return argout
        

    #----- PROTECTED REGION ID(TDSSensor.programmer_methods) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	TDSSensor.programmer_methods

class TDSSensorClass(PyTango.DeviceClass):
    # -------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(TDSSensor.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	TDSSensor.global_class_variables


    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        'calibrate':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'get_tds':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevFloat, "none"]],
        }


    #    Attribute definitions
    attr_list = {
        'current_tds':
            [[PyTango.DevFloat,
            PyTango.SCALAR,
            PyTango.READ]],
        'temperature':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ]],
        'max_tds_threshold':
            [[PyTango.DevFloat,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(TDSSensorClass, TDSSensor, 'TDSSensor')
        #----- PROTECTED REGION ID(TDSSensor.add_classes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	TDSSensor.add_classes

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed as e:
        print ('-------> Received a DevFailed exception:', e)
    except Exception as e:
        print ('-------> An unforeseen exception occured....', e)

if __name__ == '__main__':
    main()
