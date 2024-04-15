#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 19:03:58 2024

@author: tianpan
"""

import pickle
import pandas as pd
import numpy as np

# Data using is: cancer_cancer20220210_slip3_area1_20220210_slip3_area1_long_acq_blue_0.112_green_0.0673_L231_2_data.csv
DIR = '/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/'
PCC_FILE = 'PCC_Stuff_David/Results/231/bin_width_'
FILE = 'PCC_cancer_cancer20220209_slip2_area2_long_acq_20220209_slip2_area2_long_acq_blue_0.112_green_0.0673_L231_1_data.csv'
DISTANCE_DF = '/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/spatial_distances/231/cancer_20201207_slip1_area1_long_acq_corr_corr_long_acqu_blue_0.03465_green_0.07063_heated_to_37_1_data_distances.csv'

with open(DIR+PCC_FILE+'1.0/'+FILE, 'rb') as file1:
    pcc_1s_array = pickle.load(file1)
with open(DIR+PCC_FILE+'10.0/'+FILE, 'rb') as file2:
    pcc_10s_array = pickle.load(file2)
with open(DIR+PCC_FILE+'100.0/'+FILE, 'rb') as file3:
    pcc_100s_array = pickle.load(file3)
    
pcc_df = pd.DataFrame(np.transpose([pcc_1s_array,pcc_10s_array,pcc_100s_array]), columns = ['PCC Value (1s)','PCC Value (10s)','PCC Value (100s)'])


#231 
# 'cancer_cancer20220209_slip2_area2_long_acq_20220209_slip2_area2_long_acq_blue_0.112_green_0.0673_L231_1_data.csv'
# 'cancer_cancer20220210_slip3_area1_20220210_slip3_area1_long_acq_blue_0.112_green_0.0673_L231_2_data.csv'
# 'cancer_20201218_slip2_area1_long_acq_long_acq_blue_0.0318_green_0.0772_heated_to_37_1_data.csv'
# 'cancer_20201217_slip2_area1_long_acq_foc_correct_long_acq_blue_0.0318_green_0.0772_heated_to_37_1_data.csv'
# 'cancer_20201219_slip1_area1_long_acq_long_acq_blue_0.0318_green_0.0772_heated_to_37_1_data.csv'

#468 
# cancer_cancer20220315_slip1_area1_long_acq_cancer20220315_slip1_area1_long_acq_blue_0.112_green_0.0673_L468_1_data.csv
# cancer_cancer20220309_slip4_area2_long_acq_cancer20220309_slip4_area2_long_acq_blue_0.112_green_0.0673_L468_1_data.csv
# cancer_cancer20220310_slip3_area4_long_acq_cancer20220310_slip3_area4_long_acq_blue_0.112_green_0.0673_L468_1_data.csv
# cancer_cancer20220311_slip2_area1_long_acq_cancer20220311_slip2_area1_long_acq_blue_0.112_green_0.0673_L468_1_data.csv