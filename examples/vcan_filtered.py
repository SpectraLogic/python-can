#!/usr/bin/env python
"""
This shows how message filtering works.
"""

import time

import pycan

if __name__ == '__main__':
    bus = pycan.interface.Bus(bustype='socketcan',
                              channel='vcan0',
                              receive_own_messages=True)

    can_filters = [{"can_id": 1, "can_mask": 0xf, "extended": True}]
    bus.set_filters(can_filters)
    notifier = pycan.Notifier(bus, [pycan.Printer()])
    bus.send(pycan.Message(arbitration_id=1, is_extended_id=True))
    bus.send(pycan.Message(arbitration_id=2, is_extended_id=True))
    bus.send(pycan.Message(arbitration_id=1, is_extended_id=False))

    time.sleep(10)
