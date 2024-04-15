#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:11:53 2024

@author: tianpan
"""

import os
import pandas as pd

# Get the data
# SAVEPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/STTC_and_Distance"
SAVEPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/PCC_and_Distances_noabs"
EVENT_PATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/event_time_list"
EVENTSFILE = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/original_data/events_data/20220423_original_and_review_all_events_df.csv"
SAVEPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/events_and_distances"
# db for the x,y values
events_df = pd.read_csv(EVENTSFILE)

for filename in os.listdir(EVENT_PATH):
    if filename.endswith('.csv'):
        filepath = os.path.join(EVENT_PATH, filename)
        cell_line = filename.split('.csv')[0]

        eventtime_df = pd.read_csv(filepath)
        x_pos = []
        y_pos = []
        slip_area_list = []
        
        # Extract relevant data for a new coords df
        for index, row in eventtime_df.iterrows():
            cell_id = row['FOV_cell_label']
            slip_area = cell_id.split("_")[2:4]
            slip_area_list.append(("_").join(slip_area))

            # Getting the x and y positions of the cell
            cell_coordinates = events_df[events_df['cell_id'] == cell_id]
            x = cell_coordinates['cell_x'].iloc[0] # Lots of entries with the same position
            y = cell_coordinates['cell_y'].iloc[0]
            
            print(x,y)
                
            x_pos.append(x)
            y_pos.append(y)
            
        
        # Using DataFrame.insert() to add a column
        eventtime_df.insert(3,"cell_x", x_pos, True)
        eventtime_df.insert(4,"cell_y", y_pos, True)
        eventtime_df.insert(5,"slip_area", slip_area_list, True)
         
        
        combined_filepath = os.path.join(SAVEPATH, cell_line+'.csv')
        eventtime_df.to_csv(combined_filepath, sep=',', index=False, encoding='utf-8')
    
        
            