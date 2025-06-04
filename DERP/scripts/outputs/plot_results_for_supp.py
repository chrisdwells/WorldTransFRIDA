import pandas as pd
import numpy as np
import copy 
import matplotlib.pyplot as plt

scenarios = {
    'NDC_EI_DERP2_HD':'black',
    # 'HD_ER_RCP85_1_CDD_30_20':'#2ca02c', 
    # 'HD_ER_RCP85_2_CDD_30_20':'#278c27', 
    # 'HD_ER_RCP85_3_CDD_30_20':'#217821', 
    # 'HD_ER_RCP85_4_CDD_30_20':'#1b641b', 
    # 'HD_ER_RCP85_5_CDD_30_20':'#165016', 
    'HD_ER_RCP85_1_CDD_20_10':'#1f77b4', 
    # 'HD_ER_RCP85_2_CDD_20_10':'#1b689e',
    # 'HD_ER_RCP85_3_CDD_20_10':'#175987', 
    # 'HD_ER_RCP85_4_CDD_20_10':'#134a71', 
    # 'HD_ER_RCP85_5_CDD_20_10':'#0f3b5a', 
    # 'HD_ER_RCP85_1_CDD_30_20_nCAP':'#9f4f09',
    'HD_ER_RCP85_1_CDD_20_10_nCAP':'#bf5f0a', 
    # 'HD_ER_RCP26_1_CDD_30_20_nCAP':'#df6f0c', 
    # 'HD_ER_RCP26_1_CDD_20_10_nCAP':'#ff7f0e',
             }

percs = ['', '_5th', '_95th']

y1 = 1980
y2 = 2155
years = np.arange(y1, y2, 5)

scenario_data = {}
for scenario in scenarios.keys():
    scenario_data[scenario] = {}
    for perc in percs:
        scenario_data[scenario][perc] = pd.read_csv(f"../../data/outputs/processed/with_elec_cap/FRIDA_{scenario}{perc}_bysource.csv", index_col=False)

varlist = [
    # "Temperature Anomaly",
    # "CO2 Emissions",
    # "CO2 Emissions|Energy",
    # "CO2 Emissions|Food and Land Use",
    # "Capacity|Electricity|Solar",
    # "Capacity|Electricity|Wind",
    # "Capacity|Biomass",
    # "Production|Biomass",
    # "Capacity|Coal",
    # "Capacity|Gas",
    # "Capacity|Oil",
    # "Capacity|Electricity|Hydro",
    # "Capacity|Electricity|Nuclear",
    # "Secondary Energy",
    # "Secondary Energy|Coal",
    # "Secondary Energy|Gas",
    # "Secondary Energy|Oil",
    # "Secondary Energy|Electricity|Nuclear",
    # "Secondary Energy|Biomass",
    # "Secondary Energy|Electricity|Hydro",
    # "Secondary Energy|Electricity|Solar",
    # "Secondary Energy|Electricity|Wind",
    "Capacity|Electricity",
    # "Capacity|Electricity|Coal",
    # "Capacity|Electricity|Gas",
    # "Capacity|Electricity|Oil",
]

    
#%%
plot_uncertainties = True

for var in varlist:
    varname = var.replace("|", " ")

    fig, axs = plt.subplots(1, 2, figsize=(8, 4))
    
    for scenario in scenarios.keys():
        
        data_in = {}
        for perc in percs:
            data_in[perc] = np.full(years.shape[0], np.nan)
            for y_i, year_i in enumerate(years):
                data_in[perc][y_i] = scenario_data[scenario][perc].loc[
                    scenario_data[scenario][perc]["Variable"] == var][
                        f"{year_i}"].values[0]

        axs[0].plot(years, data_in[''],
                 color=scenarios[scenario], alpha=1, label=scenario)
        
        if plot_uncertainties:
            axs[0].fill_between(years, data_in['_5th'], data_in['_95th'],
                     color=scenarios[scenario], alpha=0.3, linewidth=0)
            
        if scenario == 'NDC_EI_DERP2_HD':
            baseline_data = copy.deepcopy(data_in)
            continue
        
        
        axs[1].plot(years, data_in[''] - baseline_data[''],
                 color=scenarios[scenario], alpha=1, label=scenario)
        
        if plot_uncertainties:
            axs[1].fill_between(years, data_in['_5th'] - baseline_data['_5th'], 
                        data_in['_95th'] - baseline_data['_95th'],
                     color=scenarios[scenario], alpha=0.3, linewidth=0)
            
        
    axs[0].set_title(f'{varname}')
    axs[0].legend()
    
    axs[1].set_title(f'{varname} cf baseline')
    axs[1].legend()
    
    plt.tight_layout()

    plt.savefig(
        f"../../figures/for_supp/{varname}.png", dpi=100#, transparent=True
    )
    plt.clf()
    
    
#%%

frida_to_iamc = pd.read_csv('../../data/misc/FRIDA_to_IAMC.csv')

varlist_for_multi = [
    "Capacity|Coal",
    "Capacity|Gas",
    "Capacity|Oil",
    "Capacity|Biomass",
    "Capacity|Electricity|Hydro",
    "Capacity|Electricity|Nuclear",
    "Capacity|Electricity|Solar",
    "Capacity|Electricity|Wind",
    
    "Capacity|Electricity",

    "Temperature Anomaly",
    "CO2 Emissions",
    "CO2 Emissions|Energy",
    
    # "CO2 Emissions|Food and Land Use",
    # "Production|Biomass",
    # "Secondary Energy",
    # "Secondary Energy|Coal",
    # "Secondary Energy|Gas",
    # "Secondary Energy|Oil",
    # "Secondary Energy|Electricity|Nuclear",
    # "Secondary Energy|Biomass",
    # "Secondary Energy|Electricity|Hydro",
    # "Secondary Energy|Electricity|Solar",
    # "Secondary Energy|Electricity|Wind",
    # "Capacity|Electricity|Coal",
    # "Capacity|Electricity|Gas",
    # "Capacity|Electricity|Oil",
]

fig, axs = plt.subplots(4, 3, figsize=(12, 12))
axs = axs.ravel()

for v_i, var in enumerate(varlist_for_multi):
    varname = var.replace("|", " ")
    
    for scenario in scenarios.keys():
        
        data_in = {}
        for perc in percs:
            data_in[perc] = np.full(years.shape[0], np.nan)
            for y_i, year_i in enumerate(years):
                data_in[perc][y_i] = scenario_data[scenario][perc].loc[
                    scenario_data[scenario][perc]["Variable"] == var][
                        f"{year_i}"].values[0]

        axs[v_i].plot(years, data_in[''],
                 color=scenarios[scenario], alpha=1, label=scenario)
        
        if plot_uncertainties:
            axs[v_i].fill_between(years, data_in['_5th'], data_in['_95th'],
                     color=scenarios[scenario], alpha=0.3, linewidth=0)

    if var == 'Capacity|Electricity':
        units = 'GW'
    else:
        units = frida_to_iamc.loc[frida_to_iamc['IAMC name'] == var]['Units'].values[0]

    axs[v_i].set_ylabel(f'{units}')
    
    axs[v_i].set_title(f'{varname}')
    if v_i == 0:
        axs[v_i].legend()
    
plt.tight_layout()

plt.savefig(
    "../../figures/for_supp/panel_plot.png", dpi=100#, transparent=True
)
# plt.clf()
    
    
