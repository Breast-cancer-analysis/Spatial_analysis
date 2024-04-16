#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 20:46:51 2024

@author: tianpan
"""

# Code for all cell lines
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

DATAPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/all_data"
CELL_LINES = ['MDA-MB-231', 'MDA-MB-468','BT-474']
save_path = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/plots"
# Create an empty list to store all dataframes
dfs = []

# Load data for each cell line
for filename in os.listdir(DATAPATH):
    if filename.endswith('.csv') and 'sttc' in filename:
        # Extract cell line name from filename
        cell_line = filename.split('_')[0]
        
        
        filepath = os.path.join(DATAPATH, filename)
        full_df = pd.read_csv(filepath)
        # Add the cell line name as a new column in the dataframe
        full_df['Cell line'] = cell_line
            
        dfs.append(full_df)

# Concatenate all dataframes into one dataframe
combined_df = pd.concat(dfs, ignore_index=True)


# Sort the combined dataframe by the order of CELL_LINES
combined_df = combined_df.sort_values('Cell line')

# Set up seaborn settings
sns.set_theme(style="ticks")

# Initialize a grid of plots with an Axes for each cell line
grid = sns.FacetGrid(combined_df, col="Cell line",col_wrap=3, height=4)

# Draw a line plot for each cell line
grid.map(plt.scatter, "distance(um)", "STTC_plusminus5", s= 5)


for ax in grid.axes.flat:
    ax.axhspan(0.8, 1, color='grey', alpha=0.2)
    ax.axhspan(0.4, 1, color='blue', alpha=0.1)
    

# Set x and y axis labels
grid.set_axis_labels(r'Distance ($\mu$ m)', "Correlation Coefficient")
grid.set_titles("{col_name}", fontsize = 20)

# Adjust the arrangement of the plots
grid.fig.tight_layout(w_pad=1)

plt.savefig(os.path.join(save_path, 'sttc_5s_shaded.png'))

plt.show()

# ----- Plotting for specific cell lines ---------------------------------------------

import os
import pandas as pd
import matplotlib.pyplot as plt

DATAPATH = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/all_data"
CELL_LINES = ['MDA-MB-231', 'MDA-MB-468', 'BT-474']
save_path = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/plots"
# time_bins = ['STTC_plusminus1', 'STTC_plusminus5']  # Select if using STTC
time_bins = ['1','10'] # Select for PCC

# Create an empty list to store all dataframes
dfs = []

# Load data for each cell line and the specified time bins
for filename in os.listdir(DATAPATH):
    if filename.endswith('.csv') and 'pcc' in filename:  # Filter files with 'sttc'
        cell_line = filename.split('_')[0]  # Extract cell line name
        # if cell_line in CELL_LINES:  # Check if the cell line is in the specified list
        if cell_line in CELL_LINES:
            filepath = os.path.join(DATAPATH, filename)
            full_df = pd.read_csv(filepath)
            full_df['Cell line'] = cell_line  # Add the cell line name as a new column
            dfs.append(full_df)

# Concatenate all dataframes into one dataframe
combined_df = pd.concat(dfs, ignore_index=True)

# Sort the combined dataframe by the order of CELL_LINES
combined_df = combined_df.sort_values('Cell line')

# Create subplots for each cell line
fig, axs = plt.subplots(len(CELL_LINES), len(time_bins), figsize=(8, 12), sharex=True, sharey=True)

# Iterate over cell lines
for i, cell_line in enumerate(CELL_LINES):
    # Filter dataframe for the current cell line
    cell_line_df = combined_df[combined_df['Cell line'] == cell_line]
    
    # Iterate over time bins
    for j, time_bin in enumerate(time_bins):
        # Plot scatter plot for the current time bin
        axs[i, j].scatter(cell_line_df["distance(um)"], cell_line_df[time_bin], s=5)
        axs[i, j].set_title(cell_line, fontsize = 16)  # Set title for the subplot

        axs[i, j].axhspan(0.8, 1, color='grey', alpha=0.2)
        axs[i, j].axhspan(0.4, 1, color='blue', alpha=0.1)
        axs[i, j].tick_params(axis='y', labelsize=12)  # Set tick label font size

            
        if j == 0:
            axs[i, j].set_ylabel("Correlation Coefficient", fontsize = 14)  # Set y-axis label
      
      # Add x-axis label only for the bottom subplot
        if i == len(CELL_LINES) - 1:
            axs[i, j].set_xlabel("Distance ($\mu$m)",fontsize = 14)
            axs[i, j].tick_params(axis='x', labelsize=12)  # Set tick label font size

        
plt.tight_layout()  

plt.savefig('pcc.png')
plt.show() 

