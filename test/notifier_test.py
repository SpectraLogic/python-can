#!/usr/bin/env python
import unittest
import time
try:
    import asyncio
except ImportError:
    asyncio = None

import pycan


class NotifierTest(unittest.TestCase):

    def test_single_bus(self):
        bus = pycan.Bus('test', bustype='virtual', receive_own_messages=True)
        reader = pycan.BufferedReader()
        notifier = pycan.Notifier(bus, [reader], 0.1)
        msg = pycan.Message()
        bus.send(msg)
        self.assertIsNotNone(reader.get_message(1))
        notifier.stop()
        bus.shutdown()

    def test_multiple_bus(self):
        bus1 = pycan.Bus(0, bustype='virtual', receive_own_messages=True)
        bus2 = pycan.Bus(1, bustype='virtual', receive_own_messages=True)
        reader = pycan.BufferedReader()
        notifier = pycan.Notifier([bus1, bus2], [reader], 0.1)
        msg = pycan.Message()
        bus1.send(msg)
        time.sleep(0.1)
        bus2.send(msg)
        recv_msg = reader.get_message(1)
        self.assertIsNotNone(recv_msg)
        self.assertEqual(recv_msg.channel, 0)
        recv_msg = reader.get_message(1)
        self.assertIsNotNone(recv_msg)
        self.assertEqual(recv_msg.channel, 1)
        notifier.stop()
        bus1.shutdown()
        bus2.shutdown()


class AsyncNotifierTest(unittest.TestCase):

    @unittest.skipIf(asyncio is None, 'Test requires asyncio')
    def test_asyncio_notifier(self):
        loop = asyncio.get_event_loop()
        bus = pycan.Bus('test', bustype='virtual', receive_own_messages=True)
        reader = pycan.AsyncBufferedReader()
        notifier = pycan.Notifier(bus, [reader], 0.1, loop=loop)
        msg = pycan.Message()
        bus.send(msg)
        future = asyncio.wait_for(reader.get_message(), 1.0)
        recv_msg = loop.run_until_complete(future)
        self.assertIsNotNone(recv_msg)
        notifier.stop()
        bus.shutdown()


if __name__ == '__main__':
    unittest.main()
