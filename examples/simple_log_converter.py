#!/usr/bin/env python
"""
Use this to convert .can/.asc files to .log files.

Usage: simpleLogConvert.py sourceLog.asc targetLog.log
"""

import sys

import pycan.io.logger
import pycan.io.player

reader = pycan.io.player.LogReader(sys.argv[1])
writer = pycan.io.logger.Logger(sys.argv[2])

for msg in reader:
    writer.on_message_received(msg)
