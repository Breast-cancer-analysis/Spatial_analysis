#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 09:08:11 2024

@author: tianpan
"""

import pandas as pd
import numpy as np
import os

DATAPATH = '/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/PCC_Distances'
CELL_LINE = '/468_all/'

# Initialize DataFrames to store PCC values
all_pcc_1s = pd.DataFrame(columns=['close', 'mid', 'far'])
all_pcc_10s = pd.DataFrame(columns=['close', 'mid', 'far'])
all_pcc_100s = pd.DataFrame(columns=['close', 'mid', 'far'])

directory = DATAPATH + CELL_LINE
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        fov = filename[:-4]
        
        # Loading the database with PCC and distances
        full_df = pd.read_csv(filepath)
        
        # Defining the distances of cells
        close_cells_df = full_df.loc[full_df['distance(um)'] < 37.5] 
        midrange_cells_df = full_df.loc[(full_df['distance(um)'] > 37.5) & (full_df['distance(um)'] < 100)]
        far_cells_df = full_df.loc[full_df['distance(um)'] > 100] 
        
        pcc_1s_vals = []
        pcc_10s_vals = []
        pcc_100s_vals = []
        PCC_types = ['PCC Value (1s)', 'PCC Value (10s)', 'PCC Value (100s)']

        for value in PCC_types:
            close_cells_pcc = np.corrcoef(close_cells_df['distance(um)'], close_cells_df[value])[0, 1]
            midrange_cells_pcc = np.corrcoef(midrange_cells_df['distance(um)'], midrange_cells_df[value])[0, 1]
            far_cells_pcc = np.corrcoef(far_cells_df['distance(um)'], far_cells_df[value])[0, 1]
            
            if value == 'PCC Value (1s)':
                pcc_1s_vals.extend([close_cells_pcc, midrange_cells_pcc, far_cells_pcc])
            elif value == 'PCC Value (10s)':
                pcc_10s_vals.extend([close_cells_pcc, midrange_cells_pcc, far_cells_pcc])
            elif value == 'PCC Value (100s)':
                pcc_100s_vals.extend([close_cells_pcc, midrange_cells_pcc, far_cells_pcc])
        
        all_pcc_1s.loc[fov] = pcc_1s_vals
        all_pcc_10s.loc[fov] = pcc_10s_vals
        all_pcc_100s.loc[fov] = pcc_100s_vals