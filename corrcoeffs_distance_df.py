#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 19:07:38 2024

@author: tianpan
"""

import os
import numpy as np 
import pandas as pd
import pickle

def load_events_data(events_file):
    return pd.read_csv(events_file)

# PCC files are in a plk format so this helps to format it
def load_pcc_data(cell_line, pcc_path, fov, bin_widths):
    pcc_data = {}
    for bin_width in bin_widths:
        with open(os.path.join(pcc_path, cell_line, f'bin_width_{bin_width}', f'PCC_{fov}.plk'), 'rb') as file:
            pcc_array = pickle.load(file)
            pcc_data[f'PCC Value ({bin_width}s)'] = pcc_array
    return pd.DataFrame(pcc_data)

# Create a csv with the pcc values and distances
def combine_pcc_and_distance(cell_line, pcc_path, data_path, events_df, save_path):
    cell_line_folder = os.path.join(save_path, cell_line)
    os.makedirs(cell_line_folder, exist_ok=True)  # Create folder for each cell line

    for filename in os.listdir(os.path.join(data_path, cell_line)):
        if filename.endswith('.csv'):
            try:
                filepath = os.path.join(data_path, cell_line, filename)
                timeseries_df = pd.read_csv(filepath)
                fov = filename[:-4]
                coords_list = []

                for index, row in timeseries_df.iterrows():
                    cell_id = row['cell']
                    cell_id_short = cell_id.split('cell_')[-1]
                    cell_coordinates = events_df[events_df['cell_id'] == cell_id]
                    x_pos = cell_coordinates['cell_x'].iloc[0] / 1.04
                    y_pos = cell_coordinates['cell_y'].iloc[0] / 1.04
                    new_row = {'cell_id': cell_id_short, 'x': x_pos, 'y': y_pos}
                    coords_list.append(new_row)

                coords_df = pd.DataFrame(coords_list)

                if len(coords_df) == 1:
                    print(f"Skipping {filename}: Only one cell present")
                    continue

                else:
                    distances_list = []
                    for i in range(len(coords_df)):
                        for j in range(i + 1, len(coords_df)):
                            cell1_id = coords_df.iloc[i]['cell_id']
                            cell2_id = coords_df.iloc[j]['cell_id']
                            distance = np.sqrt((coords_df.iloc[i]['x'] - coords_df.iloc[j]['x']) ** 2 + 
                                        (coords_df.iloc[i]['y'] - coords_df.iloc[j]['y']) ** 2)
                            distances_list.append({'cell_1': cell1_id, 'cell_2': cell2_id, 'distance(um)': distance})

                    distances_df = pd.DataFrame(distances_list)
                    pcc_df = load_pcc_data(cell_line, pcc_path, fov, [1.0, 10.0, 100.0])
                    distance_pcc_df = pd.concat([distances_df, pcc_df], axis=1)
                    combined_filepath = os.path.join(cell_line_folder, fov + '_pcc_and_distance_db.csv')
                    distance_pcc_df.to_csv(combined_filepath, sep=',', index=False, encoding='utf-8')

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Create a csv with the sttc values and distances
def combine_sttc_and_distance(cell_line, sttc_path, data_path, events_df, save_path):
    cell_line_folder = os.path.join(save_path, cell_line)
    os.makedirs(cell_line_folder, exist_ok=True)  # Create folder for each cell line

    for filename in os.listdir(os.path.join(data_path, cell_line)):
        if filename.endswith('.csv'):
            try:
                filepath = os.path.join(data_path, cell_line, filename)
                timeseries_df = pd.read_csv(filepath)
                fov = filename[:-4]
                coords_list = []

                for index, row in timeseries_df.iterrows():
                    cell_id = row['cell']
                    cell_id_short = cell_id.split('cell_')[-1]
                    cell_coordinates = events_df[events_df['cell_id'] == cell_id]
                    x_pos = cell_coordinates['cell_x'].iloc[0] / 1.04
                    y_pos = cell_coordinates['cell_y'].iloc[0] / 1.04
                    new_row = {'cell_id': cell_id_short, 'x': x_pos, 'y': y_pos}
                    coords_list.append(new_row)

                coords_df = pd.DataFrame(coords_list)

                if len(coords_df) == 1:
                    print(f"Skipping {filename}: Only one cell present")
                    continue

                else:
                    distances_list = []
                    for i in range(len(coords_df)):
                        for j in range(i + 1, len(coords_df)):
                            cell1_id = coords_df.iloc[i]['cell_id']
                            cell2_id = coords_df.iloc[j]['cell_id']
                            distance = np.sqrt((coords_df.iloc[i]['x'] - coords_df.iloc[j]['x']) ** 2 + 
                                        (coords_df.iloc[i]['y'] - coords_df.iloc[j]['y']) ** 2)
                            distances_list.append({'cell_1': cell1_id, 'cell_2': cell2_id, 'distance(um)': distance})

                    distances_df = pd.DataFrame(distances_list)
                    sttc_df = pd.read_csv(os.path.join(sttc_path, f'{cell_line}_sttc', f'sttc_{fov}.csv'))
                    sttc_distance_df = pd.concat([distances_df, sttc_df], axis=1)
                    sttc_distance_df = sttc_distance_df.drop(['FirstCell', 'SecndCell'], axis=1)
                    combined_filepath = os.path.join(cell_line_folder, fov + '_sttc_and_distance_db.csv')
                    sttc_distance_df.to_csv(combined_filepath, sep=',', index=False, encoding='utf-8')

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Define paths and filenames
SAVE_PATH_PCC = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/PCC_Distances"
SAVE_PATH_STTC = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/STTC_and_Distance"
DATAPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/sorted_data/"
PCC_PATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/PCC_Stuff_David/Results_2"
STTC_PATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/hyperpolarisation_sttc"
EVENTSFILE = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/original_data/events_data/20220423_original_and_review_all_events_df.csv"
CELL_LINE = ['231','468','453','BT474','Cal51','MCF10A','MCF10A_TGFB','SUM159','T47D']

# Load events data
events_df = load_events_data(EVENTSFILE)

# Combine PCC and distance data
for cell_line in CELL_LINE:
    combine_pcc_and_distance(cell_line, PCC_PATH, DATAPATH, events_df, SAVE_PATH_PCC)

# Combine STTC and distance data
for cell_line in CELL_LINE:
    combine_sttc_and_distance(cell_line, STTC_PATH, DATAPATH, events_df, SAVE_PATH_STTC)
