/* Includes */
#include "halcon.hpp"
#include "ac_fixed.h"
#include <fstream>
#include "stimulus_adc_2_ports.hpp"
#include "continuous_time_filter.hpp"
#include "dsp_rx_defines.hpp"
/* Module to test */
#include "dsp_rx.hpp"
#include "converterd2s.hpp"
#include "parallel_to_serial.hpp"


class Root : public Simulator
{
public:

    Root();

private:

    /* FIXED POINT
        W: integer representing width of the type
        I: integer representing integer width
        S: bool parameter representing signedness
        Q: enumeration parameter for quantization
        O: enumeration parameter for overflow modes
    */

    /* User methods */
    void Init() override;
    void Connect() override;
    void Iteration() override;
    bool ContinueRunning() override;
    void Terminate() override;

    /* Variables */

    /* Settings YAML */
    bool enable_log       { false };
    size_t n_iterations   { 100 };
    long double fs_channel { 4 };

    long unsigned int line_egress_clock_fnum  {1};
    long unsigned int line_egress_clock_fden  {1};
    long unsigned int line_ingress_clock_fnum {1};
    long unsigned int line_ingress_clock_fden {1};
    long unsigned int clk_rx_adc_sr_fnum {1};
    long unsigned int clk_rx_adc_sr_fden {1};
    long unsigned int rx_cal_adc_fden {1};
    long unsigned int rx_cal_adc_fnum {1};

    Dsp_Rx  u_dsp_rx_h;
    StimulusTwoPorts<RX_COMP_EQ_INPUT> u_stim_hi;
    StimulusTwoPorts<RX_COMP_EQ_INPUT> u_stim_hq;
    ContinuousTimeFilter u_hCalADC_xi;
    ContinuousTimeFilter u_hCalADC_xq;

    std::array<T_IN_TRN_NOISE_LOOPBACK_RX,RX_COMP_EQ_IN_PARALLELISM>     dsp_rx_hi {0};
    std::array<T_IN_TRN_NOISE_LOOPBACK_RX,RX_COMP_EQ_IN_PARALLELISM>     dsp_rx_hq {0};

    ParallelToSerial<RX_COMP_EQ_INPUT, double, RX_COMP_EQ_IN_PARALLELISM> u_parallel_to_serial_hi;
    ParallelToSerial<RX_COMP_EQ_INPUT, double, RX_COMP_EQ_IN_PARALLELISM> u_parallel_to_serial_hq;

    Converterd2s <double, AFIFO_RX_CAL_ADC> u_cd2f_rx_cal_adc_hi;
    Converterd2s <double, AFIFO_RX_CAL_ADC> u_cd2f_rx_cal_adc_hq;

    /* Clocks */
    Clock line_egress_clock;
    Clock line_ingress_clock;
    Clock clk_adc_serial;
    Clock clk_rx_cal_adc;
    Clock clk_analog;

    bool    dsp_rx_regmap_enable;

    // VERIFICATION
    int case_number;
    int data_input_dsp      ;
    int data_input_lp_noise ;

    std::array<RX_COMP_EQ_INPUT,RX_COMP_EQ_IN_PARALLELISM/2> dsp_rx_zero {0};
    
    std::array<T_IN_TRN_NOISE_LOOPBACK_RX,RX_COMP_EQ_IN_PARALLELISM>     input_lp_signal_txi  {0};
    std::array<T_IN_TRN_NOISE_LOOPBACK_RX,RX_COMP_EQ_IN_PARALLELISM>     input_lp_signal_txq  {0};
    std::array<T_IN_TRN_NOISE_LOOPBACK_RX,RX_COMP_EQ_IN_PARALLELISM>     zero_noise  {0};
    std::array<T_IN_TRN_NOISE_LOOPBACK_RX,RX_COMP_EQ_IN_PARALLELISM>     known_noise {0};

};
