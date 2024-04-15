#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:11:02 2024

@author: tianpan
"""

import os
import numpy as np 
import pandas as pd
import pickle

# Filepath to save the data
SAVEPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/PCC_Distances"

#Filepaths for the data
DATAPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/sorted_data/"
CELL_LINE =  ['231','468','453','BT474','Cal51','MCF10A','MCF10A_TGFB','SUM159','T47D']
PCC_PATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/PCC_Stuff_David/Results_2"
EVENTSFILE = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/original_data/events_data/20220423_original_and_review_all_events_df.csv"

# Dataframe for the events data to get the x,y coordinates
events_df = pd.read_csv(EVENTSFILE)

invalid_files = []

for cell_line in CELL_LINE:
    print("Starting:",cell_line)
    
    cell_line_folder = os.path.join(SAVEPATH, cell_line)
    os.makedirs(cell_line_folder, exist_ok=True)  # Create folder for each cell line
    
    # Reading multiple files for each cell_line
    directory = os.path.join(DATAPATH, cell_line)
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            try:
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
                    x_pos = cell_coordinates['cell_x'].iloc[0] / 1.04  # Lots of entries with the same position
                    y_pos = cell_coordinates['cell_y'].iloc[0] / 1.04
                        
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
                    
                    # Load PCC values
                    pcc_file ='PCC_'+fov+'.plk'
                    with open(os.path.join(PCC_PATH,cell_line, 'bin_width_1.0', pcc_file), 'rb') as file1:
                        pcc_1s_array = pickle.load(file1)
                    with open(os.path.join(PCC_PATH,cell_line, 'bin_width_10.0', pcc_file), 'rb') as file2:
                        pcc_10s_array = pickle.load(file2)
                    with open(os.path.join(PCC_PATH,cell_line, 'bin_width_100.0', pcc_file), 'rb') as file3:
                        pcc_100s_array = pickle.load(file3)
                        
                    pcc_df = pd.DataFrame(np.transpose([pcc_1s_array, pcc_10s_array, pcc_100s_array]), 
                                          columns=['PCC Value (1s)', 'PCC Value (10s)', 'PCC Value (100s)'])
            
                    distance_pcc_df = pd.concat([distances_df, pcc_df], axis=1)
                    
                    # Save the combined DataFrame to the cell line folder
                    combined_filepath = os.path.join(cell_line_folder, fov + '_pcc_and_distance_db.csv')
                    distance_pcc_df.to_csv(combined_filepath, sep=',', index=False, encoding='utf-8')
            
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                invalid_files.append(filename)
                continue
            
     
print("Invalid files:", invalid_files)

