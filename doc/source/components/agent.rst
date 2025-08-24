.. _agent:

AVL-AXI-STREAM Agent
====================

.. inheritance-diagram:: avl_axi_stream._agent_cfg
    :parts: 1

.. inheritance-diagram:: avl_axi_stream._agent
    :parts: 1

Unlike many VIPs AVL-AXI-STREAM does not contain an environment.

The AVL-AXI-STREAM verification components is designed to be integrated easily into existing AVL environments, and \
as such an agent can be individually configured without a wider global environment.

The agent is composed of a transmitter and receiver side, which can be used independently or together, and \
and number of non-directional passive components. To configure the agents, the user must override the :doc:`avl_axi_stream.AgentCfg </modules/avl_axi_stream._agent_cfg>` class. \
The best way to do this is via the factory:

.. code-block:: python

    avl.Factory.set_variable("*.agent.cfg.has_transmitter", True)
    avl.Factory.set_variable("*.agent.cfg.has_receiver", True)
    avl.Factory.set_variable("*.agent.cfg.has_monitor", True)

.. note::

    The :doc:`avl_axi_stream.AgentCfg </modules/avl_axi_stream._agent_cfg>` does not configure the AXI-STREAM bus itself, only the agent. \
    The bus configuration is done via RTL interface (see :ref:`configuration` for more details.)

Sub-Components
--------------

.. toctree::
   :maxdepth: 1

   transmitter
   receiver
   monitor
   bandwidth
   coverage
   trace

