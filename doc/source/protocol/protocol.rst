.. _protocol:

Protocol Support
================

AVL-AXI-STREAM supports all AXI STREAM features including AMBA5 protocols with all optional signals.

For full details see `AXI-STREAM Documentation <https://developer.arm.com/documentation/ihi0051/latest/>`_.

.. table:: Interface signals list

   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | Signal  | Source      | Width          | Description                                                                        |
   +=========+=============+================+====================================================================================+
   | ACLK    | Clock       | 1              | ACLK is a global clock signal. All signals are sampled on the rising edge of ACLK. |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | ARESETn | Reset       | 1              | ARESETn is a global reset signal.                                                  |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TVALID  | Transmitter | 1              | TVALID indicates the Transmitter is driving a valid transfer. A transfer takes     |
   |         |             |                | place when both TVALID and TREADY are asserted.                                    |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TREADY  | Receiver    | 1              | TREADY indicates that a Receiver can accept a transfer.                            |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TDATA   | Transmitter | TDATA_WIDTH    | TDATA is the primary payload used to provide the data that is passing across the   |
   |         |             |                | interface. TDATA_WIDTH must be an integer number of bytes and is recommended to be |
   |         |             |                | 8, 16, 32, 64, 128, 256, 512 or 1024-bits.                                         |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TSTRB   | Transmitter | TDATA_WIDTH/8  | TSTRB is the byte qualifier that indicates whether the content of the associated   |
   |         |             |                | byte of TDATA is processed as a data byte or a position byte.                      |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TKEEP   | Transmitter | TDATA_WIDTH/8  | TKEEP is the byte qualifier that indicates whether content of the associated byte  |
   |         |             |                | of TDATA is processed as part of the data stream.                                  |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TLAST   | Transmitter | 1              | TLAST indicates the boundary of a packet.                                          |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TID     | Transmitter | TID_WIDTH      | TID is a data stream identifier. TID_WIDTH is recommended to be no more than 8.    |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TDEST   | Transmitter | TDEST_WIDTH    | TDEST provides routing information for the data stream. TDEST_WIDTH is recommended |
   |         |             |                | to be no more than 8.                                                              |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TUSER   | Transmitter | TUSER_WIDTH    | TUSER is a user-defined sideband information that can be transmitted along the     |
   |         |             |                | data stream. TUSER_WIDTH is recommended to be an integer multiple of               |
   |         |             |                | TDATA_WIDTH/8.                                                                     |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
   | TWAKEUP | Transmitter | 1              | TWAKEUP identifies any activity associated with AXI-Stream interface.              |
   |         |             |                |                                                                                    |
   +---------+-------------+----------------+------------------------------------------------------------------------------------+
