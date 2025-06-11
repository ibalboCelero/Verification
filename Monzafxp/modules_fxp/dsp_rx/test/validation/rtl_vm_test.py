################################################################################
# Verification File
################################################################################
# PYTHON MODULES
################################################################################

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal  as sp
import sys
import os
################################################################################
# HALCON MODULES
################################################################################

from halcon import SimulatorHandler
from halcon import Options
from halcon import Parameter
from halcon import Case
from halcon import Test
from halcon.command_handler import *
from modules_fxp.afifo.tests.afifo_cpi import *

################################################################################
# VALIDATION UTILS
################################################################################
from config_utils import *
from regmap import *
from global_parameters import *
from log_utils_rx import *
from log_utils_simplistic import log_simplistic_stim
from conf.default_paths import DefaultPaths
from log_rx_rtl import *
################################################################################
# Processing file
################################################################################

processing_dir = ["datapath_validation_plot.py"]

################################################################################
# Module to test
################################################################################

module_folder     = "modules_fxp"
module_to_test    = "dsp_rx"
tb_dsp_rx         = "tb_rtl_vm"
aux_module_folder = "modules_fxp"
aux_modules       = ["rx_comp_eq","rx_comp_adap","rx_comp_lms","synchronizer_single_bit", "rx_fifo",
                     "rx_mux","rx_regressor","rx_mux_1s","rx_equalizer",
                     "rx_fir","interface_ADC_DIG","top_rx_correlator",
                     "correlator","FSM_rx","adc_gain_offset","adc_offset_n",
                     "adc_offset","adc_gain_top","adc_gain_0","adc_gain_n","rx_mux_register",
                     "adc_gain","counter","rx_scfsm","afifo","afifo_cal_adc_wraper","datapath_interface_single_reset",
                     "dsp_rx_regmap","serial_to_parallel","parallel_to_serial",
                     "converterd2s","loopback_rx_top","loopback_rx","rx_bypass_samples","rx_dig_adc"]
modules_fp        = ["stimulus_adc_2_ports","continuous_time_filter"]
analog_models     = [""]
# analog_models     = ["channel","channel_wrapper","noise_loading","carrier_error","analog_agc",
#                      "dac","adc","afe_tx_fi","afe_rx_fi"]
################################################################################
# COMMAND LINE OPTIONS
################################################################################

args = Options.args()

#######################################
# SIMULATOR
#######################################

simh = SimulatorHandler()
simh, paths = init_usim(args, simh, module_folder, module_to_test, tb_dsp_rx, aux_module_folder, aux_modules,modules_fp=modules_fp,analog_models=analog_models)

#######################################
# RTL TEST CASES
#######################################
# Above this code, copy from any other test made by system team
test = Test (
    name = "dsp_rx_test", 
    base_dir = f"{DefaultPaths.scratch_dir}",
    parameters = Parameter.list()
)

test.__memory_limit = 50e3

# Matrix generation
mode                        = [1, 0, 2]
#                               0,8,16        1,9,17      2,10,18   3,11,19  4,12,20  5,13,21 6,14,22  7,15,23
testcase_name               = ["DSPInBypass","LpInBypass","Noise\t","Offset","Gain\t","Eq\t","All\t","All Noise"]
rx_comp_eq_mu_lms           = [0            ,0           ,0        ,0       ,0       ,255   ,255    ,255        ]
adc_offset_alpha            = [63           ,63          ,63       ,32      ,32      ,63    ,32     ,32         ]
max_count_cal_gain_offset   = [20           ,20          ,20       ,17000   ,17000   ,20    ,17000  ,17000      ]
data_input_dsp              = [1            ,0           ,1        ,0       ,0       ,0     ,0      ,1          ] # 0 send zero 1 dsp in
data_input_lp_noise         = [0            ,1           ,2        ,1       ,1       ,1     ,1      ,2          ] # 0 send zero 1 tx out 2 send noise
CORR_LEN                    = [324          ,324         ,324      ,324     ,324     ,2000  ,2000   ,2000       ] # 
gain_sel                    = [1            ,1           ,1        ,1       ,0       ,1     ,0      ,0          ] # 
offset_sel                  = [1            ,1           ,1        ,0       ,1       ,1     ,0      ,0          ] # 
caseMatrix = []

