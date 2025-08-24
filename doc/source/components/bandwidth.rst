.. _bandwidth:

AVL-AXI-STREAM Bandwidth Monitor
================================

.. inheritance-diagram:: avl_axi_stream._bandwidth
    :parts: 2


The :any:`Bandwidth <avl_axi_stream._bandwidth.Bandwidth>` module is a passive component hangs of the :any:`Monitor <avl_axi_stream._monitor.Monitor>` item_export.

The user defines a rolling time window. During each window the bandwidth monitor tallies the number of bytes transferred during that period.

In the :any:`report_phase <avl_axi_stream._bandwidth.Bandwidth.report_phase>` a bar plot of the bandwidth over time is generated.

.. code-block:: python

    avl.Factory.set_variable("*.agent_cfg.has_bandwidth", True)

.. image:: /images/bandwidth.png
