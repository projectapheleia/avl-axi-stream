# AVL-AXI-STREAM - Apheleia Verification Library AMBA AXI-STREAM Verification Component

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)


AVL-AXI-STREAM has been developed by experienced, industry professional verification engineers to provide a simple, \
extensible verification component for the [AMBA AXI-STREAM Bus](https://developer.arm.com/documentation/ihi0051/latest/) \
developed in [Python](https://www.python.org/) and the [AVL](https://avl-core.readthedocs.io/en/latest/index.html) library.

AVL is built on the [CocoTB](https://docs.cocotb.org/en/stable/) framework, but aims to combine the best elements of \
[UVM](https://accellera.org/community/uvm) in a more engineer friendly and efficient way.


## Protocol Features

| Signal  | Source      | Width         | Description |
|---------|-------------|---------------|-------------|
| **ACLK**    | Clock       | 1             | ACLK is a global clock signal. All signals are sampled on the rising edge of ACLK. |
| **ARESETn** | Reset       | 1             | ARESETn is a global reset signal. |
| **TVALID**  | Transmitter | 1             | TVALID indicates the Transmitter is driving a valid transfer. A transfer takes place when both TVALID and TREADY are asserted. |
| **TREADY**  | Receiver    | 1             | TREADY indicates that a Receiver can accept a transfer. |
| **TDATA**   | Transmitter | TDATA_WIDTH   | TDATA is the primary payload used to provide the data that is passing across the interface. TDATA_WIDTH must be an integer number of bytes and is recommended to be 8, 16, 32, 64, 128, 256, 512 or 1024-bits. |
| **TSTRB**   | Transmitter | TDATA_WIDTH/8 | TSTRB is the byte qualifier that indicates whether the content of the associated byte of TDATA is processed as a data byte or a position byte. |
| **TKEEP**   | Transmitter | TDATA_WIDTH/8 | TKEEP is the byte qualifier that indicates whether content of the associated byte of TDATA is processed as part of the data stream. |
| **TLAST**   | Transmitter | 1             | TLAST indicates the boundary of a packet. |
| **TID**     | Transmitter | TID_WIDTH     | TID is a data stream identifier. TID_WIDTH is recommended to be no more than 8. |
| **TDEST**   | Transmitter | TDEST_WIDTH   | TDEST provides routing information for the data stream. TDEST_WIDTH is recommended to be no more than 8. |
| **TUSER**   | Transmitter | TUSER_WIDTH   | TUSER is a user-defined sideband information that can be transmitted along the data stream. TUSER_WIDTH is recommended to be an integer multiple of TDATA_WIDTH/8. |
| **TWAKEUP** | Transmitter | 1             | TWAKEUP identifies any activity associated with AXI-Stream interface. |

## Component Features

- All protocol features supported
- Simple RTL interface to interact with HDL and define parameter and configuration options
- Transmitter transaction and packets sequences, sequencer and driver with easy to control rate limiter and wakeup control
- Receiver driver with rate control
- Monitor
- Bandwidth monitor generating bus activity plots over user defined windows during simulation
- Functional coverage including performance measurements
- Searchable trace file generation

---

## 📦 Installation

### Using `pip`
```sh
# Standard build
pip install avl-axi-stream

# Development build
pip install avl-axi-stream[dev]
```

### Install from Source
```sh
git clone https://github.com/projectapheleia/avl-axi-stream.git
cd avl-axi-stream

# Standard build
pip install .

# Development build
pip install .[dev]
```

Alternatively if you want to create a [virtual environment](https://docs.python.org/3/library/venv.html) rather than install globally a script is provided. This will install, with edit privileges to local virtual environment.

This script assumes you have [Graphviz](https://graphviz.org/download/) and appropriate simulator installed, so all examples and documentation will build out of the box.


```sh
git clone https://github.com/projectapheleia/avl-axi-stream.git
cd avl-axi-stream
source avl-axi-stream.sh
```

## 📖 Documentation

In order to build the documentation you must have installed the development build.

### Build from Source
```sh
cd docs
make html
<browser> build/html/index.html
```
## 🏃 Examples

In order to run all the examples you must have installed the development build.

To run all examples:

```sh
cd examples

# To run
make -j 8 sim

# To clean
make -j 8 clean
```

To run an individual example:

```sh
cd examples/THE EXAMPLE YOU WANT

# To run
make sim

# To clean
make clean
```

The examples use the [CocoTB Makefile](https://docs.cocotb.org/en/stable/building.html) and default to [Verilator](https://www.veripool.org/verilator/) with all waveforms generated. This can be modified using the standard CocoTB build system.

---


## 🧹 Code Style & Linting

This project uses [**Ruff**](https://docs.astral.sh/ruff/) for linting and formatting.

Check code for issues:

```sh
ruff check .
```

Automatically fix common issues:

```sh
ruff check . --fix
```



## 📧 Contact

- Email: avl@projectapheleia.net
- GitHub: [projectapheleia](https://github.com/projectapheleia)
