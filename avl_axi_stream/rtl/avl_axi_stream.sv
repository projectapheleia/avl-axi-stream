// Copyright 2025 Apheleia
//
// Description:
// Apheleia Verification Library AXI_STREAM Interface
// As defined in https://developer.arm.com/documentation/ihi0051/latest/

`define AVL_AXI_STREAM_IMPL_CHECK(cond, signal) \
if (``cond`` == 1) begin : ``signal``_cond \
    initial begin \
        #0.1; \
        @(``signal``) $fatal("%m: ``signal`` not supported in configuration");\
    end \
end : ``signal``_cond

interface axi_stream_if #(parameter string CLASSIFICATION      = "AXI-STREAM",
                          parameter int    VERSION = 4,
                          parameter int    TDATA_WIDTH = 8,
                          parameter int    TID_WIDTH = 0,
                          parameter int    TDEST_WIDTH = 0,
                          parameter int    TUSER_WIDTH = 0,
                          parameter bit    Tready_Signal = 0,
                          parameter bit    Tstrb_Signal = 0,
                          parameter bit    Tkeep_Signal = 0,
                          parameter bit    Tlast_Signal = 0,
                          parameter bit    Wakeup_Signal = 0)();

    localparam TSTRB_WIDTH = int'(TDATA_WIDTH/8);
    localparam TKEEP_WIDTH = int'(TDATA_WIDTH/8);

    logic                                                aclk;
    logic                                                aresetn;
    logic                                                tvalid;
    logic                                                tready;
    logic [TDATA_WIDTH > 0 ? TDATA_WIDTH-1 : 0 :0]       tdata;
    logic [TSTRB_WIDTH > 0 ? TSTRB_WIDTH-1 : 0 :0]       tstrb;
    logic [TKEEP_WIDTH > 0 ? TKEEP_WIDTH-1 : 0 :0]       tkeep;
    logic                                                tlast;
    logic [TID_WIDTH > 0   ? TID_WIDTH-1   : 0 :0]       tid;
    logic [TDEST_WIDTH > 0 ? TDEST_WIDTH-1 : 0 :0]       tdest;
    logic [TUSER_WIDTH > 0 ? TUSER_WIDTH-1 : 0 :0]       tuser;
    logic                                                twakeup;

    initial begin
        assert (TDATA_WIDTH % 8 == 0) else $fatal("TDATA_WIDTH must be multiple of 8");
    end

    generate

        `AVL_AXI_STREAM_IMPL_CHECK((Tready_Signal == 0), tready)

        `AVL_AXI_STREAM_IMPL_CHECK((TDATA_WIDTH == 0), tdata)

        `AVL_AXI_STREAM_IMPL_CHECK((TSTRB_WIDTH == 0), tstrb)

        `AVL_AXI_STREAM_IMPL_CHECK((TKEEP_WIDTH == 0), tkeep)

        `AVL_AXI_STREAM_IMPL_CHECK((Tlast_Signal == 0), tlast)

        `AVL_AXI_STREAM_IMPL_CHECK((TID_WIDTH == 0), tid)

        `AVL_AXI_STREAM_IMPL_CHECK((TDEST_WIDTH == 0), tdest)

        `AVL_AXI_STREAM_IMPL_CHECK((TUSER_WIDTH == 0), tuser)

        `AVL_AXI_STREAM_IMPL_CHECK(((VERSION < 5) || (Wakeup_Signal == 0)), twakeup)

    endgenerate

endinterface : AXI_STREAM_if

`undef AVL_AXI_STREAM_IMPL_CHECK
