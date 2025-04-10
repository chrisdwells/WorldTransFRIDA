import pandas as pd
import numpy as np
import copy 
import matplotlib.pyplot as plt

baseline_data =  pd.read_csv("../../data/outputs/outputs_baseline_NDC.csv", index_col=False)
variant1_data =  pd.read_csv("../../data/outputs/HD_ER_RCP85_1_CDD_30_20.csv", index_col=False)

n_members = 1000


#%%
varlist = []

rename_dict = {}

for k_in in variant1_data.keys():
    if k_in == 'Year':
        continue
    k_out = copy.deepcopy(k_in)
    if '"' in k_in:
        k_out = k_in.split('="')[1].split('"')[0]
        rename_dict[k_in] = k_out
    if 'Run 1: ' in k_out:
    # if 'invest' in k:
        k_out_crop = k_out.split('Run 1: ')[1]
        print(k_out_crop)
        varlist.append(k_out_crop)
       
    
    
    #%%
# variant1_data = variant1_data.rename(columns=rename_dict)
# baseline_data = baseline_data.rename(columns=rename_dict)



       #%%
    
# varlist.remove('CCS.Storing CO2[1]')
    
for var in varlist:
    
    base_data = np.full((len(baseline_data['Year']), n_members), np.nan)
    
    for i in np.arange(n_members):
        base_data[:,i] = baseline_data[f'="Run {i+1}: {var}"']
        
        
    
    var_data = np.full((len(variant1_data['Year']), n_members), np.nan)
    
    for i in np.arange(n_members):
        var_data[:,i] = variant1_data[f'="Run {i+1}: {var}"']
        

    fig, axs = plt.subplots(1, 1, figsize=(6, 6))

    plt.plot(baseline_data['Year'], np.nanpercentile(base_data, 50, axis=1),
             color='black', alpha=1, label='NDC')
    
    plt.fill_between(baseline_data['Year'], np.nanpercentile(base_data, 16, axis=1),
             np.nanpercentile(base_data, 84, axis=1),
             color='black', alpha=0.3, linewidth=0)
    
    
    plt.plot(variant1_data['Year'], np.nanpercentile(var_data, 50, axis=1),
             color='green', alpha=1, label='HD_ER_RCP85_1_CDD_30_20')
    
    plt.fill_between(variant1_data['Year'], np.nanpercentile(var_data, 16, axis=1),
             np.nanpercentile(var_data, 84, axis=1),
             color='green', alpha=0.3, linewidth=0)
    
    diff = var_data - base_data
    
    
    plt.plot(variant1_data['Year'], np.nanpercentile(diff, 50, axis=1),
              color='red', alpha=1, label='Difference')
    
    plt.fill_between(variant1_data['Year'], np.nanpercentile(diff, 16, axis=1),
              np.nanpercentile(diff, 84, axis=1),
              color='red', alpha=0.3, linewidth=0)
    
    
    plt.title(f'{var}')
    
    # plt.xlim([2010, 2040])
    plt.legend()
    
    
