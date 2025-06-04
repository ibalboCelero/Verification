//--------------------------------------------------------------------------------------------------
//
//            (C) COPYRIGHT 2024 Celero Communications Inc.
//                ALL RIGHTS RESERVED
//
// This entire notice must be reproduced on all copies of this file
// and copies of this file may only be made by a person if such person is
// permitted to do so under the terms of a subsisting license agreement
// from Celero Communications Inc.
//
//--------------------------------------------------------------------------------------------------
// File name   : dsp_rx_tb_custom.svh
// Date        : 2024-12-10
//--------------------------------------------------------------------------------------------------
// Description : Custom testbench configurations
//--------------------------------------------------------------------------------------------------
// Author      :
//--------------------------------------------------------------------------------------------------

localparam NB_SAMPLES = 8;
localparam PARALLELISM = 384;

logic [NB_SAMPLES*192 - 1 : 0] i_dsp_rx_high_hi ;
logic [NB_SAMPLES*192 - 1 : 0] i_dsp_rx_low_hi  ;

logic [NB_SAMPLES*192 - 1 : 0] i_dsp_rx_high_hq ;
logic [NB_SAMPLES*192 - 1 : 0] i_dsp_rx_low_hq  ;

// assign i_dsp_rx_hi = {i_dsp_rx_high_hi, i_dsp_rx_low_hi};
// assign i_dsp_rx_hq = {i_dsp_rx_high_hq, i_dsp_rx_low_hq};

