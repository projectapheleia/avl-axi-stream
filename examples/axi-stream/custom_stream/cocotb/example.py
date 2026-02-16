# Copyright 2024 Apheleia
#
# Description:
# Apheleia attributes example


import avl
import avl_axi_stream
import cocotb

from cocotb.triggers import Timer

class CustomSequence(avl_axi_stream.TransSequence):
    def __init__(self, name: str, parent: avl.Component) -> None:
        super().__init__(name, parent)

    async def body(self) -> None:

        # Fully Random Sequence
        await self.write(randomize=True)
        await Timer(500, unit="ns")

        # Constrained Sequence
        await self.write(randomize=False, tdata=0x0)
        await self.write(randomize=False, tdata=0x1)
        await self.write(randomize=False, tdata=0x2)
        await self.write(randomize=False, tdata=0x3, tlast=1)
        await Timer(500, unit="ns")

        # Constrained Stream Sequence
        await self.write_stream([0x8, 0x9, 0xa], randomize=False)
        await Timer(500, unit="ns")

        # Constrained Stream Sequence
        await self.write_stream([{"tdata" : 0x20} , {"tdata" : 0x21}], randomize=False)
        await Timer(500, unit="ns")

class example_env(avl.Env):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)
        self.clk = avl.Factory.get_variable(f"{self.get_full_name()}.clk", None)
        self.rst_n = avl.Factory.get_variable(f"{self.get_full_name()}.rst_n", None)
        self.agent = avl_axi_stream.Agent("agent", self)

    async def run_phase(self):
        self.raise_objection()

        cocotb.start_soon(self.timeout(1, units="ms"))
        cocotb.start_soon(self.clock(self.clk, 100))
        await self.async_reset(self.rst_n, duration=100, units="ns", active_high=False)

        self.drop_objection()

@cocotb.test
async def test(dut):
    """
    Example Simple interface
        - No tready
        - No tstrb
        - No tkeep
        - No tlast
        - No tid
        - No tdest
        - No tuser
        - No twakeup
        - 100 items in the request sequence with a rate limit of 0.1
        - random data

    :param dut: The DUT instance
    :return: None
    """
    avl.Factory.set_variable("*.clk", dut.clk)
    avl.Factory.set_variable("*.rst_n", dut.rst_n)
    avl.Factory.set_variable("*.hdl", dut.axi_stream_if)
    avl.Factory.set_variable("*.agent.cfg.has_transmitter", True)
    avl.Factory.set_variable("*.agent.cfg.has_receiver", False)
    avl.Factory.set_variable("*.agent.cfg.has_monitor", True)
    avl.Factory.set_variable("*.agent.cfg.has_coverage", True)
    avl.Factory.set_variable("*.agent.cfg.has_trace", True)
    avl.Factory.set_variable("*.agent.tsqr.tseq.n_items", 100)
    avl.Factory.set_variable("*.agent.tdrv.rate_limit", lambda: 0.1)

    avl.Factory.set_override_by_type(avl_axi_stream.TransSequence, CustomSequence)

    e = example_env("env", None)
    await e.start()

