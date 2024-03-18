#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 08:25:46 2024

@author: tianpan
"""

import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

# Datapath for 1 cell line
DATAPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/sorted_data/"
CELL_LINE = "wm" # can change for the relevant cell line
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
        plot_title = filename[:-4]
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
        
        # Creating the figures 
        plt.figure(figsize=(16, 12))
        plt.scatter(coords_df['x'], coords_df['y'], c='b', label='Cell positions', s=20)
        
        # Annotate each point with cell ID
        for i, txt in enumerate(coords_df['cell_id']):
            plt.annotate(txt, (coords_df['x'][i], coords_df['y'][i]), fontsize=15)
        
        plt.xlabel('x (um)')
        plt.ylabel('y (um)')
        plt.title(f'Spatial Distribution of Cells for {plot_title}')
        
        plt.savefig(f'spatialplot_{plot_title}.png')
        plt.close()
        # plt.show()

        

# Ignore: creates spatial figures and the timeseries in one plot
# # Creating figures
# fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(18, 20))

# axes[0].scatter(coords_df['x'], coords_df['y'], c='b', label='Cell positions', s=20)

# # Annotate each point with cell ID
# for i, txt in enumerate(coords_df['cell_id']):
#     axes[0].annotate(txt, (coords_df['x'][i], coords_df['y'][i]), fontsize=15)

# axes[0].set_xlabel('X/um')
# axes[0].set_ylabel('Y/um')
# axes[0].set_title('Spatial Distribution of Cells')

# # Plot the time series of the cells
# for i in range(len(timeseries_df)):
#     cell_data = timeseries_df.iloc[i]
#     timeseries = cell_data.iloc[3:] 
#     cell_id = cell_data.iloc[2].split('cell_')[-1] 
#     axes[1].plot(timeseries + i*0.1, label=f'Cell {cell_id}') 
# axes[1].set_xlabel('Time')
# axes[1].set_ylabel('Voltage')
# axes[1].legend()
# axes[1].set_title('Time Series of Cells')

# # Add an overall title for the figure
# fig.suptitle(f'Analysis of {plot_title}', fontsize=16)

# # Adjust layout to prevent overlap
# plt.tight_layout()

# plt.show()


        
