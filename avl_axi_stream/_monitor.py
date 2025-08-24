# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Monitor

import avl
import cocotb
from cocotb.triggers import FallingEdge, First, RisingEdge
from cocotb.utils import get_sim_time

from ._item import SequenceItem


class Monitor(avl.Monitor):
    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the AMBA Monitor for the APB agent.

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

        self.i_f = avl.Factory.get_variable(f"{self.get_full_name()}.i_f", None)

        self.wakeup = 0

    async def monitor(self) -> None:
        """
        Monitor the APB bus signals and create sequence items based on the activity.
        This method is called to monitor the bus signals and create sequence items
        when there is activity on the bus.
        """
        try:
            item = SequenceItem(f"from_{self.name}", self)
            item.wait_cycles = 0
            item.time_since_wakeup = get_sim_time("ns") - self.wakeup

            item.set("tdata", self.i_f.get("tdata"))
            item.set("tstrb" , self.i_f.get("tstrb"))
            item.set("tkeep", self.i_f.get("tkeep"))
            item.set("tlast", self.i_f.get("tlast"))
            item.set("tid", self.i_f.get("tid"))
            item.set("tdest", self.i_f.get("tdest"))
            item.set("tuser", self.i_f.get("tuser"))

            while True:
                if bool(self.i_f.get("tready", 1)):
                    break

                await RisingEdge(self.i_f.aclk)
                item.wait_cycles += 1

            # Send to export
            self.item_export.write(item)

        except BaseException:
            self.debug(f"Drive task for item {item} was cancelled by reset")
            item.set_event("done")

    async def run_phase(self):
        """
        Run phase for the Requester Driver.
        This method is called during the run phase of the simulation.
        It is responsible for driving the request signals based on the sequencer's items.

        :raises NotImplementedError: If the run phase is not implemented.
        """

        async def wait_on_wakeup() -> None:
            while True:
                await RisingEdge(self.i_f.twakeup)
                self.wakeup = get_sim_time("ns")

        async def wait_on_reset() -> None:
            try:
                await FallingEdge(self.i_f.aresetn)
                await self.reset()
            except BaseException:
                pass

        # Start Wakeup Monitor
        if hasattr(self.i_f, "twakeup"):
            cocotb.start_soon(wait_on_wakeup())

        while True:
            await RisingEdge(self.i_f.aclk)

            if self.i_f.aresetn == 0 or self.i_f.tvalid == 0 or self.i_f.get("twakeup", 1) == 0:
                continue

            monitor_task = cocotb.start_soon(self.monitor())
            reset_task = cocotb.start_soon(wait_on_reset())

            await First(monitor_task, reset_task)
            for t in [monitor_task, reset_task]:
                if not t.done():
                    t.kill()

__all__ = ["Monitor"]
