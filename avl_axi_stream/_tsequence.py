# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Transmitter Sequence

import math
import random

import avl

from ._item import SequenceItem


class TransSequence(avl.Sequence):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the sequence

        Sequence of independently randomized transactions

        :param name: Name of the sequence item
        :param parent: Parent component of the sequence item
        """
        super().__init__(name, parent)

        self.i_f = avl.Factory.get_variable(f"{self.get_full_name()}.i_f", None)
        """Handle to interface - defines capabilities and parameters"""

        self.n_items = avl.Factory.get_variable(f"{self.get_full_name()}.n_items", 1)
        """Number of items in the sequence (default 1)"""

    async def body(self) -> None:
        """
        Body of the sequence
        """

        self.info(f"Starting transaction sequence {self.get_full_name()} with {self.n_items} items")
        for _ in range(self.n_items):
            item = SequenceItem(f"from_{self.name}", self)
            await self.start_item(item)
            if _ == self.n_items-1 and hasattr(item, "tlast"):
                item.add_constraint("c_tlast", lambda x : x == 1, item.tlast)
            item.randomize()
            await self.finish_item(item)

class PacketSequence(TransSequence):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the sequence

        Sequence of packets

        :param name: Name of the sequence item
        :param parent: Parent component of the sequence item
        """
        super().__init__(name, parent)

        self.packet_length = avl.Factory.get_variable(f"{self.get_full_name()}.packet_length", lambda : 1)
        """Function to return packet length (in bytes)"""

        self.keep_rate = avl.Factory.get_variable(f"{self.get_full_name()}.keep_rate", lambda : 1.0)
        """Function to determine rate of keep trasactions"""

        self.sleep_rate = avl.Factory.get_variable(f"{self.get_full_name()}.sleep_rate", lambda : 0.0)
        """Function to determine rate of sleep transactions"""

        self.tid =avl.Factory.get_variable(f"{self.get_full_name()}.tid", lambda : 0)
        """Function o determine Stream idetifier"""

    async def body(self) -> None:
        """
        Body of the sequence
        """

        self.info(f"Starting packet sequence {self.get_full_name()} with {self.n_items} items")

        all_bytes = (2**self.i_f.TSTRB_WIDTH)-1
        for _ in range(self.n_items):
            packet_length = self.packet_length()

            transactions_in_packet = math.ceil(packet_length  / self.i_f.TDATA_WIDTH)
            last_bytes =  (1 << ((packet_length % self.i_f.TDATA_WIDTH) // 8)) - 1

            if not hasattr(self.i_f, "tstrb"):
                if last_bytes != 0:
                    raise ValueError("Packet must be multiple of TDATA_WITH if no tstrb")

            i = 0
            while i < transactions_in_packet:
                item = SequenceItem(f"from_{self.name}", self)
                await self.start_item(item)

                # Add constraints
                if hasattr(item, "tid"):
                    item.add_constraint("_c_tid", lambda x: x == self.tid(), item.tid)

                if random.random() > self.keep_rate():
                    if hasattr(item, "tkeep"):
                        item.add_constraint("_c_tkeep", lambda x: x == 0, item.tkeep)
                else:
                    if hasattr(item, "tkeep"):
                        if i == (transactions_in_packet - 1) and last_bytes != 0:
                            item.add_constraint("_c_tkeep", lambda x, y=last_bytes: x == y, item.tkeep)
                        else:
                            item.add_constraint("_c_tkeep", lambda x, y=all_bytes: x == y, item.tkeep)

                    if hasattr(item, "tlast"):
                        if i == (transactions_in_packet - 1):
                            item.add_constraint("_c_tlast", lambda x: x == 1, item.tlast)
                        else:
                            item.add_constraint("_c_tlast", lambda x: x == 0, item.tlast)

                    if hasattr(item, "tstrb"):
                        if i == (transactions_in_packet - 1) and last_bytes != 0:
                           item.add_constraint("_c_tstrb", lambda x, y=last_bytes: x == y, item.tstrb)
                        else:
                            item.add_constraint("_c_tstrb", lambda x, y=all_bytes: x == y, item.tstrb)

                    if hasattr(item, "goto_sleep"):
                        if i == (transactions_in_packet - 1):
                            item.add_constraint("_c_goto_sleep", lambda x: x == 1, item.goto_sleep)
                        else:
                            item.add_constraint("_c_goto_sleep", lambda x: x == 0, item.goto_sleep)

                item.randomize()
                await self.finish_item(item)

                if bool(item.get("tkeep", 1)):
                    i += 1

__all__ = ["TransSequence", "PacketSequence"]
