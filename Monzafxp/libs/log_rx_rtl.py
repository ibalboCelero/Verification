# Processing file
def log_rtl(case, simh, STEP=1, hierarchy = 0):
    if (hierarchy):
        hierarchy_str = '.u_phy_core'
    else:
        hierarchy_str = ''

# FSM
    case.log("root.u_dsp_rx_h.u_rx_scfsm.r_current_state.o", "root.line_ingress_clock", edge = "p", begin = 0, step = STEP,  end = 0, file_type = "t", file_name_type = simh.SHORT, format = simh.UINT)


    for lane in ['i','q']:
        LOGS = [

# LOOPBACK
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_rm_enable",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_rm_srst",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_rm_static_corr_sel",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_afifo_loopback_rx_valid",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_afifo_valid",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_rm_static_cnt_ph",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_rm_static_fifo_rp",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_signal",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_noise",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.i_analog_sample",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.o_signal",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.o_corr",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_loopback_h{lane}.o_valid",

# GAIN OFFSET
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_adc_gain_offset_h{lane}.i_samples",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_adc_gain_offset_h{lane}.o_samples",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_adc_gain_offset_h{lane}.i_enable_offset",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_adc_gain_offset_h{lane}.i_enable_gain",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_adc_gain_offset_h{lane}.i_rm_static_alpha",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_adc_gain_offset_h{lane}.i_rm_static_gain_sel",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_adc_gain_offset_h{lane}.i_rm_static_agc_gain",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_adc_gain_offset_h{lane}.i_rm_static_adc_ref",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_adc_gain_offset_h{lane}.i_srst",

# EQUALIZER
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.o_rx_comp_eq_samples",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.o_sample_to_correlator",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_samples",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_error",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_lms_eq_mux_index_in",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_R_counter",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_phase_counter",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_rm_static_taps",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_rm_static_offset",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_rm_static_mu",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_rm_static_afifo_delay",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_rm_static_taps_leakage",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_rm_static_offset_leakage",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_eq_enable",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_lms_enable",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_comp_eq_h{lane}.i_srst",


# CORRELATOR
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_signal",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_afifo",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_enable",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_enable_correlator",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_srst",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_valid_afifo",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_rm_static_data_path_fifo_ptr",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_rm_static_afifo_delay",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_rm_static_correlation_length",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_rm_static_bypass_correlator",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_rm_static_delay",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_rm_static_phase",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_rm_static_reference_coef",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.i_init_correlation",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.o_error",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.o_done",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.o_skip_condition",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.o_lms_eq_mux_index_in",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.o_lms_eq_mux_index_out",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.o_lms_eq_kernel_to_update",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_correlator_h{lane}.o_lms_eq_enable",

# FSM
            f"root.u_dsp_rx_h.u_rx_scfsm.i_rx_corr_h{lane}_done",
            f"root.u_dsp_rx_h.u_rx_scfsm.i_rx_afifo_cal_adc_h{lane}_valid",
            f"root.u_dsp_rx_h.u_rx_scfsm.i_rx_datapath_fifo_h{lane}_valid",

# OTHER
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_datapath_fifo_h{lane}.o_high",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_datapath_fifo_h{lane}.o_low",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_datapath_fifo_h{lane}.o_valid",

            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_dig_adc_h{lane}.o_samples",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_dig_adc_h{lane}.o_rx_cal_adc",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_dig_adc_h{lane}.o_afifo_valid",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_dig_adc_h{lane}.o_datapath_interface_valid",

            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_afifo_cal_adc_h{lane}.o_read_data_single",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_afifo_cal_adc_h{lane}.o_valid",

            f"root{hierarchy_str}.u_dsp_rx_h.u_afifo_loopback_h{lane}.i_low",
            f"root{hierarchy_str}.u_dsp_rx_h.u_afifo_loopback_h{lane}.i_high",
            f"root{hierarchy_str}.u_dsp_rx_h.u_afifo_loopback_h{lane}.o_low",
            f"root{hierarchy_str}.u_dsp_rx_h.u_afifo_loopback_h{lane}.o_high",

            #f"root.u_dsp_rx_h.u_rx_comp_eq_h{lane}.u_rx_equalizer.u_rx_ADC_DIG.o_current_samples",

            f"root{hierarchy_str}.u_dsp_rx_h.i_dsp_rx_lp_h{lane}",
            f"root{hierarchy_str}.u_dsp_rx_h.o_dsp_rx_h{lane}",
            f"root{hierarchy_str}.u_dsp_rx_h.u_rx_bypass_samples_h{lane}.o_rx_bypass_samples"
        ]
        case.log(LOGS, "root.line_ingress_clock", edge = "p", begin = 0, step = STEP,  end = 0, file_type = "t", file_name_type = simh.SHORT, format = simh.UINT)

def log_afifo_lp(case, simh, STEP=1, hierarchy = 0):
    if (hierarchy):
        hierarchy_str = '.u_phy_core'
    else:
        hierarchy_str = ''

    for lane in ['i','q']:
        LOGS = [
            f"root{hierarchy_str}.u_dsp_rx_h.u_afifo_loopback_h{lane}.o_valid",
        ]
        case.log(LOGS, "root.line_ingress_clock", edge = "p", begin = 0, step = STEP,  end = 0, file_type = "t", file_name_type = simh.SHORT, format = simh.UINT)


