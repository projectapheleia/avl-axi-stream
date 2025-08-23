module example_hdl();


    logic clk, rst_n;

    axi_stream_if#(.VERSION(4),
                   .TDATA_WIDTH(32),
                   .Tready_Signal(1),
                   .Tlast_Signal(1),
                   .Tkeep_Signal(1),
                   .Tstrb_Signal(1))  axi_stream_if();

    assign axi_stream_if.aclk = clk;
    assign axi_stream_if.aresetn = rst_n;

endmodule : example_hdl
