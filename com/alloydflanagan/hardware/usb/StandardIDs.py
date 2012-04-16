# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

#Copyright 2012 A. Lloyd Flanagan
#This file is part of USBProbe.

#USBProbe is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#USBProbe is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with USBProbe.  If not, see <http://www.gnu.org/licenses/>.
import re

"""
Created on Mar 18, 2012

@author: A. Lloyd Flanagan
"""


class DeviceEntry(object):
    """
    Simple helper class to represent a device entry in usb.ids.txt file.
    """
    def __init__(self, device_name, device_code):
        self.name = device_name
        self.code = device_code

    def __str__(self):
        result = '    Device: %s (%s)' % (self.name, self.code)
        return result


class VendorEntry(object):
    """
    Simple helper class to represent a vendor entry in usb.ids.txt file, and
    collect its devices.
    """

    def __init__(self, vendor_code, vendor_name):
        self.name = vendor_name
        self.code = vendor_code
        self.devices = {}

    def add_dev(self, device_code, device_name):
        self.devices[device_code] = DeviceEntry(device_name, device_code)

    def __str__(self):
        result = 'Vendor: %s (%s)' % (self.name, self.code)
        for key in self.devices:
            result += '\n   ' + str(self.devices[key])
        return result


class USBStdVendors(object):
    """
    A class to wrap the usb.ids.txt file (from linux) and allow it to act as a
    searchable dictionary.

    """

    #TODO: provide option to download new IDs list from http://www.linux-
    #usb.org/usb.ids
    def __init__(self, fname):
        """
        Create a new USB standard IDs list. If fname is a valid file name, will
        parse the file and provide the contents in a searchable format.

        """
        vendor_id_line = re.compile(r'^([0-9a-fA-F]+)\s+(.*)$')
        device_line = re.compile(r'^\t([0-9a-fA-F]+)\s+(.*)$')
        self._vendors = {}
        current_vendor = ''
        if fname:
            with open(fname, 'r') as id_file:
                for line in id_file:
                    if line.endswith('\n'):
                        line = line[:-1]
                    if not line or line.startswith('#'):
                        continue
                    m = vendor_id_line.match(line)
                    if m:
                        current_vendor = m.groups()[0]
                        self._vendors[current_vendor] = VendorEntry(
                                                            *m.groups())
                    else:
                        m = device_line.match(line)
                        if m:
                            self._vendors[current_vendor].add_dev(*m.groups())
                        else:
                            if '# List of known device class' in line:
                                return
                            else:
                                print('UNMATCHED: %s' % line)

    def __str__(self):
        result = ''
        for v in self._vendors:
            result += '\n' + str(self._vendors[v])
        return result

if __name__ == '__main__':
    import os
    data_file = '../../../../../../data/usb.ids.txt'
    print(os.path.realpath(data_file))
    x = USBStdVendors(data_file)
    print(x)
