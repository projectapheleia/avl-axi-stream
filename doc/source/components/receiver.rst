.. _receiver:

AVL-AXI-STREAM Receiver
=======================

.. inheritance-diagram:: avl_axi_stream._rdriver
    :parts: 2

The receiver side of the AVL-AXI-STREAM agent does not follow the standard AVL / UVM structure of sequence, sequencer and driver.

As the receiver is responsive the overhead of interacting between a monitor, sequence and driver is overly complicated \
and not required.

Instead the receiver is implemented as a single driver that implements the legal protocol for the bus via 3 user defined tasks:

- :any:`RecDriver.reset` Action to be taken on bus reset. By default all completion signals are set to 0.
- :any:`Driver.quiesce` Action to be taken between transactions. By default all completion signals are set to 0.
- :any:`RecDriver.drive` Action of driving.

In AXI-STEAM the receiver is only responsible for driving tready (if present), and as such the rdriver is very simple.

Rate Control
~~~~~~~~~~~~

The receiver driver is responsible for rate control. By setting the rate_limit variable in the :any:`RecDriver` class, \
using a lambda function that returns a value between 0.0 and 1.0 the user can control the rate of driving the tready signal, if supported.

.. code-block:: python

    avl.Factory.set_variable("*.agent.rdrv.rate_limit", lambda: 0.1)


Example
~~~~~~~

.. literalinclude:: ../../../examples/axi-stream/packet_of_bytes_stream/cocotb/example.py
    :language: python
