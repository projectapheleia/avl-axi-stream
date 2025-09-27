# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Driver

import asyncio
import random

import avl
from cocotb.triggers import RisingEdge

from ._driver import Driver
from ._item import SequenceItem


class RecDriver(Driver):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the Receiver Driver for the AMBA agent.

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

        if not hasattr(self.i_f, "tready"):
            raise ValueError("Receiver Driver instanced on AXI-STREAM with no tready signal")

    async def reset(self) -> None:
        """
        Reset the driver by setting all signals to their default values.
        This method is called when the driver is reset.

        By default 0's all signals - can be overridden in subclasses to add randomization or other behavior.
        """

        self.i_f.set("tready", 0)

    async def drive(self, item : SequenceItem) -> None:
        """
        Drive the signals based on the provided sequence item.
        This method is called to drive the signals of the AMBA interface.

        :param item: The sequence item containing the values to drive
        :type item: SequenceItem
        """
        try:
            self.i_f.set("tready", 0)
            # Rate Limiter
            rate = self.rate_limit()
            while random.random() > rate:
                await RisingEdge(self.i_f.aclk)

            if bool(self.i_f.get("twakeup", 1)):
                self.i_f.set("tready", 1)

                # Wait for the next clock edge to drive the item
                while True:
                    await RisingEdge(self.i_f.aclk)
                    if bool(self.i_f.get("tvalid", 1)) or not bool(self.i_f.get("twakeup", 1)):
                        break

            # Clear the bus
            await self.quiesce()
        except asyncio.CancelledError:
            raise
        except Exception:
            self.debug(f"Receiver drive task for item was cancelled by reset:\n{item}")

    async def get_next_item(self, item : SequenceItem = None) -> SequenceItem:
        """
        Get the next sequence item.

        The implementation ensures items are driven on the rising edge of pclk, when not in reset,
        while allowing for back-to-back requests if the sequencer provides them.

        :param item: The sequence item to retrieve, defaults to None
        :type item: SequenceItem, optional
        :return: The next sequence item
        :rtype: SequenceItem
        :raises NotImplementedError: If the method is not implemented in subclasses
        """

        return None

__all__ = ["RecDriver"]
