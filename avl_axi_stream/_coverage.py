# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Coverage

import avl

from ._item import SequenceItem


class Coverage(avl.Component):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize Coverage

        :param name: Name of the coverage class.
        :type name: str
        :param parent: Parent component.
        :type parent: Component
        """
        super().__init__(name, parent)

        self.item_port = avl.List()
        self.item = SequenceItem("for_coverage", self)

        self.packet_length = 0

        # Define coverage
        self.cg = avl.Covergroup("axi_stream", self)
        self.cg.set_comment("AXI Stream Coverage")

        if hasattr(self.item, "tkeep"):
            #TKEEP
            self.cp_tkeep = self.cg.add_coverpoint("tkeep", lambda: self.item.tkeep)
            self.cp_tkeep.set_comment("TKEEP")
            for i in range(2):
                self.cp_tkeep.add_bin(f"{i}", i)

        if hasattr(self.item, "tlast"):
            #TLAST
            self.cp_tlast = self.cg.add_coverpoint("tlast", lambda: self.item.tlast)
            self.cp_tlast.set_comment("TLAST")
            for i in range(2):
                self.cp_tlast.add_bin(f"{i}", i)

            self.cp_packet_length = self.cg.add_coverpoint("packet_length", lambda : self.packet_length if (self.item.get("tkeep", 1) and self.item.tlast) else 0)
            self.cp_packet_length.set_comment("Packet length in bytes")
            self.cp_packet_length.add_bin("packet_length", range(1, 8*1024), stats=True)

        if hasattr(self.item, "tkeep") and hasattr(self.item, "tlast"):
            self.cc_tkeepXtlast = self.cg.add_covercross("tkeepXtlast", self.cp_tkeep, self.cp_tlast)
            self.cc_tkeepXtlast.set_comment("TKEEP x TLAST")

        if hasattr(self.item, "tdata"):
            # TDATA
            self.cp_tdata = self.cg.add_coverpoint("tdata", lambda: self.item.tdata if self.item.get("tkeep", 1) else 0)
            self.cp_tdata.set_comment("TDATA (transmit data)")
            for i in range(self.item.tdata.width):
                self.cp_tdata.add_bin(f"[{i}] == 0", lambda x ,y=i: 0 == (x & (1<<y)))
                self.cp_tdata.add_bin(f"[{i}] == 1", lambda x ,y=i: 0 != (x & (1<<y)))

        if hasattr(self.item, "wait_cycles"):
            # TREADY
            self.cp_wait_cycles = self.cg.add_coverpoint("wait_cycles", lambda: self.item.wait_cycles)
            self.cp_wait_cycles.set_comment("Wait cycles (number of cycles before TREADY after TVALID)")
            for i in range(3):
                self.cp_wait_cycles.add_bin(f"{i}", i)
            self.cp_wait_cycles.add_bin("wait_cycles", range(0,1024), stats=True)

        if hasattr(self.item, "tstrb"):
            # TSTRB
            self.cp_tstrb = self.cg.add_coverpoint("tstrb", lambda: self.item.tstrb if self.item.get("tkeep", 1) else 0)
            self.cp_tstrb.set_comment("TSTRB (transmit strobe)")
            for i in range(self.item.tstrb.width):
                self.cp_tstrb.add_bin(f"[{i}] == 0", lambda x, y=i : 0 == (x & (1<<y)))
                self.cp_tstrb.add_bin(f"[{i}] == 1", lambda x, y=i : 0 != (x & (1<<y)))

            self.cp_tstrb_size = self.cg.add_coverpoint("tstrb_size", lambda: int(self.item.tstrb).bit_count() if self.item.get("tkeep", 1) else 0)
            self.cp_tstrb_size.set_comment("TSTRB (transmit strobe size)")
            for i in range(1, self.item.tstrb.width+1):
                self.cp_tstrb_size.add_bin(f"{i}", i)

        if hasattr(self.item, "tuser"):
            # TUSER
            self.cp_tuser = self.cg.add_coverpoint("tuser", lambda: self.item.tuser if self.item.get("tkeep", 1) else 0)
            self.cp_tuser.set_comment("TUSER (user sideband)")
            for i in range(self.item.tuser.width):
                self.cp_tuser.add_bin(f"[{i}] == 0", lambda x, y=i : 0 == (x & (1<<y)))
                self.cp_tuser.add_bin(f"[{i}] == 1", lambda x, y=i : 0 != (x & (1<<y)))

        if hasattr(self.item, "tdest"):
            # TDEST
            self.cp_tdest = self.cg.add_coverpoint("tdest", lambda: self.item.tdest if self.item.get("tkeep", 1) else 0)
            self.cp_tdest.set_comment("TDEST (routing sideband)")

            for i in range(self.item.tdest.get_min(), self.item.tdest.get_max()+1):
                self.cp_tdest.add_bin(f"[{i}]", i)

        if hasattr(self.item, "tid"):
            #TID
            self.cp_tid = self.cg.add_coverpoint("tid", lambda: self.item.tid if self.item.get("tkeep", 1) else 0)
            self.cp_tid.set_comment("TDEST (stream sideband)")

            for i in range(self.item.tid.get_min(), self.item.tid.get_max()+1):
                self.cp_tid.add_bin(f"[{i}]", i)

        if hasattr(self.item, "time_since_wakeup"):
            # TWAKEUP
            self.cp_twakeup = self.cg.add_coverpoint("twakeup", lambda: self.item.time_since_wakeup)
            self.cp_twakeup.set_comment("TWAKEUP (wakeup indication - time in ns since wakeup was raised)")
            self.cp_twakeup.add_bin("ns", range(0, 1000), stats=True)


        self.cg.report(full=True)

    async def run_phase(self) -> None:
        """
        Run phase for the coverage component.

        """

        while True:
            # Wait for an item to be available
            self.item = await self.item_port.blocking_get()

            if hasattr(self.item, "tdata") and bool(self.item.get("tkeep", 1)):
                self.packet_length += int(self.item.get("tstrb", (1 << self.item.tdata.width)-1).bit_count())

            # Sample
            self.cg.sample()

            if bool(self.item.get("tkeep", 1)) and bool(self.item.get("tlast", 1)):
                self.packet_length = 0

__all__ = ["Coverage"]
