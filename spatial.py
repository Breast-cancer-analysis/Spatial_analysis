import pickle
import pandas as pd
import numpy as np

# Data using is: cancer_cancer20220210_slip3_area1_20220210_slip3_area1_long_acq_blue_0.112_green_0.0673_L231_2_data.csv
DIR = '/Users/tianpan/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Yr3 Project/'
PCC_FILE = 'PCC_Stuff_David/Results/468/bin_width_'
FILE = 'PCC_cancer_cancer20220310_slip6_area3_long_acq_cancer20220310_slip6_area3_long_acq_blue_0.112_green_0.0673_L468_1_data.plk'
DISTANCE_MATRIX = 'distancematrix/L468_slip6_area3_distance_matrix.csv'



with open(DIR+PCC_FILE+'1.0/'+FILE, 'rb') as file:
    pcc_1s_array = pickle.load(file)
with open(DIR+PCC_FILE+'10.0/'+FILE, 'rb') as file:
    pcc_10s_array = pickle.load(file)
with open(DIR+PCC_FILE+'100.0/'+FILE, 'rb') as file:
    pcc_100s_array = pickle.load(file)


# Method 1
distance_df = pd.read_csv(DIR+DISTANCE_MATRIX)
distance_df.set_index('Unnamed: 0', inplace=True)

# Directly calculate the pcc by going allong each thing I think might be easiest
cells = distance_df.columns.tolist()
rows, cols = distance_df.shape
spatial_df = pd.DataFrame(index=range(rows), columns=range(cols))
pcc_pos = 0


# for i in range(cols):
#     for j in range(i,rows-1):
#         pcc_val = pcc_array[pcc_pos]
#         cell_i = int(cells[i])
#         cell_j = int(cells[j])
    
#         distance_val = distance_df.iloc[j,i]
#         #Calculate the pcc between them and try to figure out why it's giving me a nan :(
#         spatial_pcc = np.corrcoef(distance_val,pcc_val)[0, 1]
        
#         pcc_pos += 1

#         print(cell_i,cell_j, distance_val,pcc_val,spatial_pcc)
        
# try to convert the distance matrix into something that I had before: cell 1 vs cell 2 and distance - easier to order in that way, then have the pcc in the last row


# Method 2
all_data_df = pd.DataFrame(columns = ['cell_1','cell_2','distance/um','pcc_val (1s)','pcc_val (10s)','pcc_val (100s)'])

for i in range(cols):
    for j in range(i,rows-1):
        pcc_1s_val = pcc_1s_array[pcc_pos]
        pcc_10s_val = pcc_10s_array[pcc_pos]
        pcc_100s_val = pcc_100s_array[pcc_pos]
        cell_i = int(cells[i])
        cell_j = int(cells[j])
    
        distance_val = distance_df.iloc[j,i]/1.04
        #Calculate the pcc between them and try to figure out why it's giving me a nan :(
        
        all_data_df.loc[len(all_data_df.index)] = [cell_i, cell_j, distance_val,pcc_1s_val,pcc_10s_val,pcc_100s_val] 
        pcc_pos += 1

        print(cell_i,cell_j, distance_val,pcc_1s_val,pcc_10s_val,pcc_100s_val)
        
        
sorted_distances = all_data_df.sort_values(by='distance/um', ascending=True)
        
        