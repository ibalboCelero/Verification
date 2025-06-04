/* Includes */
#include "halcon.hpp"
#include "ac_fixed.h"
#include <fstream>

#include "tb_rtl_vm.hpp"
Root::Root()
{
    /* Clocks */
    REFLECT(line_ingress_clock);
    REFLECT(line_egress_clock);
    REFLECT(clk_rx_cal_adc);
    REFLECT(clk_adc_serial);
    REFLECT(clk_analog);

    /* Modules */
    REFLECT(u_dsp_rx_h);
    REFLECT(u_stim_hi);
    REFLECT(u_stim_hq);
    REFLECT(u_hCalADC_xi);
    REFLECT(u_hCalADC_xq);
    REFLECT(u_cd2f_rx_cal_adc_hi);
    REFLECT(u_cd2f_rx_cal_adc_hq);
    REFLECT(u_parallel_to_serial_hi);
    REFLECT(u_parallel_to_serial_hq);

    /* Settings YAML */
    REFLECT_YAML(enable_log);
    REFLECT_YAML(n_iterations);
    REFLECT_YAML(fs_channel);


    REFLECT_YAML(line_egress_clock_fnum );
    REFLECT_YAML(line_egress_clock_fden );
    REFLECT_YAML(line_ingress_clock_fnum);
    REFLECT_YAML(line_ingress_clock_fden);
    REFLECT_YAML(clk_rx_adc_sr_fnum     );
    REFLECT_YAML(clk_rx_adc_sr_fden     );
    REFLECT_YAML(rx_cal_adc_fden        );
    REFLECT_YAML(rx_cal_adc_fnum        );
    REFLECT_YAML(dsp_rx_regmap_enable   );


    // Verification
    REFLECT_YAML(data_input_dsp);
    REFLECT_YAML(data_input_lp_noise);
    REFLECT_YAML(case_number);

}

