#!/usr/bin/env python
from __future__ import absolute_import, print_function

import unittest
import random
import logging
import tempfile
import os
from os.path import join, dirname

import pycan

from .data.example_data import generate_message

channel = 'virtual_channel_0'
pycan.rc['interface'] = 'virtual'

logging.basicConfig(level=logging.DEBUG)

# makes the random number generator deterministic
random.seed(13339115)


class ListenerImportTest(unittest.TestCase):

    def testClassesImportable(self):
        self.assertTrue(hasattr(pycan, 'Listener'))
        self.assertTrue(hasattr(pycan, 'BufferedReader'))
        self.assertTrue(hasattr(pycan, 'Notifier'))
        self.assertTrue(hasattr(pycan, 'Logger'))

        self.assertTrue(hasattr(pycan, 'ASCWriter'))
        self.assertTrue(hasattr(pycan, 'ASCReader'))

        self.assertTrue(hasattr(pycan, 'BLFReader'))
        self.assertTrue(hasattr(pycan, 'BLFWriter'))

        self.assertTrue(hasattr(pycan, 'CSVReader'))
        self.assertTrue(hasattr(pycan, 'CSVWriter'))

        self.assertTrue(hasattr(pycan, 'CanutilsLogWriter'))
        self.assertTrue(hasattr(pycan, 'CanutilsLogReader'))

        self.assertTrue(hasattr(pycan, 'SqliteReader'))
        self.assertTrue(hasattr(pycan, 'SqliteWriter'))

        self.assertTrue(hasattr(pycan, 'Printer'))

        self.assertTrue(hasattr(pycan, 'LogReader'))

        self.assertTrue(hasattr(pycan, 'MessageSync'))


class BusTest(unittest.TestCase):

    def setUp(self):
        self.bus = pycan.interface.Bus()

    def tearDown(self):
        self.bus.shutdown()


class ListenerTest(BusTest):

    def testBasicListenerCanBeAddedToNotifier(self):
        a_listener = pycan.Printer()
        notifier = pycan.Notifier(self.bus, [a_listener], 0.1)
        notifier.stop()
        self.assertIn(a_listener, notifier.listeners)

    def testAddListenerToNotifier(self):
        a_listener = pycan.Printer()
        notifier = pycan.Notifier(self.bus, [], 0.1)
        notifier.stop()
        self.assertNotIn(a_listener, notifier.listeners)
        notifier.add_listener(a_listener)
        self.assertIn(a_listener, notifier.listeners)

    def testRemoveListenerFromNotifier(self):
        a_listener = pycan.Printer()
        notifier = pycan.Notifier(self.bus, [a_listener], 0.1)
        notifier.stop()
        self.assertIn(a_listener, notifier.listeners)
        notifier.remove_listener(a_listener)
        self.assertNotIn(a_listener, notifier.listeners)

    def testPlayerTypeResolution(self):
        def test_filetype_to_instance(extension, klass):
            print("testing: {}".format(extension))
            try:
                if extension == ".blf":
                    delete = False
                    file_handler = open(join(dirname(__file__), "data/logfile.blf"))
                else:
                    delete = True
                    file_handler = tempfile.NamedTemporaryFile(suffix=extension, delete=False)

                with file_handler as my_file:
                    filename = my_file.name
                with pycan.LogReader(filename) as reader:
                    self.assertIsInstance(reader, klass)
            finally:
                if delete:
                    os.remove(filename)

        test_filetype_to_instance(".asc", pycan.ASCReader)
        test_filetype_to_instance(".blf", pycan.BLFReader)
        test_filetype_to_instance(".csv", pycan.CSVReader)
        test_filetype_to_instance(".db" , pycan.SqliteReader)
        test_filetype_to_instance(".log", pycan.CanutilsLogReader)

        # test file extensions that are not supported
        with self.assertRaisesRegexp(NotImplementedError, ".xyz_42"):
            test_filetype_to_instance(".xyz_42", pycan.Printer)

    def testLoggerTypeResolution(self):
        def test_filetype_to_instance(extension, klass):
            print("testing: {}".format(extension))
            try:
                with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as my_file:
                    filename = my_file.name
                with pycan.Logger(filename) as writer:
                    self.assertIsInstance(writer, klass)
            finally:
                os.remove(filename)

        test_filetype_to_instance(".asc", pycan.ASCWriter)
        test_filetype_to_instance(".blf", pycan.BLFWriter)
        test_filetype_to_instance(".csv", pycan.CSVWriter)
        test_filetype_to_instance(".db" , pycan.SqliteWriter)
        test_filetype_to_instance(".log", pycan.CanutilsLogWriter)
        test_filetype_to_instance(".txt", pycan.Printer)

        # test file extensions that should use a fallback
        test_filetype_to_instance("", pycan.Printer)
        test_filetype_to_instance(".", pycan.Printer)
        test_filetype_to_instance(".some_unknown_extention_42", pycan.Printer)
        with pycan.Logger(None) as logger:
            self.assertIsInstance(logger, pycan.Printer)

    def testBufferedListenerReceives(self):
        a_listener = pycan.BufferedReader()
        a_listener(generate_message(0xDADADA))
        a_listener(generate_message(0xDADADA))
        self.assertIsNotNone(a_listener.get_message(0.1))
        a_listener.stop()
        self.assertIsNotNone(a_listener.get_message(0.1))


if __name__ == '__main__':
    unittest.main()
