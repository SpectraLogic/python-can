Scripts
=======

The following modules are callable from pythoncan.

They can be called for example by ``python -m pycan.logger`` or ``can_logger.py`` (if installed using pip).

pycan.logger
----------

Command line help, called with ``--help``:


.. command-output:: python -m pycan.logger -h


pycan.player
----------

.. command-output:: python -m pycan.player -h


pycan.viewer
----------

A screenshot of the application can be seen below:

.. image:: images/viewer.png
    :width: 100%

The first column is the number of times a frame with the particular ID that has been received, next is the timestamp of the frame relative to the first received message. The third column is the time between the current frame relative to the previous one. Next is the length of the frame, the data and then the decoded data converted according to the ``-d`` argument. The top red row indicates an error frame.

Command line arguments
^^^^^^^^^^^^^^^^^^^^^^

By default the ``pycan.viewer`` uses the :doc:`/interfaces/socketcan` interface. All interfaces are supported and can be specified using the ``-i`` argument or configured following :doc:`/configuration`.

The full usage page can be seen below:

.. command-output:: python -m pycan.viewer -h