# FIXME: MANUALLY ADDED
def log_dsp_rx_rm(case, simh, STEP=1,END_LOG_RM=0):
    case.log(signals = [f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_rst_n',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_enable',                                     
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_scfsm_max_cter_r_datapath',                 
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_scfsm_max_cter_load_coeff',                 
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_scfsm_max_cter_cal_gain_offset_done',       
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_force_state',                                
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_state',                                  
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_comp_eq_hi_srst',                     
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_comp_eq_hq_srst',                     
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_corr_hi_srst',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_corr_hq_srst',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_gain_offset_hi_srst',                 
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_gain_offset_hq_srst',                 
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_datapath_fifo_hi_srst',            
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_datapath_fifo_hq_srst',            
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_afifo_cal_adc_hi_srst',            
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_afifo_cal_adc_hq_srst',            
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_comp_eq_hi_enable',                   
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_comp_eq_hq_enable',                   
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_corr_hi_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_corr_hq_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_corr_hi_enable_correlator',           
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_corr_hq_enable_correlator',           
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_corr_hi_init',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_corr_hq_init',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_gain_hi_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_gain_hq_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_offset_hi_enable',                    
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_offset_hq_enable',                    
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_comp_eq_hi_srst',                     
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_comp_eq_hq_srst',                     
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_corr_hi_srst',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_corr_hq_srst',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_gain_offset_hi_srst',                 
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_gain_offset_hq_srst',                 
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_datapath_fifo_hi_srst',            
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_datapath_fifo_hq_srst',            
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_afifo_cal_adc_hi_srst',            
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_afifo_cal_adc_hq_srst',            
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_comp_eq_hi_enable',                   
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_comp_eq_hq_enable',                   
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_corr_hi_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_corr_hq_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_corr_hi_enable_correlator',           
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_corr_hq_enable_correlator',           
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_corr_hi_init',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_corr_hq_init',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_gain_hi_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_gain_hq_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_offset_hi_enable',                    
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_offset_hq_enable',                    

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_loopback_hi_srst',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_loopback_hq_srst', 
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_loopback_hi_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_loopback_hq_enable', 
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_loopback_hi_srst',                        
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_loopback_hq_srst', 
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_loopback_hi_enable',                      
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_loopback_hq_enable', 

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_digadc_hi_srst',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_digadc_hq_srst',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_digadc_hi_enable',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_sel_rx_digadc_hq_enable',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_digadc_hi_srst',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_digadc_hq_srst',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_digadc_hi_enable',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_scfsm_ovr_rx_digadc_hq_enable',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_mode',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hi_coeffs_init',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hi_offset_init',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hi_mu_lms',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hi_afifo_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hi_taps_leakage',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hi_offset_leakage',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hq_coeffs_init',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hq_offset_init',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hq_mu_lms',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hq_afifo_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hq_taps_leakage',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hq_offset_leakage',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hi_cal_adc_fir_taps',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_comp_eq_hq_cal_adc_fir_taps',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_afifo_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_correlation_length',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_bypass_correlator',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_phase',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_reference_coef',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_data_path_fifo_ptr',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_afifo_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_correlation_length',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_bypass_correlator',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_phase',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_reference_coef',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_data_path_fifo_ptr',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_ovr_tap_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_ovr_tap_value',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_ovr_tap',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_ovr_tap',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hi_reference_offset',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_corr_hq_reference_offset',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_cal_adc_hi_afifo_valid_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_cal_adc_hi_read_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_cal_adc_hi_write_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_cal_adc_hq_afifo_valid_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_cal_adc_hq_read_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_cal_adc_hq_write_pointer_reset_value',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_dp_fifo_hi_valid_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_dp_fifo_hi_read_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_dp_fifo_hi_write_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_adc_ref_hi',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_dp_fifo_hq_valid_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_dp_fifo_hq_read_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_dp_fifo_hq_write_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_adc_ref_hq',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_adc_offset_alpha_hi',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_adc_agc_gain_sel_hi',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_adc_agc_gain_hi',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_adc_offset_alpha_hq',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_adc_agc_gain_sel_hq',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_adc_agc_gain_hq',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hi_enable',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hi_srst',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hi_corr_sel',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hi_cnt_ph',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hi_fifo_rp',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hq_enable',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hq_srst',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hq_corr_sel',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hq_cnt_ph',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_lp_hq_fifo_rp',

                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_lp_hi_valid_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_lp_hi_read_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_lp_hi_write_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_afifo_lp_hi_write_reset',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_afifo_lp_hi_read_reset',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_lp_hq_valid_delay',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_lp_hq_read_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_static_rx_afifo_lp_hq_write_pointer_reset_value',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_afifo_lp_hq_write_reset',
                        f'root.u_dsp_rx_h.u_dsp_rx_regmap.o_rm_rx_afifo_lp_hq_read_reset'                           ], 
                        
                        clock = "root.line_ingress_clock", edge = simh.POSITIVE, begin = 0, step = STEP, end = END_LOG_RM, file_type = simh.TEXT, file_name_type = simh.SHORT, format = simh.UINT)
