# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Agent Configuration

import avl


class AgentCfg(avl.Object):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the avl-apb Agent Configuration

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

        # Agent Attributes
        self.has_transmitter = avl.Factory.get_variable(f"{self.get_full_name()}.has_transmitter", False)
        """Has Transmit Driver"""
        self.has_receiver = avl.Factory.get_variable(f"{self.get_full_name()}.has_receiver", False)
        """Has Receive Driver"""
        self.has_monitor = avl.Factory.get_variable(f"{self.get_full_name()}.has_monitor", False)
        """Has Monitor Driver"""
        self.has_coverage = avl.Factory.get_variable(f"{self.get_full_name()}.has_coverage", False)
        """Has Functional Coverage"""
        self.has_bandwidth = avl.Factory.get_variable(f"{self.get_full_name()}.has_bandwidth", False)
        """Has Bandwidth Monitor"""
        self.has_trace = avl.Factory.get_variable(f"{self.get_full_name()}.has_trace", False)
        """Has Trace Generator"""

__all__ = ["AgentCfg"]