for md in mode:
    for i in range(len(rx_comp_eq_mu_lms)):
        caseMatrix.append(
            [md,                            # 0                
             rx_comp_eq_mu_lms[i],          # 1                               
             adc_offset_alpha[i],           # 2                               
             max_count_cal_gain_offset[i],  # 3                                       
             data_input_dsp[i],             # 4                               
             data_input_lp_noise[i],        # 5                               
             CORR_LEN[i],                   # 6
             gain_sel[i],                   # 7
             offset_sel[i]                  # 8
             ])

print(f"\n-----------------------------------  CASE MATRIX  ----------------------------------")
print(f"{'Case':<6} {'FullRate':<9} {'Mu':<5} {'Alpha':<7} {'Count_G_O':<10} {'DSP_in':<8} {'LP_in':<8} {'Corr_len':<9} {'Gain_sel':<8} {'offset_sel':<8}")

for idx, row in enumerate(caseMatrix):
    print(f"{idx:<6} {row[0]:<9} {row[1]:<5} {row[2]:<7} {row[3]:<10} {row[4]:<8} {row[5]:<8} {row[6]:<9} {row[7]:<8} {row[8]:<8}")

case_number = Parameter(
    name            = 'root.case_number',
    text            = 'dsp_rx_case_number_{:.0f}',
    alpha           = 1,
    value           = np.arange(len(caseMatrix)).tolist()
)

