#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 11:31:40 2024

@author: tianpan
"""
#Try to create a function that can get all the distances and then I just add it to the end of the sttc data

import os
import numpy as np 
import pandas as pd

# Get the data
# SAVEPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/STTC_and_Distance"
SAVEPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/PCC_and_Distances_noabs"
DATAPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/sorted_data/"
CELL_LINE = ['MCF10A','MCF10A_TGFB','SUM159','T47D']

# STTC_PATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/hyperpolarisation_sttc"
STTC_PATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/PCC_noabs"
EVENTSFILE = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/original_data/events_data/20220423_original_and_review_all_events_df.csv"

# db for the x,y values
events_df = pd.read_csv(EVENTSFILE)

for cell_line in CELL_LINE:
    print("Starting:",cell_line)
    
    cell_line_folder = os.path.join(SAVEPATH, cell_line)
    os.makedirs(cell_line_folder, exist_ok=True)  # Create folder for each cell line
        
    # Reading mulitple files for each cell_line
    directory = os.path.join(DATAPATH, cell_line)
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            
            # Time series db
            timeseries_df = pd.read_csv(filepath)
            fov = filename[:-4]
            coords_list = []
            
            # Extract relevant data for a new coords df
            for index, row in timeseries_df.iterrows():
                cell_id = row['cell']
                cell_id_short = cell_id.split('cell_')[-1]
    
                # Getting the x and y positions of the cell
                cell_coordinates = events_df[events_df['cell_id'] == cell_id]
                x_pos = cell_coordinates['cell_x'].iloc[0]/1.04  # Lots of entries with the same position
                y_pos = cell_coordinates['cell_y'].iloc[0]/1.04
                    
                new_row = {'cell_id': cell_id_short, 'x': x_pos, 'y': y_pos}
                coords_list.append(new_row)
            
          
            # Concatenate all dictionaries into a DataFrame
            coords_df = pd.DataFrame(coords_list)
            
            if len(coords_df) == 1:
                print(f"Skipping {filename}: Only one cell present")
                continue
            
            else:
                # Calculate pairwise distances between cell positions
                distances_list = []
                for i in range(len(coords_df)):
                    for j in range(i + 1, len(coords_df)):
                        cell1_id = coords_df.iloc[i]['cell_id']
                        cell2_id = coords_df.iloc[j]['cell_id']
                        distance = np.sqrt((coords_df.iloc[i]['x'] - coords_df.iloc[j]['x']) ** 2 + 
                                    (coords_df.iloc[i]['y'] - coords_df.iloc[j]['y']) ** 2)
                        distances_list.append({'cell_1': cell1_id, 'cell_2': cell2_id, 'distance(um)': distance})
                    
                # Create a DataFrame to store distances
                distances_df = pd.DataFrame(distances_list)
                
                # # Loading the STTC files
                # sttc_files = 'sttc_' + fov + '.csv'
                # STTC_df = pd.read_csv(os.path.join(STTC_PATH,cell_line+"_sttc",sttc_files))
        
                # sttc_distance_df = pd.concat([distances_df,STTC_df],axis = 1)
                # sttc_distance_df = sttc_distance_df.drop(['FirstCell', 'SecndCell'], axis=1)
                
                sttc_files = fov + '.csv'
                STTC_df = pd.read_csv(os.path.join(STTC_PATH,cell_line,sttc_files))
        
                sttc_distance_df = pd.concat([distances_df,STTC_df],axis = 1)
                sttc_distance_df = sttc_distance_df.drop(['cell1', 'cell2'], axis=1)
                
                # Combines the PCC values with the 
                
                  # Save the combined DataFrame to the cell line folder
                combined_filepath = os.path.join(cell_line_folder, fov + '_pcc_and_distance_db.csv')
                sttc_distance_df.to_csv(combined_filepath, sep=',', index=False, encoding='utf-8')
            
        
        