void Root::Connect()
{
    /* Scheduler */
    /* Analog */
    clk_analog.i_frequency_hz << fs_channel;
    clk_analog.i_phase_deg.SetData(0);
    clk_analog.i_division_factor_num.SetData(1);
    clk_analog.i_division_factor_den.SetData(1);

    clk_cmd_handler << clk_analog;
    clk_cmd_handler.i_phase_deg.SetData(0);
    clk_cmd_handler.i_division_factor_num.SetData(1);
    clk_cmd_handler.i_division_factor_den.SetData(1);

    /* LRX Clokc */
    line_egress_clock         << clk_analog;
    line_egress_clock.i_phase_deg.SetData(0);
    line_egress_clock.i_division_factor_num << line_egress_clock_fnum;
    line_egress_clock.i_division_factor_den << line_egress_clock_fden;

    line_ingress_clock        << clk_analog;
    line_ingress_clock.i_phase_deg.SetData(0);
    line_ingress_clock.i_division_factor_num << line_ingress_clock_fnum;
    line_ingress_clock.i_division_factor_den << line_ingress_clock_fden;

    clk_adc_serial          << clk_analog;
    clk_adc_serial.i_phase_deg.SetData(0);
    clk_adc_serial.i_division_factor_num << clk_rx_adc_sr_fnum;
    clk_adc_serial.i_division_factor_den << clk_rx_adc_sr_fden;

    /* Rx CAL ADC */
    clk_rx_cal_adc            << clk_analog;
    clk_rx_cal_adc.i_phase_deg.SetData(0);
    clk_rx_cal_adc.i_division_factor_num << rx_cal_adc_fnum;
    clk_rx_cal_adc.i_division_factor_den << rx_cal_adc_fden;

    /* Modules */
    // Stimulus
    u_stim_hi.i_clock << line_ingress_clock;
    u_stim_hq.i_clock << line_ingress_clock;

    // Cal ADC XI interp
    u_parallel_to_serial_hi.i_mode.SetData(1);
    u_parallel_to_serial_hi.i_clock_fast    << clk_adc_serial;
    u_parallel_to_serial_hi.i_parallel      << u_stim_hi.o_parallel;

    u_hCalADC_xi.i_signal << u_parallel_to_serial_hi.o_serial;
    u_hCalADC_xi.i_clock_input << clk_adc_serial;
    u_hCalADC_xi.i_clock_output << clk_rx_cal_adc;

    u_cd2f_rx_cal_adc_hi.i_clock                 << clk_rx_cal_adc;    
    u_cd2f_rx_cal_adc_hi.i_data                  << u_hCalADC_xi.o_signal;
    
    // Cal ADC XQ interp
    u_parallel_to_serial_hq.i_mode.SetData(1);
    u_parallel_to_serial_hq.i_clock_fast    << clk_adc_serial;
    u_parallel_to_serial_hq.i_parallel      << u_stim_hq.o_parallel;

    u_hCalADC_xq.i_signal << u_parallel_to_serial_hq.o_serial;
    u_hCalADC_xq.i_clock_input << clk_adc_serial;
    u_hCalADC_xq.i_clock_output << clk_rx_cal_adc;

    u_cd2f_rx_cal_adc_hq.i_clock                 << clk_rx_cal_adc;    
    u_cd2f_rx_cal_adc_hq.i_data                  << u_hCalADC_xq.o_signal;

    // DSP Rx
    u_dsp_rx_h.i_line_ingress_clock << line_ingress_clock;
    u_dsp_rx_h.i_clk_rx_cal_adc << clk_rx_cal_adc;
    u_dsp_rx_h.i_line_egress_clock << line_egress_clock;

    u_dsp_rx_h.i_dsp_rx_regmap_enable << dsp_rx_regmap_enable;
    u_dsp_rx_h.i_dsp_rx_hi_cal_adc << u_cd2f_rx_cal_adc_hi.o_data;
    u_dsp_rx_h.i_dsp_rx_hq_cal_adc << u_cd2f_rx_cal_adc_hq.o_data;

    // DSP INPUT 
    if(data_input_dsp){
        u_dsp_rx_h.i_dsp_rx_hi_high  << u_stim_hi.o_parallel_high;//             << u_serial_to_parallel_xi_high.o_parallel;
        u_dsp_rx_h.i_dsp_rx_hi_low   << u_stim_hi.o_parallel_low;//             << u_serial_to_parallel_xi_low.o_parallel ; 
        u_dsp_rx_h.i_dsp_rx_hq_high  << u_stim_hq.o_parallel_high;//             << u_serial_to_parallel_xq_high.o_parallel;
        u_dsp_rx_h.i_dsp_rx_hq_low   << u_stim_hq.o_parallel_low;//             << u_serial_to_parallel_xq_low.o_parallel ; 
    }
    else {
        u_dsp_rx_h.i_dsp_rx_hi_high               << dsp_rx_zero;
        u_dsp_rx_h.i_dsp_rx_hi_low                << dsp_rx_zero; 
        u_dsp_rx_h.i_dsp_rx_hq_high               << dsp_rx_zero;
        u_dsp_rx_h.i_dsp_rx_hq_low                << dsp_rx_zero; 
    }
    
    // LOOPBACK INPUT
    if (data_input_lp_noise == 0) {

        u_dsp_rx_h.i_dsp_rx_lp_hi             << zero_noise; // Zero
        u_dsp_rx_h.i_dsp_rx_lp_hq             << zero_noise; // Zero 

    }
    else if (data_input_lp_noise == 1) {

        u_dsp_rx_h.i_dsp_rx_lp_hi             << input_lp_signal_txi;
        u_dsp_rx_h.i_dsp_rx_lp_hq             << input_lp_signal_txq;

    }
    else if (data_input_lp_noise == 2) {

        u_dsp_rx_h.i_dsp_rx_lp_hi           << known_noise;
        u_dsp_rx_h.i_dsp_rx_lp_hq           << known_noise; 

    }

};

void Root::Init()
{
    dsp_rx_zero.fill(-1);
    zero_noise.fill(0);
    known_noise.fill(2);
    /* Pass */
    std::cout << "INIT Root" << std::endl;
}

void Root::Iteration()
{
    unsigned long lastPrinted = -1; // Track the last printed value
    unsigned long c_iteration = line_ingress_clock.GetTickCount();
    if (!(c_iteration % 500) && enable_log && c_iteration != lastPrinted)
    {
        lastPrinted = c_iteration;
        std::cout << "-- Running: " << c_iteration << "/" << n_iterations << std::endl;
    }

    // std::cout<<"Line ingress: " <<line_egress_clock.GetFrequency();
    // std::cout<<"Line egress: "<<line_ingress_clock.GetFrequency();
    // std::cout<<"Line adc serial: "<<clk_adc_serial.GetFrequency();
    // std::cout<<"Line adc cal: "<<clk_rx_cal_adc.GetFrequency();
    // std::cout<<"Line analog: "<<clk_analog.GetFrequency();
}

bool Root::ContinueRunning()
{
    return line_ingress_clock.GetTickCount() <= n_iterations;
}

void Root::Terminate()
{

    std::cout << std::endl;
    std::cout << "-----------------------------" << std::endl;
    std::cout << "-- Simulation sample rate [kbps]: " << (GetIterationRate()) << std::endl;
    std::cout << "-----------------------------" << std::endl;

}
