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

    async def write(self, randomize: bool = True, **kwargs) -> SequenceItem:
        """
        Write a single transaction item

        Creates, constrains, and sends a single AXI Stream transaction.
        Can either randomize the item or set specific values via kwargs.

        :param randomize: If True, randomizes the item. If False, uses kwargs to set values.
        :type randomize: bool
        :param kwargs: Field values to set when randomize=False (e.g., tdata=0x1234, tkeep=0xF)
        :return: The sequence item that was sent
        :rtype: SequenceItem
        """
        item = SequenceItem(f"from_{self.name}", self)
        await self.start_item(item)

        if randomize:
            # Randomize all fields
            item.randomize()
        else:
            # Set fields from kwargs
            for field_name, value in kwargs.items():
                if hasattr(item, field_name):
                    item.set(field_name, value)

        await self.finish_item(item)

        return item

    async def write_stream(self, stream: list, randomize: bool = False) -> list[SequenceItem]:
        """
        Write a stream of data transactions

        Accepts a list of data entries and writes them sequentially.
        The last entry automatically sets tlast=1.


        :param stream: List of data entries. Each entry can be:
                       - int: Value for tdata field
                       - dict: Field names and values (e.g., {'tdata': 0x1234, 'tkeep': 0xF})
        :type stream: list
        :param randomize: If True, randomizes the item. If False, uses kwargs to set values.
        :type randomize: bool
        :return: List of sequence items that were sent
        :rtype: list[SequenceItem]

        Example:
            # Simple data stream
            await seq.write_stream([0x10, 0x20, 0x30, 0x40])

            # Stream with explicit field values
            await seq.write_stream([
                {'tdata': 0x1234, 'tkeep': 0xF},
                {'tdata': 0x5678, 'tkeep': 0xF},
                {'tdata': 0xABCD, 'tkeep': 0x3}
            ])

            # separate case for a simplified stream (just tdata):
            await seq.write_stream([0x1234, 0x5678, 0xF, 0xABCD, 0x3])

        """
        items = []

        for i, entry in enumerate(stream):
            tlast =  1 if (i == len(stream) - 1) else 0

            if isinstance(entry, dict):
                # Entry is a dictionary of field values
                item = await self.write(tlast=tlast, randomize=randomize, **entry)
            else:
                # Entry is a single value for tdata - simplified version!
                item = await self.write(tlast=tlast, randomize=randomize, tdata=entry)

            items.append(item)

        return items

    async def body(self) -> None:
        """
        Body of the sequence

        Generates n_items transactions by repeatedly calling write()
        """
        self.info(f"Starting transaction sequence {self.get_full_name()} with {self.n_items} items")

        for i in range(self.n_items):
            tlast = 1 if (i == self.n_items - 1) else 0
            await self.write(tlast=tlast)

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
