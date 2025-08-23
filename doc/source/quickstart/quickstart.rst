Quickstart Guide
================

This guide will help you get started with the AVL axi-stream library. It will show you how to install the library, compile and run the examples, \
and how to use the library in your own projects.

Before you start this guide, you should have a basic understanding of `AVL <https://avl-core.readthedocs.io/en/latest/>`_.

In order to run the examples you will need to have installed:

- `Python <https://www.python.org/downloads/>`_

- A HDL simulator
    - If you haven't licensed a commercial HDL simulator `Verilator <https://www.veripool.org/wiki/verilator>`_ is available as an open-source alternative.

- A waveform viewer
    - If you haven't licensed a commercial HDL simulator `GTKWave <http://gtkwave.sourceforge.net/>`_ is a popular open-source waveform viewer.

It's also recommended that you have a basic understanding of the `cocotb <https://docs.cocotb.org/en/stable/>`_ framework.

Installing From pip
---------------------

.. code-block:: bash

    # Standard build
    pip install avl-axi-stream

    # Development build
    pip install avl-axi-stream[dev]

This will install the latest version of the library and all required dependencies.
If you want to install a specific version, you can specify the version number:

.. code-block:: bash

    pip install avl-axi-stream==0.1.0

Installing From Source
----------------------

AVL is available via `GitHub <https://github.com/projectapheleia/avl-axi-stream.git>`_.

All required libraries including cocotb are included in the pyproject.toml file.

.. code-block:: bash

    git clone https://github.com/projectapheleia/avl-axi-stream.git
    cd avl-axi-stream

    # Standard build
    pip install .

    # Development build
    pip install .[dev]

Or if you plan on editing the source code, you can install in editable mode:

.. code-block:: bash

    git clone https://github.com/projectapheleia/avl-axi-stream.git
    cd avl-axi-stream
    pip install --editable .[dev]

A script is provided to setup a python virtual environment and install all dependencies for development.

.. code-block:: bash

    git clone https://github.com/projectapheleia/avl-axi-stream.git
    cd avl-axi-stream
    source avl.sh

This assumes you have a simulator and `Graphviz <https://graphviz.gitlab.io/download/>`_ installed, to ensure all examples and documentation can be built out of the box.

.. note::

    avl.sh updated to work on Linux and macOS.

Building The Docs
-----------------

.. code-block:: bash

    cd doc
    make html
    <browser> build/html/index.html

Running the Examples
--------------------

The examples are located in the examples directory. To run the examples, you will need to have a HDL simulator installed, the default is `Verilator <https://www.veripool.org/wiki/verilator>`_.

To run all examples:

.. code-block:: bash

    cd examples
    make sim

To clean up the examples:

.. code-block:: bash

    cd examples
    make clean

Alternatively, you can run each example individually:

.. code-block:: bash

    cd examples/axi-stream/axi-stream-5
    make sim

If using Verilator all examples generate `vcd <https://en.wikipedia.org/wiki/Value_change_dump>`_ files.
