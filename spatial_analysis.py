#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 07:34:56 2024

@author: tianpan
"""
import pandas as pd
import numpy as np
import os
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

def process_data(file_path, method_prefix, method_types):
    data = []
    for filename in os.listdir(file_path):
        if filename.endswith('.csv') and method_prefix in filename:
            filepath = os.path.join(file_path, filename)
            cell_line = filename.split("_")[0]
            full_df = pd.read_csv(filepath)
            full_df = full_df.dropna()
            
            for value in method_types:
                filtered_df = full_df[full_df[value] > 0.4]

                if len(filtered_df) > 2:
                    percentage = len(filtered_df) / len(full_df) * 100
                    x = filtered_df['distance(um)']
                    y = filtered_df[value]
                    pcc = stats.pearsonr(x,y)
                    pcc_val =  pcc.correlation
                    pcc_CI = list(pcc.confidence_interval(confidence_level=0.9))
                    
                    # spearman = stats.spearmanr(x, y)
                    # spearman_val = spearman.correlation
                    # spearman_pval = spearman.pvalue
                    # data.append({"Cell line": cell_line, "Time bin": value, "Filtered Points": len(filtered_df),"Total Points": len(full_df),"Percentage > 0.4": percentage})
                    
                    data.append({"Cell line": cell_line, "Time bin": value, "PCC Value": pcc_val, "PCC CI lower": pcc_CI[0], "PCC CI upper": pcc_CI[1],
                                 "Points > 0": len(filtered_df),"Total Points": len(full_df), "Percentage > 0.": percentage})
                else:
                    print(filename)
    return pd.DataFrame(data)

def plot_dataframe(df,fig_width, fig_height,save_path):
    df = df.sort_values('Cell line')
    
    # Get unique cell lines
    unique_cell_lines = df["Cell line"].unique()
    
    # Generate a dictionary to map each cell line to a color
    color_map = {cell_line: plt.cm.tab10.colors[i % len(plt.cm.tab10.colors)] for i, cell_line in enumerate(unique_cell_lines)}


    time_bins = df["Time bin"].unique()
    num_bins = len(time_bins)
    
    fig, axes = plt.subplots(nrows=num_bins, ncols=1, figsize=(fig_width, fig_height))
    
    for i, time_bin in enumerate(time_bins):
        df_bin = df[df["Time bin"] == time_bin]
        ax = axes[i] if num_bins > 1 else axes
        for cell_line in df_bin["Cell line"].unique():
            df_subset = df_bin[df_bin["Cell line"] == cell_line]
            color = color_map[cell_line]  # Get color from the dictionary
            ax.scatter(df_subset["PCC Value"], df_subset["Cell line"], label=cell_line, color=color, s=70)
            x_values = df_subset["PCC Value"]
            y_values = [cell_line] * len(df_subset)
            xerr = [abs(df_subset["PCC Value"] - df_subset["PCC CI lower"]), abs(df_subset["PCC CI upper"] - df_subset["PCC Value"])]
            ax.errorbar(x=x_values, y=y_values, xerr=xerr, fmt='none', c=color, capsize=8,linewidth = 3)
        ax.axvline(x=0, color='black', linestyle='--')
        ax.set_ylabel("Cell line", fontsize = 14)
        ax.tick_params(axis='y', labelsize=12) 
        if "STTC" in time_bin:
            time = time_bin.split("minus")[1]
            ax.set_title(r"Time window = $\pm$"+f"{time}s", fontsize = 16)
        else:
            ax.set_title(f"Time bin = {time_bin}s", fontsize = 16)
        ax.set_xlim(-1.0, 1.0)
        ax.grid()
        if i == num_bins - 1:
            ax.set_xlabel("Correlation Coefficient", fontsize = 14)
            ax.tick_params(axis='x', labelsize=12) 
        else:
            ax.set_xticklabels([])
    
    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
    
    plt.savefig(os.path.join(save_path, 'PCC_plots_for_PCC_4.png'))
    
    plt.show() 
    
def main():
    file_path = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/3rd Year/Project/all_data"
    # Process pcc data
    pcc_prefix = '_pcc_'
    pcc_types = ['1', '10']
    pcc_vals_df = process_data(file_path, pcc_prefix, pcc_types)
    
    # Process sttc data
    sttc_prefix = '_sttc_'
    sttc_types = ['STTC_plusminus1', 'STTC_plusminus5'] #'STTC_plusminus10'
    sttc_vals_df = process_data(file_path, sttc_prefix, sttc_types)
    
    return pcc_vals_df, sttc_vals_df

if __name__ == "__main__":
    save_path = "/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/Tian_spatial_analysis/Plots/PCC_result_plots"

    pcc_vals_df, sttc_vals_df = main()
    
    plot_dataframe(pcc_vals_df,8,8,save_path)
    # plot_dataframe(sttc_vals_df,8,8,save_path)
