#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:11:02 2024

@author: tianpan
"""

import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt


# Get the data - testing for 1 FOV
DATAPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/sorted_data/"
CELL_LINE = "231"
EVENTSFILE = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/original_data/events_data/20220423_original_and_review_all_events_df.csv"

# db for the x,y values
events_df = pd.read_csv(EVENTSFILE)

# Reading mulitple files for each cell_line
directory = DATAPATH + CELL_LINE
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        
        # Time series db
        timeseries_df = pd.read_csv(filepath)
        fov = filename[:-4]+'_distances.csv'
        coords_list = []
        
        # Extract relevant data for a new coords df
        for index, row in timeseries_df.iterrows():
            cell_id = row['cell']
            cell_id_short = cell_id.split('cell_')[-1]

            # Getting the x and y positions of the cell
            cell_coordinates = events_df[events_df['cell_id'] == cell_id]
            x_pos = cell_coordinates['cell_x'].iloc[0]  # Lots of entries with the same position
            y_pos = cell_coordinates['cell_y'].iloc[0]
                
            new_row = {'cell_id': cell_id_short, 'x': x_pos, 'y': y_pos}
            coords_list.append(new_row)
        
      
        # Concatenate all dictionaries into a DataFrame
        coords_df = pd.DataFrame(coords_list)

        # Create an excel that has a new sheet for the different FOV
        # Calculate pairwise distances between cell positions
        distances_list = []
        for i in range(len(coords_df)):
            for j in range(i + 1, len(coords_df)):
                cell1_id = coords_df.iloc[i]['cell_id']
                cell2_id = coords_df.iloc[j]['cell_id']
                distance = np.sqrt((coords_df.iloc[i]['x'] - coords_df.iloc[j]['x']) ** 2 + 
                            (coords_df.iloc[i]['y'] - coords_df.iloc[j]['y']) ** 2)
                distances_list.append({'cell_1': cell1_id, 'cell_2': cell2_id, 'distance': distance})
            
        # Create a DataFrame to store distances
        distances_df = pd.DataFrame(distances_list)
        distances_df.to_csv(fov, sep=',', index=False, encoding='utf-8')

        
        