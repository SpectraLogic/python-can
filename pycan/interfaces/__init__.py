"""
Interfaces contain low level implementations that interact with CAN hardware.
"""

import warnings
from pkg_resources import iter_entry_points


# interface_name => (module, classname)
BACKENDS = {
    'kvaser':           ('pycan.interfaces.kvaser',           'KvaserBus'),
    'socketcan':        ('pycan.interfaces.socketcan',        'SocketcanBus'),
    'serial':           ('pycan.interfaces.serial.serial_can','SerialBus'),
    'pcan':             ('pycan.interfaces.pcan',             'PcanBus'),
    'usb2can':          ('pycan.interfaces.usb2can',          'Usb2canBus'),
    'ixxat':            ('pycan.interfaces.ixxat',            'IXXATBus'),
    'nican':            ('pycan.interfaces.nican',            'NicanBus'),
    'iscan':            ('pycan.interfaces.iscan',            'IscanBus'),
    'virtual':          ('pycan.interfaces.virtual',          'VirtualBus'),
    'neovi':            ('pycan.interfaces.ics_neovi',        'NeoViBus'),
    'vector':           ('pycan.interfaces.vector',           'VectorBus'),
    'slcan':            ('pycan.interfaces.slcan',            'slcanBus'),
    'canalystii':       ('pycan.interfaces.canalystii',       'CANalystIIBus'),
    'systec':           ('pycan.interfaces.systec',           'UcanBus')
}

BACKENDS.update({
    interface.name: (interface.module_name, interface.attrs[0])
    for interface in iter_entry_points('pycan.interface')
})

# Old entry point name. May be removed >3.0.
for interface in iter_entry_points('python_can.interface'):
    BACKENDS[interface.name] = (interface.module_name, interface.attrs[0])
    warnings.warn('{} is using the deprecated python_can.interface entry point. '.format(interface.name) +
                  'Please change to pycan.interface instead.', DeprecationWarning)

VALID_INTERFACES = frozenset(list(BACKENDS.keys()) + ['socketcan_native', 'socketcan_ctypes'])
