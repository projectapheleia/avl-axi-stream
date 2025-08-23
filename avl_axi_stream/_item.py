# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Sequence Item

from typing import Any

import avl


class SequenceItem(avl.SequenceItem):
    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the sequence item

        :param name: Name of the sequence item
        :param parent: Parent component of the sequence item
        """
        super().__init__(name, parent)

        # Handle to interface - defines capabilities and parameters
        i_f = avl.Factory.get_variable(f"{self.get_full_name()}.i_f", None)

        if hasattr(i_f, "tdata"):
            self.tdata = avl.Logic(0, width=len(i_f.tdata), fmt=hex)
            """Transmit data (payload)"""

        if hasattr(i_f, "tstrb"):
            self.tstrb = avl.Logic(0, width=len(i_f.tstrb), fmt=hex)
            """Transmit strobe (byte enable)"""

        if hasattr(i_f, "tkeep"):
            self.tkeep = avl.Logic(0, width=len(i_f.tkeep), fmt=hex)
            """Transmit keep"""

        if hasattr(i_f, "tlast"):
            self.tlast = avl.Logic(0, width=len(i_f.tlast), fmt=hex)
            """Transmit last in packet indicator"""

        if hasattr(i_f, "tid"):
            self.tid = avl.Logic(0, width=len(i_f.tid), fmt=hex)
            """Transmit stream indicator"""

        if hasattr(i_f, "tdest"):
            self.tdest = avl.Logic(0, width=len(i_f.tdest), fmt=hex)
            """Transmit routing information"""

        if hasattr(i_f, "tuser"):
            self.tuser = avl.Logic(0, width=len(i_f.tuser), fmt=hex)
            """Transmit user defined sideband signal"""

        if hasattr(i_f, "twakeup"):
            self.goto_sleep = avl.Logic(0, width=len(i_f.twakeup), fmt=str)
            """Wakeup indication (optional >= version 5)"""

        # Constraints

        if hasattr(self, "tstrb"):
            self.add_constraint("c_tstrb", lambda x, y : ((x^y) & y == 0), self.tkeep, self.tstrb)

        # Monitor only attributes used for debug and coverage
        if hasattr(i_f, "tready"):
            self.wait_cycles = 0
            """Wait cycles - cycles from enable to ready (monitor only)"""
            self.set_field_attributes("wait_cycles", compare=False)

        if hasattr(i_f, "twakeup"):
            self.time_since_wakeup = 0
            """Time since last wakeup - used for debug and coverage (monitor only)"""
            self.set_field_attributes("time_since_wakeup", compare=False)

        # By default transpose to make more readable
        self.set_table_fmt(transpose=True)

    def set(self, name : str, value : int) -> None:
        """
        Set the value of a field in the sequence item - if it exists.

        :param name: Name of the field to set
        :param value: Value to set for the field
        """
        signal = getattr(self, name, None)
        if signal is not None:
            signal.value = value

    def get(self, name : str, default : Any = None) -> int:
        """
        Get the value of a field in the sequence item - if it exists.

        :param name: Name of the field to get
        :param default: Default value to return if the field does not exist
        :return: Value of the field or default value
        """
        signal = getattr(self, name, None)
        if signal is not None:
            return signal.value
        return default

__all__ = ["SequenceItem"]
