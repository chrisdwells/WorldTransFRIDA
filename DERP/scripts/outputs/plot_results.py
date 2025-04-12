import pandas as pd
import numpy as np
# import copy 
import matplotlib.pyplot as plt
import math

scenarios = [
    'HD_ER_RCP85_1_CDD_30_20', 
    'HD_ER_RCP85_2_CDD_30_20', 
    'HD_ER_RCP85_3_CDD_30_20', 
    'HD_ER_RCP85_4_CDD_30_20', 
    'HD_ER_RCP85_5_CDD_30_20', 
    'HD_ER_RCP85_1_CDD_20_10', 
    'HD_ER_RCP85_2_CDD_20_10', 
    'HD_ER_RCP85_3_CDD_20_10', 
    'HD_ER_RCP85_4_CDD_20_10', 
    'HD_ER_RCP85_5_CDD_20_10', 
    'HD_ER_RCP85_1_CDD_30_20_nCAP',
    'HD_ER_RCP85_1_CDD_20_10_nCAP', 
    'HD_ER_RCP26_1_CDD_30_20_nCAP', 
    'HD_ER_RCP26_1_CDD_20_10_nCAP'
             ]

scenario_data = {}

for scenario in scenarios:
    scenario_data[scenario] = pd.read_csv(f"../../data/outputs/raw/{scenario}.csv", index_col=False)

baseline_data =  pd.read_csv("../../data/outputs/raw/NDC_EI_DERP2_HD.csv", index_col=False)

n_members = 1000

varlist = [
     'Energy Balance Model.Surface Temperature Anomaly[1]',
     'Emissions.Total CO2 Emissions[1]',
     'Emissions.CO2 emissions from Energy[1]',
     'Emissions.CO2 Emissions from Food and Land Use[1]',
     'solar energy.Current Solar Capacity[1]',
     'wind energy.Current Wind Capacity[1]',
     'bio fuel energy.bio fuel production Capacity[1]',
     'bio fuel energy.bio fuel production[1]',
     'fossil energy coal.Fossil Energy and Fuel Capital[1]',
     'fossil energy gas.Fossil Energy and Fuel Capital[1]',
     'fossil energy oil.Fossil Energy and Fuel Capital[1]',
     'hydropower energy.Hydropower Energy Capacity[1]',
     'nuclear energy.Nuclear Energy Capacity[1]',
     'energy supply.Total Energy Output[1]',
     'fossil energy coal.Secondary Fossil Energy Output[1]',
     'fossil energy gas.Secondary Fossil Energy Output[1]',
     'fossil energy oil.Secondary Fossil Energy Output[1]',
     'nuclear energy.Nuclear Energy Output[1]',
     'bio fuel energy.bio fuel secondary energy output[1]',
     'hydropower energy.Hydropower Energy Output[1]',
     'solar energy.Solar Energy Output[1]',
     'wind energy.Wind Energy Output[1]',
         ]
    
#%%
remove_nans = True
plot_diff = False
plot_uncertainties = False
# find the indices where all the runs have full data. 
# we have to make sure we're plotting the same members for each scenario, so
# if the member has nans for any scenario then it has to be discarded - if we
# have the remove_nans flag.
keep = np.arange(n_members)

if remove_nans:
    print(len(keep))
    
    # just do for one var - have checked that if it's nan for one it's nan for
    # all, since the run has failed
    var = varlist[0]
    base_data = np.full((len(baseline_data['Year']), n_members), np.nan)
    for i in np.arange(n_members):
        base_data[:,i] = baseline_data[f'="Run {i+1}: {var}"']
        
    keep_base = [idx for idx in np.arange(n_members) if math.isnan(base_data[-1,idx]) == False]
    keep = np.intersect1d(keep, keep_base)
    
    print(len(keep))
    
    for scenario in scenarios:
    
        var_data = np.full((len(scenario_data[scenario]['Year']), n_members), np.nan)
        for i in np.arange(n_members):
            var_data[:,i] = scenario_data[scenario][f'="Run {i+1001}: {var}"']
            
        keep_var = [idx for idx in np.arange(n_members) if math.isnan(var_data[-1,idx]) == False]
        keep = np.intersect1d(keep, keep_var)
        
        print(len(keep))

np.savetxt(
    "../../data/misc/keep_idxs.csv",
    keep.astype(int),
    fmt="%d",
)

name_str = ''
if remove_nans:
    name_str = name_str + '_no_nans'
if plot_uncertainties:
    name_str = name_str + 'with 5-95%'    
    
perc_removed = 100*((n_members - (len(keep)))/n_members)

for var in varlist:
    varname = var.split(".")[1][:-3]
    if "fossil" in var:
        carrier = var.split(".")[0].split(" ")[-1]
        varname = varname + ' ' + carrier
    
    base_data = np.full((len(baseline_data['Year']), n_members), np.nan)
    
    for i in np.arange(n_members):
        base_data[:,i] = baseline_data[f'="Run {i+1}: {var}"']
        

    fig, axs = plt.subplots(1, 1, figsize=(6, 6))


    plt.plot(baseline_data['Year'], np.nanpercentile(base_data[:,keep], 50, axis=1),
             color='black', alpha=1, label='NDC')
    
    if plot_uncertainties:
        plt.fill_between(baseline_data['Year'], np.nanpercentile(base_data[:,keep], 5, axis=1),
                 np.nanpercentile(base_data[:,keep], 95, axis=1),
                 color='black', alpha=0.3, linewidth=0)
        
    
    for s_i, scenario in enumerate(scenarios):
        print(scenario)
    
        var_data = np.full((len(scenario_data[scenario]['Year']), n_members), np.nan)
        
        for i in np.arange(n_members):
            var_data[:,i] = scenario_data[scenario][f'="Run {i+1001}: {var}"']
            
        
        plt.plot(scenario_data[scenario]['Year'], np.nanpercentile(var_data[:,keep], 50, axis=1),
                 color=plt.cm.tab20(s_i), alpha=1, label=scenario)
        
        if plot_uncertainties:
            plt.fill_between(scenario_data[scenario]['Year'], np.nanpercentile(var_data[:,keep], 5, axis=1),
                     np.nanpercentile(var_data[:,keep], 95, axis=1),
                     color=plt.cm.tab20(s_i), alpha=0.3, linewidth=0)
            
        
        
        if plot_diff:
            diff = var_data[:,keep] - base_data[:,keep]
            
            plt.plot(scenario_data[scenario]['Year'], np.nanpercentile(diff, 50, axis=1),
                      color='red', alpha=1, label='Difference')
            
            if plot_uncertainties:
                plt.fill_between(scenario_data[scenario]['Year'], np.nanpercentile(diff, 5, axis=1),
                          np.nanpercentile(diff, 95, axis=1),
                          color='red', alpha=0.3, linewidth=0)
                
        
    plt.title(f'{varname} {name_str} {perc_removed}% removed')
    
    # plt.xlim([2010, 2040])
    plt.legend()
    
    plt.tight_layout()
    

    plt.savefig(
        f"../../figures/{varname}{name_str}.png", dpi=100#, transparent=True
    )
    plt.clf()
    
    
