Library API
===========

The main objects are the :class:`~pycan.BusABC` and the :class:`~pycan.Message`.
A form of CAN interface is also required.

.. hint::

    Check the backend specific documentation for any implementation specific details.


.. toctree::
   :maxdepth: 1
   
   bus
   message
   listeners
   asyncio
   bcm
   internal-api


Utilities
---------


.. automethod:: pycan.detect_available_configs


.. _notifier:

Notifier
--------

The Notifier object is used as a message distributor for a bus.

.. autoclass:: pycan.Notifier
    :members:

Errors
------

.. autoclass:: pycan.CanError
