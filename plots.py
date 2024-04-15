#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 19:08:53 2024

@author: tianpan
"""
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def load_data_frame(cell_line, data_path, file_suffix):
    full_df = pd.DataFrame()
    directory = os.path.join(data_path, cell_line)
    for filename in os.listdir(directory):
        if filename.endswith(file_suffix):
            filepath = os.path.join(directory, filename)
            fov = filename[:-len(file_suffix)]
            fov_df = pd.read_csv(filepath)
            full_df = pd.concat([full_df, fov_df], ignore_index=True)

    return full_df

def plot_pcc_against_distance(cell_lines, pcc_path, save_path):
    for cell_line in cell_lines:
        plt.figure(figsize=(8, 6))
        full_df = load_data_frame(cell_line, pcc_path, '.csv')
        plt.scatter(full_df['distance(um)'], full_df['1'], s=5, label=cell_line)
        plt.xlabel(r'distance ($\mu$m)')
        plt.ylabel(r'PCC (1s)')
        plt.title(f'PCC against distance for 1s for {cell_line}')
        # plt.savefig(os.path.join(save_path, f'{cell_line}_pcc_1s.png'))
        plt.show()
        
        plt.figure(figsize=(8, 6))
        full_df = load_data_frame(cell_line, pcc_path, '.csv')
        plt.scatter(full_df['distance(um)'], full_df['10'], s=5, label=cell_line)
        plt.xlabel(r'distance ($\mu$m)')
        plt.ylabel(r'PCC (10s)')
        plt.title(f'PCC against distance for 10s for {cell_line}')
        # plt.savefig(os.path.join(save_path, f'{cell_line}_pcc_10s.png'))
        plt.show()
        
        # plt.figure(figsize=(8, 6))
        # full_df = load_data_frame(cell_line, pcc_path, '.csv')
        # plt.scatter(full_df['distance(um)'], full_df['100'], s=5, label=cell_line)
        # plt.xlabel(r'distance ($\mu$m)')
        # plt.ylabel(r'PCC (100s)')
        # plt.title(f'PCC against distance for 100s for {cell_line}')
        # plt.savefig(os.path.join(save_path, f'{cell_line}_pcc_100s.png'))
        # plt.show()

def plot_sttc_against_distance(cell_lines, sttc_path, save_path):
    for cell_line in cell_lines:
        full_df = load_data_frame(cell_line, sttc_path, '.csv')
        
        plt.figure(figsize=(8, 6))
        plt.scatter(full_df['distance(um)'], full_df['STTC_plusminus1'], s=5, label=cell_line)
        plt.xlabel(r'distance ($\mu$m)')
        plt.ylabel(r'STTC ($\pm 1$)')
        plt.title(f'STTC against Distance for 1s for {cell_line}')
        # plt.savefig(os.path.join(save_path, f'{cell_line}_sttc_1s.png'))
        plt.show()
        
        plt.figure(figsize=(8, 6))
        plt.scatter(full_df['distance(um)'], full_df['STTC_plusminus5'], s=5, label=cell_line)
        plt.xlabel(r'distance ($\mu$m)')
        plt.ylabel(r'STTC ($\pm 5$)')
        plt.title(f'STTC against distance for 5s for {cell_line}')
        # plt.savefig(os.path.join(save_path, f'{cell_line}_sttc_5s.png'))
        plt.show()
        
        plt.figure(figsize=(8, 6))
        plt.scatter(full_df['distance(um)'], full_df['STTC_plusminus10'], s=5, label=cell_line)
        plt.xlabel(r'distance ($\mu$m)')
        plt.ylabel(r'STTC ($\pm 10$)')
        plt.title(f'STTC against distance for 10s for {cell_line}')
        # plt.savefig(os.path.join(save_path, f'{cell_line}_sttc_10s.png'))
        plt.show()

CELL_LINE = ['231','468','453','BT474','Cal51','MCF10A','MCF10A_TGFB','SUM159','T47D']
# PCC_PATH = '/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/PCC_and_Distances'
PCC_PATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/PCC_and_Distances_noabs"
# STTC_PATH = '/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/STTC_and_Distance'
SAVE_PATH = '/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/Plots/PCC_noabs'
SAVE_PATH = '/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/'

# plot_pcc_against_distance(CELL_LINE, PCC_PATH, SAVE_PATH)

# plot_sttc_against_distance(CELL_LINE, STTC_PATH, SAVE_PATH)

for cell_line in CELL_LINE:
    distance_pcc_df = load_data_frame(cell_line,PCC_PATH,'.csv')
    
    pcc_filepath = os.path.join(SAVE_PATH, cell_line + '_pcc_and_distance_db.csv')
    distance_pcc_df.to_csv(pcc_filepath, sep=',', index=False, encoding='utf-8')
    
    # distance_sttc_df = load_data_frame(cell_line,STTC_PATH,'.csv')
    
    # sttc_filepath = os.path.join(SAVE_PATH, cell_line + '_sttc_and_distance_db.csv')
    # distance_sttc_df.to_csv(sttc_filepath, sep=',', index=False, encoding='utf-8')
    

