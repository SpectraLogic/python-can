Configuration
=============


Usually this library is used with a particular CAN interface, this can be
specified in code, read from configuration files or environment variables.

See :func:`pycan.util.load_config` for implementation.

In Code
-------

The ``pycan`` object exposes an ``rc`` dictionary which can be used to set
the **interface** and **channel** before importing from ``pycan.interfaces``.

::

    import pycan
    pycan.rc['interface'] = 'socketcan'
    pycan.rc['channel'] = 'vcan0'
    pycan.rc['bitrate'] = 500000
    from pycan.interfaces.interface import Bus

    bus = Bus()


You can also specify the interface and channel for each Bus instance::

    import pycan

    bus = pycan.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)


Configuration File
------------------

On Linux systems the config file is searched in the following paths:

#. ``~/pycan.conf``
#. ``/etc/pycan.conf``
#. ``$HOME/.pycan``
#. ``$HOME/.pycanrc``

On Windows systems the config file is searched in the following paths:

#. ``~/pycan.conf``
#. ``pycan.ini`` (current working directory)
#. ``$APPDATA/pycan.ini``

The configuration file sets the default interface and channel:

::

    [default]
    interface = <the name of the interface to use>
    channel = <the channel to use by default>
    bitrate = <the bitrate in bits/s to use by default>


The configuration can also contain additional sections (or context):

::

    [default]
    interface = <the name of the interface to use>
    channel = <the channel to use by default>
    bitrate = <the bitrate in bits/s to use by default>

    [HS]
    # All the values from the 'default' section are inherited
    channel = <the channel to use>
    bitrate = <the bitrate in bits/s to use. i.e. 500000>

    [MS]
    # All the values from the 'default' section are inherited
    channel = <the channel to use>
    bitrate = <the bitrate in bits/s to use. i.e. 125000>


::

    from can.interfaces.interface import Bus

    hs_bus = Bus(context='HS')
    ms_bus = Bus(context='MS')

Environment Variables
---------------------

Configuration can be pulled from these environmental variables:

    * CAN_INTERFACE
    * CAN_CHANNEL
    * CAN_BITRATE


Interface Names
---------------

Lookup table of interface names:

+---------------------+-------------------------------------+
| Name                | Documentation                       |
+=====================+=====================================+
| ``"socketcan"``     | :doc:`interfaces/socketcan`         |
+---------------------+-------------------------------------+
| ``"kvaser"``        | :doc:`interfaces/kvaser`            |
+---------------------+-------------------------------------+
| ``"serial"``        | :doc:`interfaces/serial`            |
+---------------------+-------------------------------------+
| ``"slcan"``         | :doc:`interfaces/slcan`             |
+---------------------+-------------------------------------+
| ``"ixxat"``         | :doc:`interfaces/ixxat`             |
+---------------------+-------------------------------------+
| ``"pcan"``          | :doc:`interfaces/pcan`              |
+---------------------+-------------------------------------+
| ``"usb2can"``       | :doc:`interfaces/usb2can`           |
+---------------------+-------------------------------------+
| ``"nican"``         | :doc:`interfaces/nican`             |
+---------------------+-------------------------------------+
| ``"iscan"``         | :doc:`interfaces/iscan`             |
+---------------------+-------------------------------------+
| ``"neovi"``         | :doc:`interfaces/neovi`             |
+---------------------+-------------------------------------+
| ``"vector"``        | :doc:`interfaces/vector`            |
+---------------------+-------------------------------------+
| ``"virtual"``       | :doc:`interfaces/virtual`           |
+---------------------+-------------------------------------+
| ``"canalystii"``    | :doc:`interfaces/canalystii`        |
+---------------------+-------------------------------------+
| ``"systec"``        | :doc:`interfaces/systec`            |
+---------------------+-------------------------------------+
