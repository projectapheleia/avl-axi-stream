# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Driver

import asyncio
import random

import avl
import cocotb
from cocotb.triggers import First, NextTimeStep, RisingEdge

from ._driver import Driver
from ._item import SequenceItem


class TransDriver(Driver):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the Transmitter Driver for the AMBA agent.

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

        # Pre and Post Wakeup
        if hasattr(self.i_f, "twakeup"):
            self.pre_wakeup =  avl.Factory.get_variable(f"{self.get_full_name()}.pre_wakeup", lambda : 0.1)
            """Pre-wakeup delay - time to wait before driving the wakeup signal (0.0 - 1.0) (>= version 5)"""
            self.post_wakeup = avl.Factory.get_variable(f"{self.get_full_name()}.post_wakeup", lambda : 0.1)
            """Post-wakeup delay - time to wait after driving the wakeup signal (0.0 - 1.0) (>= version 5)"""

            if not callable(self.pre_wakeup) or not callable(self.post_wakeup):
                raise TypeError("pre_wakeup and post_wakeup must be callable (lambda functions) that return a float between 0.0 and 1.0")

    async def reset(self) -> None:
        """
        Reset the driver by setting all signals to their default values.
        This method is called when the driver is reset.

        By default 0's all signals - can be overridden in subclasses to add randomization or other behavior.
        """

        self.i_f.set("twakeup", 0)
        self.i_f.set("tvalid", 0)
        self.i_f.set("tdata", 0)
        self.i_f.set("tstrb", 0)
        self.i_f.set("tkeep", 0)
        self.i_f.set("tlast", 0)
        self.i_f.set("tid", 0)
        self.i_f.set("tdest", 0)
        self.i_f.set("tuser", 0)

    async def quiesce(self) -> None:
        """
        Quiesce the driver by setting the psel signal to 0.
        This method is called when the driver is quiesced.

        By default calls reset() to set all signals to their default values.
        Can be overridden in subclasses to add randomization or other behavior.
        """

        self.i_f.set("tvalid", 0)
        self.i_f.set("tdata", 0)
        self.i_f.set("tstrb", 0)
        self.i_f.set("tkeep", 0)
        self.i_f.set("tlast", 0)
        self.i_f.set("tid", 0)
        self.i_f.set("tdest", 0)
        self.i_f.set("tuser", 0)

    async def drive(self, item : SequenceItem) -> None:
        """
        Drive the signals based on the provided sequence item.
        This method is called to drive the signals of the AMBA interface.

        :param item: The sequence item containing the values to drive
        :type item: SequenceItem
        """
        awake = False
        try:
            self.i_f.set("tvalid", 0)

            # Rate Limiter
            rate = self.rate_limit()
            while random.random() > rate:
                await RisingEdge(self.i_f.aclk)

            if hasattr(self.i_f, "twakeup") and not awake:
                self.i_f.set("twakeup", 1)
                delay = self.pre_wakeup()
                while random.random() > delay:
                    await RisingEdge(self.i_f.aclk)

            self.i_f.set("tdata", item.get("tdata"))
            self.i_f.set("tstrb", item.get("tstrb"))
            self.i_f.set("tkeep", item.get("tkeep"))
            self.i_f.set("tlast", item.get("tlast"))
            self.i_f.set("tid", item.get("tid"))
            self.i_f.set("tdest", item.get("tdest"))
            self.i_f.set("tuser", item.get("tuser"))
            self.i_f.set("tvalid", 1)

            while True:
                await RisingEdge(self.i_f.aclk)
                if self.i_f.get("tready", 1) and self.i_f.get("twakeup", 1):
                    break

            # Clear the bus
            await self.quiesce()

            # Post wakeup
            if item.get("goto_sleep", False):
                delay = self.post_wakeup()
                while random.random() > delay:
                    await RisingEdge(self.i_f.aclk)
                self.i_f.set("twakeup", 0)
                awake = False
            else:
                awake = True

            item.set_event("done")
        except asyncio.CancelledError:
            raise
        except Exception:
            self.debug(f"Transmitter drive task for item was cancelled by reset:\n{item}")

    async def get_next_item(self, item : SequenceItem = None) -> SequenceItem:
        """
        Get the next sequence item.

        This method retrieves the next sequence item from the sequencer or
        the previously reset interrupted item.

        The implementation ensures items are driven on the rising edge of aclk, when not in reset,
        while allowing for back-to-back transmits if the sequencer provides them.

        :param item: The sequence item to retrieve, defaults to None
        :type item: SequenceItem, optional
        :return: The next sequence item
        :rtype: SequenceItem
        :raises NotImplementedError: If the method is not implemented in subclasses
        """

        async def next_time_step() -> None:
            await NextTimeStep()

        if item is not None:
            next_item = item
        else:
            a = cocotb.start_soon(self.seq_item_port.blocking_get())
            b = cocotb.start_soon(next_time_step())

            await First(a, b)
            if not a.done():
                await a
                await RisingEdge(self.i_f.aclk)
            next_item = a.result()

        while self.i_f.get("aresetn") == 0:
            await RisingEdge(self.i_f.aclk)

        return next_item

__all__ = ["TransDriver"]