real    clk_design_freq                                                                             ;
real    clk_design_time                                                                             ;
real    clk_design_toggle                                                                           ;
real    clk_noise                                                                                   ;
real    clk_duty_cycle                                                                              ;
real    duty_noise                                                                                  ;
real    clk_cal_adc_freq                                                                            ;
real    clk_regmap_freq_dsp_rx                                                                      ;
initial
begin
  //--> Clock Definition
  clk_design_freq   = 858.34                                                                        ; //--> Freq. in MHz")
  // clk_cal_adc_freq  = 830.77                                                                        ;
  clk_regmap_freq_dsp_rx   = 300                                                                    ;
  clk_noise         = 1                                                                             ; //--> Noise in PS")
  clk_duty_cycle    = 50                                                                            ; //--> DC in porcentage")
  duty_noise        = 0                                                                             ; //--> DC in porcentage")

  i_arst_n <= 1'b1;


    force   u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_adc_dac_i_du_srst_sync        = 1                 ;

    force   u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_adc_dac_q_du_srst_sync        = 1                 ;

    force   u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_rx_comp_eq_i_du_srst_sync     = 1                 ;

    force   u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_rx_comp_eq_q_du_srst_sync     = 1                 ;

    force   u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_correlator_i_du_srst_sync     = 1                 ;

    force   u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_correlator_q_du_srst_sync     = 1                 ;

    @(posedge i_arst_n                   )                                                          ;

    @(posedge i_line_egress_digital_clock)                                                          ;

    release u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_adc_dac_i_du_srst_sync                            ;

    release u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_adc_dac_q_du_srst_sync                            ;

    release u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_rx_comp_eq_i_du_srst_sync                         ;

    release u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_rx_comp_eq_q_du_srst_sync                         ;

    release u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_correlator_i_du_srst_sync                         ;

    release u_dsp_rx.u_dsp_rx_regmap.dsp_rx__i_rm_correlator_q_du_srst_sync                         ;
 
    force   u_dsp_rx.o_dsp_rx_hi        = {3072{1'b0}}                 ;
    force   u_dsp_rx.o_dsp_rx_hq        = {3072{1'b0}}                 ;
    release   u_dsp_rx.o_dsp_rx_hi ;
    release   u_dsp_rx.o_dsp_rx_hq ;

    force dsp_rx_tb.u_dsp_rx.u_rx_comp_eq_i.u_rx_equalizer_high.out_equalizer_r= {3072{1'b0}} ;
    force dsp_rx_tb.u_dsp_rx.u_rx_comp_eq_q.u_rx_equalizer_high.out_equalizer_r= {3072{1'b0}} ;
    release dsp_rx_tb.u_dsp_rx.u_rx_comp_eq_i.u_rx_equalizer_high.out_equalizer_r;
    release dsp_rx_tb.u_dsp_rx.u_rx_comp_eq_q.u_rx_equalizer_high.out_equalizer_r;

    force dsp_rx_tb.u_dsp_rx.u_rx_bypass_samples_i.decimated_samples_r = {479{1'b0}} ;
    force dsp_rx_tb.u_dsp_rx.u_rx_bypass_samples_q.decimated_samples_r = {479{1'b0}} ;
    release dsp_rx_tb.u_dsp_rx.u_rx_bypass_samples_i.decimated_samples_r;
    release dsp_rx_tb.u_dsp_rx.u_rx_bypass_samples_q.decimated_samples_r;

  i_regmap_data   <= 'd0;
  i_regmap_address<= 'd0;
  i_regmap_wr_rd  <= 'd0;
  i_regmap_req    <= 'd0;
  // i_regmap_offset <= 'd0;
  #1000;




  // //--> Input Init.
  // i_data            = 0                                                                             ;

  // //--> Reset
  // reset()                                                                                           ;
end

reg [1535 : 0] w_i_low;
reg [1535 : 0] w_q_low;
reg [1535 : 0] w_i_high;
reg [1535 : 0] w_q_high;

// assert afifo lp
logic assert_loopback;

initial begin

    assert_loopback = 0;

    @(posedge dsp_rx_tb.u_dsp_rx.u_afifo_loopback_hi.o_valid)

    @(posedge ad_pll_lrx_digclk_div24)

    @(posedge ad_pll_lrx_digclk_div24)
    
    @(posedge ad_pll_lrx_digclk_div24)

    assert_loopback = 1;

end

clock
  u_clock_line_ingress
  (
    //----> Outputs")
    .o_clk                                          (ad_pll_lrx_digclk_div24                           ),
    //----> Inputs
    .i_clk_freq                                     (clk_design_freq                                ),
    .i_clk_noise                                    (clk_noise                               ),
    .i_duty_cycle                                   (clk_duty_cycle                          ),
    .i_duty_noise                                   (duty_noise                          )
  );

clock
  u_clock_regmap2
  (
    //----> Outputs")
    .o_clk                                          (i_clock_regmap                           ),
    //----> Inputs
    .i_clk_freq                                     (clk_design_freq                                ),
    .i_clk_noise                                    (clk_noise                               ),
    .i_duty_cycle                                   (clk_duty_cycle                          ),
    .i_duty_noise                                   (duty_noise                          )
  );




// clock
// u_clock_design_netlist
// (
//   //----> Outputs")
//   .o_clk                                          (i_clock_netlist                                  ),
//   //----> Inputs
//   .i_clk_freq                                     (clk_design_freq                                  ),
//   .i_clk_noise                                    (clk_noise                                        ),
//   .i_duty_cycle                                   (clk_duty_cycle                                   ),
//   .i_duty_noise                                   (duty_noise                                       ) 
// );

clock
u_clock_design_tx
(
    //----> Outputs")
  .o_clk                                          (i_line_egress_digital_clock                             ),
  //----> Inputs
  .i_clk_freq                                     (clk_design_freq                                  ),
  .i_clk_noise                                    (clk_noise                                        ),
  .i_duty_cycle                                   (clk_duty_cycle                                   ),
  .i_duty_noise                                   (duty_noise  )   
);

// clock
// u_clock_design_rx_cal_hi
// (
//     //----> Outputs")
//   .o_clk                                          (ad_hi_lrx_calADC_clk                            ),
//   //----> Inputs
//   .i_clk_freq                                     (clk_cal_adc_freq                                 ),
//   .i_clk_noise                                    (clk_noise                                        ),
//   .i_duty_cycle                                   (clk_duty_cycle                                   ),
//   .i_duty_noise                                   (duty_noise )    
// );

// clock
// u_clock_design_rx_cal_hq
// (
//     //----> Outputs")
//   .o_clk                                          (ad_hq_lrx_calADC_clk                            ),
//   //----> Inputs
//   .i_clk_freq                                     (clk_cal_adc_freq                                 ),
//   .i_clk_noise                                    (clk_noise                                        ),
//   .i_duty_cycle                                   (clk_duty_cycle                                   ),
//   .i_duty_noise                                   (duty_noise )    
// );

// clock
// u_clock_design_rx_analog
// (
//     //----> Outputs")
//   .o_clk                                          (ad_I_lrx_hb_adc_CLK_even[0]                      ),
//   //----> Inputs
//   .i_clk_freq                                     (clk_design_freq                                  ),
//   .i_clk_noise                                    (clk_noise                                        ),
//   .i_duty_cycle                                   (clk_duty_cycle                                   ),
//   .i_duty_noise                                   (duty_noise )    
// );
//----> Add verification modules - Testbench setup.

// generate
//     genvar ptrAdc;
//     for(ptrAdc=0;ptrAdc<(PARALLELISM/2)/16;ptrAdc=ptrAdc+1) begin: adcConnect
//         assign ad_I_lrx_hb_adc_Slice0_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+0 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice1_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+1 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice2_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+2 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice3_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+3 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice4_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+4 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice5_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+5 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice6_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+6 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice7_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+7 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice8_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+8 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice9_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+9 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice10_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+10)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice11_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+11)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice12_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+12)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice13_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+13)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice14_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+14)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_I_lrx_hb_adc_Slice15_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_high[((ptrAdc*16)+1+15)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
        
//         assign ad_I_lrx_lb_adc_Slice0_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+0 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice1_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+1 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice2_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+2 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice3_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+3 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice4_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+4 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice5_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+5 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice6_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+6 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice7_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+7 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice8_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+8 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice9_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+9 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice10_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+10)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice11_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+11)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice12_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+12)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice13_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+13)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice14_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+14)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_I_lrx_lb_adc_Slice15_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_i_low[((ptrAdc*16)+1+15)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
        
//         assign ad_Q_lrx_hb_adc_Slice0_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+0 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice1_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+1 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice2_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+2 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice3_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+3 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice4_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+4 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice5_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+5 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice6_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+6 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice7_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+7 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice8_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+8 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice9_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+9 )*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice10_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+10)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice11_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+11)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice12_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+12)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice13_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+13)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice14_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+14)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
//         assign ad_Q_lrx_hb_adc_Slice15_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_high[((ptrAdc*16)+1+15)*NB_SAMPLES - 1 -: NB_SAMPLES]; 
        
//         assign ad_Q_lrx_lb_adc_Slice0_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+0 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice1_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+1 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice2_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+2 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice3_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+3 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice4_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+4 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice5_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+5 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice6_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+6 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice7_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+7 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice8_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+8 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice9_Dout [(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+9 )*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice10_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+10)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice11_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+11)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice12_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+12)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice13_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+13)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice14_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+14)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//         assign ad_Q_lrx_lb_adc_Slice15_Dout[(ptrAdc+1)*NB_SAMPLES - 1 -: NB_SAMPLES] = w_q_low[((ptrAdc*16)+1+15)*NB_SAMPLES - 1 -: NB_SAMPLES] ; 
//     end
// endgenerate

// assign ad_I_lrx_hb_adc_Slice0_Dout  = w_i_high[95   :0   ];   
// assign ad_I_lrx_hb_adc_Slice1_Dout  = w_i_high[191  :96  ];   
// assign ad_I_lrx_hb_adc_Slice2_Dout  = w_i_high[287  :192 ];   
// assign ad_I_lrx_hb_adc_Slice3_Dout  = w_i_high[383  :288 ];   
// assign ad_I_lrx_hb_adc_Slice4_Dout  = w_i_high[479  :384 ];   
// assign ad_I_lrx_hb_adc_Slice5_Dout  = w_i_high[575  :480 ];   
// assign ad_I_lrx_hb_adc_Slice6_Dout  = w_i_high[671  :576 ];   
// assign ad_I_lrx_hb_adc_Slice7_Dout  = w_i_high[767  :672 ];   
// assign ad_I_lrx_hb_adc_Slice8_Dout  = w_i_high[863  :768 ];   
// assign ad_I_lrx_hb_adc_Slice9_Dout  = w_i_high[959  :864 ];   
// assign ad_I_lrx_hb_adc_Slice10_Dout = w_i_high[1055 :960 ];    
// assign ad_I_lrx_hb_adc_Slice11_Dout = w_i_high[1151 :1056];    
// assign ad_I_lrx_hb_adc_Slice12_Dout = w_i_high[1247 :1152];    
// assign ad_I_lrx_hb_adc_Slice13_Dout = w_i_high[1343 :1248];    
// assign ad_I_lrx_hb_adc_Slice14_Dout = w_i_high[1439 :1344];    
// assign ad_I_lrx_hb_adc_Slice15_Dout = w_i_high[1535 :1440];   

// assign ad_I_lrx_lb_adc_Slice0_Dout  = w_i_low[95   :0   ];   
// assign ad_I_lrx_lb_adc_Slice1_Dout  = w_i_low[191  :96  ];   
// assign ad_I_lrx_lb_adc_Slice2_Dout  = w_i_low[287  :192 ];   
// assign ad_I_lrx_lb_adc_Slice3_Dout  = w_i_low[383  :288 ];   
// assign ad_I_lrx_lb_adc_Slice4_Dout  = w_i_low[479  :384 ];   
// assign ad_I_lrx_lb_adc_Slice5_Dout  = w_i_low[575  :480 ];   
// assign ad_I_lrx_lb_adc_Slice6_Dout  = w_i_low[671  :576 ];   
// assign ad_I_lrx_lb_adc_Slice7_Dout  = w_i_low[767  :672 ];   
// assign ad_I_lrx_lb_adc_Slice8_Dout  = w_i_low[863  :768 ];   
// assign ad_I_lrx_lb_adc_Slice9_Dout  = w_i_low[959  :864 ];   
// assign ad_I_lrx_lb_adc_Slice10_Dout = w_i_low[1055 :960 ];    
// assign ad_I_lrx_lb_adc_Slice11_Dout = w_i_low[1151 :1056];    
// assign ad_I_lrx_lb_adc_Slice12_Dout = w_i_low[1247 :1152];    
// assign ad_I_lrx_lb_adc_Slice13_Dout = w_i_low[1343 :1248];    
// assign ad_I_lrx_lb_adc_Slice14_Dout = w_i_low[1439 :1344];    
// assign ad_I_lrx_lb_adc_Slice15_Dout = w_i_low[1535 :1440];    

// assign ad_Q_lrx_hb_adc_Slice0_Dout  = w_q_high[95   :0   ];   
// assign ad_Q_lrx_hb_adc_Slice1_Dout  = w_q_high[191  :96  ];   
// assign ad_Q_lrx_hb_adc_Slice2_Dout  = w_q_high[287  :192 ];   
// assign ad_Q_lrx_hb_adc_Slice3_Dout  = w_q_high[383  :288 ];   
// assign ad_Q_lrx_hb_adc_Slice4_Dout  = w_q_high[479  :384 ];   
// assign ad_Q_lrx_hb_adc_Slice5_Dout  = w_q_high[575  :480 ];   
// assign ad_Q_lrx_hb_adc_Slice6_Dout  = w_q_high[671  :576 ];   
// assign ad_Q_lrx_hb_adc_Slice7_Dout  = w_q_high[767  :672 ];   
// assign ad_Q_lrx_hb_adc_Slice8_Dout  = w_q_high[863  :768 ];   
// assign ad_Q_lrx_hb_adc_Slice9_Dout  = w_q_high[959  :864 ];   
// assign ad_Q_lrx_hb_adc_Slice10_Dout = w_q_high[1055 :960 ];    
// assign ad_Q_lrx_hb_adc_Slice11_Dout = w_q_high[1151 :1056];    
// assign ad_Q_lrx_hb_adc_Slice12_Dout = w_q_high[1247 :1152];    
// assign ad_Q_lrx_hb_adc_Slice13_Dout = w_q_high[1343 :1248];    
// assign ad_Q_lrx_hb_adc_Slice14_Dout = w_q_high[1439 :1344];    
// assign ad_Q_lrx_hb_adc_Slice15_Dout = w_q_high[1535 :1440];    

// assign ad_Q_lrx_lb_adc_Slice0_Dout  = w_q_low[95   :0   ];   
// assign ad_Q_lrx_lb_adc_Slice1_Dout  = w_q_low[191  :96  ];   
// assign ad_Q_lrx_lb_adc_Slice2_Dout  = w_q_low[287  :192 ];   
// assign ad_Q_lrx_lb_adc_Slice3_Dout  = w_q_low[383  :288 ];   
// assign ad_Q_lrx_lb_adc_Slice4_Dout  = w_q_low[479  :384 ];   
// assign ad_Q_lrx_lb_adc_Slice5_Dout  = w_q_low[575  :480 ];   
// assign ad_Q_lrx_lb_adc_Slice6_Dout  = w_q_low[671  :576 ];   
// assign ad_Q_lrx_lb_adc_Slice7_Dout  = w_q_low[767  :672 ];   
// assign ad_Q_lrx_lb_adc_Slice8_Dout  = w_q_low[863  :768 ];   
// assign ad_Q_lrx_lb_adc_Slice9_Dout  = w_q_low[959  :864 ];   
// assign ad_Q_lrx_lb_adc_Slice10_Dout = w_q_low[1055 :960 ];    
// assign ad_Q_lrx_lb_adc_Slice11_Dout = w_q_low[1151 :1056];    
// assign ad_Q_lrx_lb_adc_Slice12_Dout = w_q_low[1247 :1152];    
// assign ad_Q_lrx_lb_adc_Slice13_Dout = w_q_low[1343 :1248];    
// assign ad_Q_lrx_lb_adc_Slice14_Dout = w_q_low[1439 :1344];    
// assign ad_Q_lrx_lb_adc_Slice15_Dout = w_q_low[1535 :1440];    

// always #clk_design_toggle ad_pll_lrx_digclk_div24 <= ~ad_pll_lrx_digclk_div24;


// ################################################################################
// CLOCK LOGGUER THAT IS NOT NEEDED FOR THIS VERSION THAT THE INTERFACE IS OUTSIDE 
// ################################################################################
// Set up the path of the clock logs
// event path_ready;
// string monza_path;
// string logs_path;

// string clk_line_ingress_path;
// string clk_cal_adc_path;
// string clk_line_egress_path;

// initial begin
//     @(hash_updated);
//     monza_path = "/projects/farina16/crn16ffPLUSll_sos/work/ibalbo/farina_tc_dsp/common/MonzaFxp";
//     logs_path = $sformatf("%s/scratch/dsp_rx_test/%s/run/logs", monza_path, hash);

//     clk_cal_adc_path       = {logs_path, "/", "root.u_dsp_rx_h.i_clk_rx_cal_adc.txt"};
//     clk_line_ingress_path  = {logs_path, "/", "root.u_dsp_rx_h.i_line_ingress_clock.txt"};
//     clk_line_egress_path   = {logs_path, "/", "root.u_dsp_rx_h.i_line_egress_clock.txt"};
//     ->path_ready;
// end

// clock_generator_log u_clk_log_ingress(
//     .path(clk_line_ingress_path),
//     .path_ready(path_ready),
//     .clk(ad_pll_lrx_digclk_div24)
// );

// clock_generator_log u_clk_log_cal_adc(
//     .path(clk_cal_adc_path),
//     .path_ready(path_ready),
//     .clk(ad_hi_lrx_calADC_clk)
// );

// clock_generator_log u_clk_log_egress(
//     .path(clk_line_egress_path),
//     .path_ready(path_ready),
//     .clk(i_line_egress_digital_clock)
// );

// assign i_clock_regmap               = ad_pll_lrx_digclk_div24;
// assign ad_hq_lrx_calADC_clk         = ad_hi_lrx_calADC_clk;      
// assign i_clock_netlist              = ad_pll_lrx_digclk_div24;
// assign ad_I_lrx_hb_adc_CLK_even[0]  = ad_pll_lrx_digclk_div24;

// integer file;

//  initial begin
//         // Open file for writing
//         file = $fopen("/projects/farina16/crn16ffPLUSll_sos/work/ibalbo/farina_tc_dsp/modules/dsp_rx/verification/testbench/output_log.txt", "w");
//         if (file == 0) begin
//             $display("Failed to open file");
//             $stop;
//         end
// end

// always @(posedge ad_pll_lrx_digclk_div24) begin
//     $fwrite(file, "%d\n",o_dsp_rx_hi);
// end

// initial begin
//     #500;  // Run simulation for 500ns
//     $fclose(file);
//     $display("Simulation complete, log written to output_log.txt");
//     $stop;
// end

