Virtual
=======

The virtual interface can be used as a way to write OS and driver independent
tests.

A virtual CAN bus that can be used for automatic tests. Any Bus instances
connecting to the same channel (in the same python program) will get each
others messages.


.. code-block:: python
    
    import pycan

    bus1 = pycan.interface.Bus('test', bustype='virtual')
    bus2 = pycan.interface.Bus('test', bustype='virtual')

    msg1 = pycan.Message(arbitration_id=0xabcde, data=[1,2,3])
    bus1.send(msg1)
    msg2 = bus2.recv()

    assert msg1 == msg2