for i,case_num in enumerate(case_number):
    if i==5: # use this if to run a specific test  
        
        print(f"\n# # # # # # Test Case Number ", i, " Name: ", end="  ")
        print(testcase_name[i%8], end="")
        print(f"  in", end=" ")
        if caseMatrix[i][0]:
            print("FULL RATE")
        else:
            print("HALF RATE")
        print(f"\n-----------------------------------  CASE MATRIX  ----------------------------------")
        print(f"{'Case':<6} {'FullRate':<9} {'Mu':<5} {'Alpha':<7} {'Count_G_O':<10} {'DSP_in':<8} {'LP_in':<8} {'Corr_len':<9} {'Gain_sel':<8} {'Offset_sel':<8}")
        print(f"{i:<6} {caseMatrix[i][0]:<9} {caseMatrix[i][1]:<5} {caseMatrix[i][2]:<7} {caseMatrix[i][3]:<10} {caseMatrix[i][4]:<8} {caseMatrix[i][5]:<8} {caseMatrix[i][6]:<9} {caseMatrix[i][7]:<8} {caseMatrix[i][8]:<8}")

        # Create Case
        case = Case(simh,mode='E1',group='G0')
        # Add Parameters
        case.add(case_num   )

        # Simulation taps
        case.settings['root']['enable_log'             ] = 1
        case.settings['root']['n_iterations'           ] = 1000 + caseMatrix[i][3] + caseMatrix[i][6] #20000
        case.settings['root']['logger_buffer_size'     ] = 1000

        # Configure DSP
        set_clocks_simplistic_case(case)

        # Select DSP input
        case.settings['root']['data_input_dsp'         ] = caseMatrix[i][4]
        case.settings['root']['data_input_lp_noise'    ] = caseMatrix[i][5]


        REGMAP_TOTAL = regMap().get_regMap()

        REGMAP = {
                "global": REGMAP_TOTAL["global"],
                "u_dsp_rx_h": REGMAP_TOTAL["u_phy_core"]["u_dsp_rx_h"]
            }

        # Case Regmap value
        REGMAP["global"]["RM_STATIC_MODE"]                                                     = caseMatrix[i][0]

        REGMAP["u_dsp_rx_h"]["u_rx_comp_eq_hi"]["RM_RX_COMP_EQ_HI_MU_LMS"]                     = caseMatrix[i][1]
        REGMAP["u_dsp_rx_h"]["u_rx_comp_eq_hq"]["RM_RX_COMP_EQ_HQ_MU_LMS"]                     = caseMatrix[i][1]
        REGMAP["u_dsp_rx_h"]["u_rx_adc_gain_offset_hi"]["RM_RX_ADC_OFFSET_ALPHA_HI"]           = caseMatrix[i][2]
        REGMAP["u_dsp_rx_h"]["u_rx_adc_gain_offset_hq"]["RM_RX_ADC_OFFSET_ALPHA_HQ"]           = caseMatrix[i][2]
        REGMAP["u_dsp_rx_h"]["u_rx_adc_gain_offset_hi"]["RM_RX_ADC_AGC_GAIN_SEL_HI"]           = caseMatrix[i][7]
        REGMAP["u_dsp_rx_h"]["u_rx_adc_gain_offset_hq"]["RM_RX_ADC_AGC_GAIN_SEL_HQ"]           = caseMatrix[i][7]
        REGMAP["u_dsp_rx_h"]["u_rx_correlator_hi"]["RM_RX_CORR_HI_CORRELATION_LENGTH"]         = caseMatrix[i][6]
        REGMAP["u_dsp_rx_h"]["u_rx_correlator_hq"]["RM_RX_CORR_HQ_CORRELATION_LENGTH"]         = caseMatrix[i][6]
        REGMAP["u_dsp_rx_h"]["u_rx_scfsm"]["RM_STATIC_RX_SCFSM_MAX_CTER_CAL_GAIN_OFFSET_DONE"] = caseMatrix[i][3]

        # Loopback reset
        REGMAP["u_dsp_rx_h"]["u_rx_loopback_hi"]["RM_STATIC_RX_LP_HI_SRST"] = 1
        REGMAP["u_dsp_rx_h"]["u_rx_loopback_hq"]["RM_STATIC_RX_LP_HQ_SRST"] = 1

        # AFIFO Loopback delay
        REGMAP["u_dsp_rx_h"]["u_afifo_loopback_hi"]["RM_STATIC_RX_AFIFO_LP_HI_VALID_DELAY"] = 3
        REGMAP["u_dsp_rx_h"]["u_afifo_loopback_hq"]["RM_STATIC_RX_AFIFO_LP_HQ_VALID_DELAY"] = 3

        REGMAP["u_dsp_rx_h"]["u_afifo_loopback_hi"]["RM_STATIC_RX_AFIFO_LP_HI_WRITE_POINTER_RESET_VALUE"] = 3
        REGMAP["u_dsp_rx_h"]["u_afifo_loopback_hq"]["RM_STATIC_RX_AFIFO_LP_HQ_WRITE_POINTER_RESET_VALUE"] = 3

        REGMAP["u_dsp_rx_h"]["u_afifo_loopback_hi"]["RM_RX_AFIFO_LP_HI_WRITE_RESET"] = 1
        REGMAP["u_dsp_rx_h"]["u_afifo_loopback_hq"]["RM_RX_AFIFO_LP_HQ_WRITE_RESET"] = 1
        REGMAP["u_dsp_rx_h"]["u_afifo_loopback_hi"]["RM_RX_AFIFO_LP_HI_READ_RESET"]  = 1
        REGMAP["u_dsp_rx_h"]["u_afifo_loopback_hq"]["RM_RX_AFIFO_LP_HQ_READ_RESET"]  = 1

        # Mu equal zero to bypass comp_eq samples
        if caseMatrix[i][1] == 0:
            cg_coeffs_init = np.zeros(RX_COMP_EQ_N_PHASES*RX_COMP_EQ_N_COEFFS)
            cg_coeffs_init[int(RX_COMP_EQ_N_COEFFS-1)::int(RX_COMP_EQ_N_COEFFS)] = -1
            rx_comp_eq_coeffs_init = cg_coeffs_init.tolist()
            REGMAP["u_dsp_rx_h"]["u_rx_comp_eq_hi"]["RM_RX_COMP_EQ_HI_COEFFS_INIT"]                     = rx_comp_eq_coeffs_init
            REGMAP["u_dsp_rx_h"]["u_rx_comp_eq_hq"]["RM_RX_COMP_EQ_HQ_COEFFS_INIT"]                     = rx_comp_eq_coeffs_init

        case.chip_config.set_u_dsp_rx_h(REGMAP=REGMAP,hierarchy=0)     
        case.chip_config.set_gain_offset_bypass(hierarchy='')
        
        # Stim config
        set_stim_config(case)
        set_cal_adc(case)

        # Enable Regmap
        case.set_value(1 , "root.dsp_rx_regmap_enable", "root.line_ingress_clock", "p", 100, 0)

        # Release Reset
        case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_rst_n"  , "root.line_ingress_clock", "p", 200, 0)
        case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_enable" , "root.line_ingress_clock", "p", 200, 0)
        case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_static_rx_lp_hi_enable"      , "root.line_ingress_clock", "p", 10*384, 0)
        case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_static_rx_lp_hi_srst"        , "root.line_ingress_clock", "p", 10*384, 0)
        case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_static_rx_lp_hq_enable"      , "root.line_ingress_clock", "p", 10*384, 0)
        case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_static_rx_lp_hq_srst"        , "root.line_ingress_clock", "p", 10*384, 0)
        case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_static_rx_lp_hi_corr_sel"    , "root.line_ingress_clock", "p", 10*384, 0)
        case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_static_rx_lp_hq_corr_sel"    , "root.line_ingress_clock", "p", 10*384, 0)
        case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_afifo_lp_hq_write_reset"  , "root.line_ingress_clock", "p", 10*384, 0)
        case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_afifo_lp_hq_read_reset"   , "root.line_ingress_clock", "p", 10*384, 0)
        case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_afifo_lp_hi_write_reset"  , "root.line_ingress_clock", "p", 10*384, 0)
        case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_afifo_lp_hi_read_reset"   , "root.line_ingress_clock", "p", 10*384, 0)

        # if bypass
        if caseMatrix[i][7]==1:
            case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_sel_rx_gain_hi_enable"            , "root.line_ingress_clock", "p", 384*10, 0)
            case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_sel_rx_gain_hq_enable"            , "root.line_ingress_clock", "p", 384*10, 0)
            case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_ovr_rx_gain_hi_enable"            , "root.line_ingress_clock", "p", 384*10, 0)
            case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_ovr_rx_gain_hq_enable"            , "root.line_ingress_clock", "p", 384*10, 0)
        if caseMatrix[i][8]==1:
            case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_sel_rx_offset_hi_enable"            , "root.line_ingress_clock", "p", 384*10, 0)
            case.set_value(1 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_sel_rx_offset_hq_enable"            , "root.line_ingress_clock", "p", 384*10, 0)
            case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_ovr_rx_offset_hi_enable"            , "root.line_ingress_clock", "p", 384*10, 0)
            case.set_value(0 , "root.u_dsp_rx_h.u_dsp_rx_regmap.rm_rx_scfsm_ovr_rx_offset_hq_enable"            , "root.line_ingress_clock", "p", 384*10, 0)



        # # Add logs
        log_rtl(case = case, STEP=1, hierarchy = 0, simh=simh)
        log_afifo_lp(case = case, STEP=1, hierarchy = 0, simh=simh)
        log_dsp_rx_rm(case, simh, STEP=1,END_LOG_RM=0)
        
        # Add to Test
        case = test.add(case)

test.save_cases()

#######################################
# COMMAND HANDLER
#######################################
test_handler(args, test, processing_dir)
