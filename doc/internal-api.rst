.. _internalapi:

Internal API
============

Here we document the odds and ends that are more helpful for creating your own interfaces
or listeners but generally shouldn't be required to interact with python-can.


.. _businternals:


Extending the ``BusABC`` class
------------------------------

Concrete implementations **must** implement the following:
    * :meth:`~pycan.BusABC.send` to send individual messages
    * :meth:`~pycan.BusABC._recv_internal` to receive individual messages
      (see note below!)
    * set the :attr:`~pycan.BusABC.channel_info` attribute to a string describing
      the underlying bus and/or channel

They **might** implement the following:
    * :meth:`~pycan.BusABC.flush_tx_buffer` to allow discarding any
      messages yet to be sent
    * :meth:`~pycan.BusABC.shutdown` to override how the bus should
      shut down
    * :meth:`~pycan.BusABC._send_periodic_internal` to override the software based
      periodic sending and push it down to the kernel or hardware.
    * :meth:`~pycan.BusABC._apply_filters` to apply efficient filters
      to lower level systems like the OS kernel or hardware.
    * :meth:`~pycan.BusABC._detect_available_configs` to allow the interface
      to report which configurations are currently available for new
      connections.
    * :meth:`~pycan.BusABC.state` property to allow reading and/or changing
      the bus state.

.. note::

    *TL;DR*: Only override :meth:`~pycan.BusABC._recv_internal`,
    never :meth:`~pycan.BusABC.recv` directly.

    Previously, concrete bus classes had to override :meth:`~pycan.BusABC.recv`
    directly instead of :meth:`~pycan.BusABC._recv_internal`, but that has
    changed to allow the abstract base class to handle in-software message
    filtering as a fallback. All internal interfaces now implement that new
    behaviour. Older (custom) interfaces might still be implemented like that
    and thus might not provide message filtering:


Concrete instances are usually created by :class:`pycan.Bus` which takes the users
configuration into account.


Bus Internals
~~~~~~~~~~~~~

Several methods are not documented in the main :class:`pycan.BusABC`
as they are primarily useful for library developers as opposed to
library users. This is the entire ABC bus class with all internal
methods:

.. autoclass:: pycan.BusABC
    :private-members:
    :special-members:
    :noindex:



About the IO module
-------------------

Handling of the different file formats is implemented in :mod:`pycan.io`.
Each file/IO type is within a separate module and ideally implements both a *Reader* and a *Writer*.
The reader usually extends :class:`pycan.io.generic.BaseIOHandler`, while
the writer often additionally extends :class:`pycan.Listener`,
to be able to be passed directly to a :class:`pycan.Notifier`.



Adding support for new file formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This assumes that you want to add a new file format, called *canstore*.
Ideally add both reading and writing support for the new file format, although this is not strictly required.

1. Create a new module: *pycan/io/canstore.py*
   (*or* simply copy some existing one like *pycan/io/csv.py*)
2. Implement a reader ``CanstoreReader`` (which often extends :class:`pycan.io.generic.BaseIOHandler`, but does not have to).
   Besides from a constructor, only ``__iter__(self)`` needs to be implemented.
3. Implement a writer ``CanstoreWriter`` (which often extends :class:`pycan.io.generic.BaseIOHandler` and :class:`pycan.Listener`, but does not have to).
   Besides from a constructor, only ``on_message_received(self, msg)`` needs to be implemented.
4. Add a case to ``pycan.io.player.LogReader``'s ``__new__()``.
5. Document the two new classes (and possibly additional helpers) with docstrings and comments.
   Please mention features and limitations of the implementation.
6. Add a short section to the bottom of *doc/listeners.rst*.
7. Add tests where appropriate, for example by simply adding a test case called
   `class TestCanstoreFileFormat(ReaderWriterTest)` to *test/logformats_test.py*.
   That should already handle all of the general testing.
   Just follow the way the other tests in there do it.
8. Add imports to *pycan/__init__py* and *pycan/io/__init__py* so that the
   new classes can be simply imported as *from pycan import CanstoreReader, CanstoreWriter*.



IO Utilities
~~~~~~~~~~~~


.. automodule:: pycan.io.generic
    :members:



Other Utilities
---------------


.. automodule:: pycan.util
    :members:
