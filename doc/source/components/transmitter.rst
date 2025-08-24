.. _transmitter:

AVL-AXI-STREAM Transmitter
==========================


The transmitter side of the AVL-AXI-STREAM agent follow the standard AVL / UVM structure of sequence, sequencer and driver.

Transmit Sequences
------------------

.. inheritance-diagram:: avl_axi_stream._tsequence
    :parts: 1

A very simple sequence is provided that generates a stream of :any:`SequenceItem` items.

The length of the sequence is defined by the n_items variable, which defaults to 1, but is expected to be override by the factory.

In addition a list of ranges can be provided to define the address space for the sequence. If not provided, the sequence will randomize \
the address along with all other variables of the item.

As the item is parameterized, only the transmit side attributes present will be randomized.

The user is expected to extend the sequence for custom behavior.

In addition a packet based sequence is provided that generates a stream of packets. This ensures the tlast, tkeep and tstrb signals are controlled correctly,
for a continuous stream of bytes. The user can configure the tkeep_rate, but the in the event of a null byte random data is used. The packet is unaffected.

Transmit Driver
---------------

.. inheritance-diagram:: avl_axi_stream._tdriver
    :parts: 2

The transmit driver implements the legal protocol for the bus via 3 user defined tasks:

- :any:`TransDriver.reset` Action to be taken on bus reset. By default all transmit signals are set to 0.
- :any:`TransDriver.quiesce` Action to be taken between transactions. By default all transmit signals are set to 0.
- :any:`TransDriver.drive` Action of driving the transaction on the bus.


Rate Control
~~~~~~~~~~~~

The transmit driver is responsible for rate control. By setting the rate_limit variable in the :any:`TransDriver` class, \
using a lambda function that returns a value between 0.0 and 1.0 the user can control the rate of driving the transmit signals. i.e. the inter-transaction gap.

.. code-block:: python

    avl.Factory.set_variable("*.agent.tdrv.rate_limit", lambda: 0.1)

Wakeup Control (AMBA5)
~~~~~~~~~~~~~~~~~~~~~~

In AMBA5, the transmitter driver can control the wakeup signal. The pre_wakeup and post_wakeup variables are used to define the \
pre-wakeup and post-wakeup delays, respectively. These are defined as lambda functions that return a value between 0.0 and 1.0.

This feature ensures the wakeup signals are driven correctly according to the AMBA5 protocol, while providing randomization of the assertion and \
de-assertion timing.

.. code-block:: python

    avl.Factory.set_variable("*.agent.tdrv.pre_wakeup", lambda: 0.1) # Early assertion of wakeup sign before driving the transmit
    avl.Factory.set_variable("*.agent.tdrv.post_wakeup", lambda: 0.9) # Quick de-assertion of wakeup signal after driving the transmit
