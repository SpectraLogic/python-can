.. _bus:

Bus
---

The :class:`~pycan.BusABC` class, as the name suggests, provides an abstraction of a CAN bus.
The bus provides a wrapper around a physical or virtual CAN Bus.
An interface specific instance of the :class:`~pycan.BusABC` is created by the :class:`~pycan.Bus`
class, for example::

    vector_bus = pycan.Bus(interface='vector', ...)

That bus is then able to handle the interface specific software/hardware interactions
and implements the :class:`~pycan.BusABC` API.

A thread safe bus wrapper is also available, see `Thread safe bus`_.

Autoconfig Bus
''''''''''''''

.. autoclass:: pycan.Bus
    :members:
    :undoc-members:


API
'''

.. autoclass:: pycan.BusABC
    :members:
    :undoc-members:

    .. automethod:: __iter__

Transmitting
''''''''''''

Writing individual messages to the bus is done by calling the :meth:`~pycan.BusABC.send` method
and passing a :class:`~pycan.Message` instance. Periodic sending is controlled by the
:ref:`broadcast manager <bcm>`.


Receiving
'''''''''

Reading from the bus is achieved by either calling the :meth:`~pycan.BusABC.recv` method or
by directly iterating over the bus::

    for msg in bus:
        print(msg.data)

Alternatively the :class:`~pycan.Listener` api can be used, which is a list of :class:`~pycan.Listener`
subclasses that receive notifications when new messages arrive.


Filtering
'''''''''

Message filtering can be set up for each bus. Where the interface supports it, this is carried
out in the hardware or kernel layer - not in Python.


Thread safe bus
---------------

This thread safe version of the :class:`~pycan.BusABC` class can be used by multiple threads at once.
Sending and receiving is locked separately to avoid unnecessary delays.
Conflicting calls are executed by blocking until the bus is accessible.

It can be used exactly like the normal :class:`~pycan.BusABC`:

    # 'socketcan' is only an example interface, it works with all the others too
    my_bus = pycan.ThreadSafeBus(interface='socketcan', channel='vcan0')
    my_bus.send(...)
    my_bus.recv(...)

.. autoclass:: pycan.ThreadSafeBus
    :members:
